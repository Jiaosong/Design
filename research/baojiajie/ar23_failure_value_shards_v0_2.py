#!/usr/bin/env python3
"""Baojiajie AR23 category-shard fallback v0.2.

Why this exists
---------------
The Dataset Viewer /search endpoint for the combined 571M-row derivative can
return HTTP 500. This fallback avoids the search service: it lists Parquet
files in relevant category folders, chooses evenly spaced shards, downloads
those shards from the Hugging Face Hub, scans them locally, and writes a
balanced discovery corpus.

Evidence boundary
-----------------
This is a CATEGORY-SHARD DISCOVERY SAMPLE, not a probability sample of Amazon
customers and not a prevalence estimator. Outputs contain short evidence
excerpts (<=20 words), not full review text. Automatic codes must be manually
reviewed before being promoted to project evidence.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import random
import re
from collections import defaultdict
from pathlib import Path

import pyarrow.compute as pc
import pyarrow.parquet as pq
from huggingface_hub import HfApi, hf_hub_download

DATASET = "bagadbilla/amazon-reviews-2023-trimmed"
SOURCE_FOLDERS = ["Home_and_Kitchen", "Tools_and_Home_Improvement"]

PRODUCT_RULES = {
    "mop": {
        "include": re.compile(r"\b(mop|mops|mopping|spin mop|sponge mop|flat mop|spray mop|microfiber mop|floor mop|dust mop)\b", re.I),
        "exclude": None,
    },
    "cleaning_brush": {
        "include": re.compile(r"\b(cleaning brush|scrub brush|scrubbing brush|bathroom brush|grout brush|tile brush|dish brush|floor scrub brush|scrubber brush)\b", re.I),
        "exclude": re.compile(r"\b(hair ?brush|tooth ?brush|toothbrush|makeup brush|nail brush|body brush|shaving brush|eyelash|mascara|scalp brush|paint brush)\b", re.I),
    },
    "squeegee": {
        "include": re.compile(r"\b(squeegee|shower squeegee|window squeegee|floor squeegee)\b", re.I),
        "exclude": None,
    },
    "bucket": {
        "include": re.compile(r"\b(mop bucket|cleaning bucket|wringer bucket|utility bucket|collapsible bucket|bucket)\b", re.I),
        "exclude": re.compile(r"\b(ice bucket|champagne bucket|beer bucket|cooler bucket|toy bucket|storage bucket|feed bucket|bait bucket|diaper pail|paint bucket)\b", re.I),
    },
}

# Used only to prefilter batches vectorially; precise relevance is checked in Python.
BROAD_PATTERN = r"(?i)(mop|squeegee|cleaning brush|scrub brush|grout brush|tile brush|dish brush|floor scrub brush|bucket)"

FAILURE_PATTERNS = {
    "Rust": r"\b(rust|rusted|rusting|corrosion|corroded)\b",
    "Breakage": r"\b(broke|broken|breaks|snapped|snap|cracked|crack|fractured)\b",
    "Looseness": r"\b(loose|loosened|wobbl|wiggl|sloppy joint)\w*",
    "Jamming/Stiction": r"\b(jam|jammed|stuck|sticks|sticking|binds?|hard to (?:push|pull|turn|wring))\b",
    "Heaviness": r"\b(heavy|too heavy|heavier|weighty|tiring|fatigu)\w*",
    "Dirt Visibility": r"\b(shows dirt|looks dirty|shows dust|water spots?|fingerprints?)\b",
    "Scratch Visibility": r"\b(scratch|scratched|scuff|scuffed)\w*",
    "Colour Loss": r"\b(fad(?:e|ed|ing)|peel(?:ed|ing)?|color came off|colour came off|paint came off|chipp(?:ed|ing))\b",
    "Burr/Sharp Flash": r"\b(burr|sharp edge|sharp plastic|rough edge|flash)\b",
    "Soil Retention": r"\b(traps? (?:dirt|hair|grime)|hard to clean|difficult to clean|holds dirt|gets clogged|clogs?)\b",
    "Odour": r"\b(odor|odour|smell|stinks?|musty|mildew|moldy|mouldy)\b",
    "Colour Mismatch": r"\b(color mismatch|colour mismatch|wrong color|different color than|doesn't match the picture)\b",
    "Yellowing": r"\b(yellowed|yellowing|turned yellow)\b",
    "Hardening": r"\b(hardened|hardens|stiffened|gets? stiff|became stiff|dries? hard)\b",
    "Leakage": r"\b(leak|leaks|leaking|drips? from|water comes out)\b",
    "Instability/Tipping": r"\b(tip(?:s|ped|ping)? over|unstable|falls? over)\b",
    "Grip Slip/Discomfort": r"\b(slippery|slips? from|uncomfortable grip|hurts? my hand|blister)\b",
    "Bristle Shedding/Wear": r"\b(bristles? (?:fall|fell|coming) out|bristle loss|bristles? wore|bristles? bent)\b",
    "Wringer Failure": r"\b(wringer|wring|spin mechanism).{0,40}\b(broke|failed|stuck|stopped|doesn't work|not work)\b",
    "Poor Cleaning/Pickup": r"\b(doesn't clean|does not clean|poor pickup|won't pick up|leaves dirt|pushes dirt around)\b",
    "Streak/Watermark": r"\b(streak|streaks|water mark|watermark|water spots? left|leaves? water)\b",
    "Storage Bulk": r"\b(bulky|takes? up too much space|hard to store|doesn't fit|does not fit)\b",
    "Head Detachment": r"\b(head (?:falls|fell|comes|came) off|head detached|keeps? popping off)\b",
}

VALUE_PATTERNS = {
    "Lightness/Low Burden": r"\b(lightweight|light weight|very light|easy to carry|not heavy|less tiring|easy on my back)\b",
    "Clean Result": r"\b(cleans? (?:really )?well|gets? (?:the )?floor clean|picks? up (?:dirt|hair)|no streaks?|no water marks?)\b",
    "Soft Contact": r"\b(soft|gentle|doesn't scratch|does not scratch)\b",
    "Compact Storage": r"\b(compact|easy to store|hangs? up|wall mount|doesn't take much space|does not take much space)\b",
    "Simple Operation": r"\b(easy to use|simple to use|easy to assemble|easy assembly|easy to wring|hands? free|one hand)\b",
    "Reliability/Durability": r"\b(sturdy|solid|durable|well built|well-made|holds? up|lasting|strong handle)\b",
    "Hygiene/Easy Maintenance": r"\b(easy to clean|easy to rinse|rinses? clean|washable|dries? quickly|easy maintenance)\b",
    "Appearance": r"\b(looks? good|nice looking|beautiful|pretty|attractive|stylish|love the color|love the colour)\b",
    "Grip/Comfort": r"\b(comfortable|good grip|easy to hold|ergonomic|non-slip|nonslip)\b",
    "Reach/Coverage": r"\b(long handle|telescop|good reach|reaches? corners|wide head|covers? (?:a lot|more|large))\w*",
    "Water Handling/Wringing": r"\b(absorbent|absorbency|wrings? (?:out )?well|easy to wring|spin dry|less water|dries? the floor)\b",
    "Replaceability/Repairability": r"\b(replaceable|replacement head|easy to replace|refill|spare head)\b",
    "Value/Price": r"\b(good value|worth the money|worth it|good price|inexpensive|affordable)\b",
    "Fast/Immediate Use": r"\b(quick|fast|grab and go|ready to use|use it right away|convenient)\b",
}

CF = {k: re.compile(v, re.I | re.S) for k, v in FAILURE_PATTERNS.items()}
CV = {k: re.compile(v, re.I | re.S) for k, v in VALUE_PATTERNS.items()}


def norm(s) -> str:
    return re.sub(r"\s+", " ", "" if s is None else str(s)).strip()


def short_excerpt(s: str, max_words: int = 20) -> str:
    words = norm(s).split()
    return " ".join(words[:max_words]) + (" …" if len(words) > max_words else "")


def rating_band(rating) -> str:
    try:
        r = float(rating)
    except Exception:
        return "unknown"
    if r <= 2:
        return "1-2_failure_discovery"
    if r == 3:
        return "3_tradeoff"
    return "4-5_value_language"


def match_products(title: str, text: str):
    blob = f"{title} {text}"
    matched = []
    for product, rule in PRODUCT_RULES.items():
        if not rule["include"].search(blob):
            continue
        if rule["exclude"] and rule["exclude"].search(blob):
            continue
        # Bare bucket must still have cleaning context.
        if product == "bucket" and not re.search(r"\b(mop|clean|floor|wring|wash|scrub|squeegee)\w*\b", blob, re.I):
            continue
        matched.append(product)
    return matched


def auto_codes(title: str, text: str):
    blob = norm(f"{title}. {text}")
    failures = [k for k, rx in CF.items() if rx.search(blob)]
    values = [k for k, rx in CV.items() if rx.search(blob)]
    return failures, values


def pick_evenly(files, n):
    files = sorted(files)
    if len(files) <= n:
        return files
    if n == 1:
        return [files[len(files)//2]]
    idx = [round(i * (len(files)-1)/(n-1)) for i in range(n)]
    return [files[i] for i in sorted(set(idx))]


def select_balanced(records, per_product, seed):
    rnd = random.Random(seed)
    targets = {
        "1-2_failure_discovery": int(per_product * 0.45),
        "3_tradeoff": int(per_product * 0.20),
        "4-5_value_language": per_product - int(per_product * 0.45) - int(per_product * 0.20),
    }
    out = []
    by_band = defaultdict(list)
    for r in records:
        by_band[r["rating_band"]].append(r)
    for vals in by_band.values():
        rnd.shuffle(vals)
    leftovers = []
    for band, vals in by_band.items():
        n = min(targets.get(band, 0), len(vals))
        out.extend(vals[:n]); leftovers.extend(vals[n:])
    if len(out) < per_product:
        rnd.shuffle(leftovers)
        out.extend(leftovers[:per_product-len(out)])
    return out[:per_product]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="research/baojiajie/ar23_failure_value_corpus_v0_2")
    ap.add_argument("--shards-per-folder", type=int, default=4)
    ap.add_argument("--per-product", type=int, default=120)
    ap.add_argument("--batch-size", type=int, default=100_000)
    ap.add_argument("--max-candidates-per-product-per-shard", type=int, default=180)
    args = ap.parse_args()

    outdir = Path(args.out); outdir.mkdir(parents=True, exist_ok=True)
    api = HfApi()
    repo_files = api.list_repo_files(DATASET, repo_type="dataset")
    selected_shards = {}
    for folder in SOURCE_FOLDERS:
        files = [f for f in repo_files if f.startswith(folder + "/") and f.endswith(".parquet")]
        selected_shards[folder] = pick_evenly(files, args.shards_per_folder)
        if not selected_shards[folder]:
            raise RuntimeError(f"No parquet shards found for {folder}")

    candidates = defaultdict(list)
    seen = defaultdict(set)
    scan_log = []

    for folder, shards in selected_shards.items():
        for shard in shards:
            local = hf_hub_download(repo_id=DATASET, filename=shard, repo_type="dataset")
            pf = pq.ParquetFile(local)
            shard_counts = defaultdict(int)
            row_base = 0
            rows_scanned = 0
            broad_hits = 0
            for batch in pf.iter_batches(columns=["rating", "title", "text"], batch_size=args.batch_size):
                n = batch.num_rows
                rows_scanned += n
                title = pc.fill_null(batch.column("title"), "")
                text = pc.fill_null(batch.column("text"), "")
                blob = pc.binary_join_element_wise(title, text, " ")
                mask = pc.match_substring_regex(blob, BROAD_PATTERN)
                idxs = pc.indices_nonzero(mask).to_pylist()
                broad_hits += len(idxs)
                if idxs:
                    ratings = batch.column("rating").to_pylist()
                    titles = batch.column("title").to_pylist()
                    texts = batch.column("text").to_pylist()
                    for i in idxs:
                        t = norm(titles[i]); x = norm(texts[i])
                        products = match_products(t, x)
                        if not products:
                            continue
                        failures, values = auto_codes(t, x)
                        for product in products:
                            if shard_counts[product] >= args.max_candidates_per_product_per_shard:
                                continue
                            h = hashlib.sha1((t + "\n" + x).lower().encode("utf-8")).hexdigest()
                            if h in seen[product]:
                                continue
                            seen[product].add(h)
                            rec = {
                                "corpus_version": "v0.2",
                                "source_dataset": DATASET,
                                "source_folder": folder,
                                "source_shard": shard,
                                "row_in_shard": row_base + i,
                                "product": product,
                                "rating": ratings[i],
                                "rating_band": rating_band(ratings[i]),
                                "review_title": short_excerpt(t, 12),
                                "evidence_excerpt": short_excerpt(x, 20),
                                "review_sha1": h,
                                "failure_codes_auto": failures,
                                "value_codes_auto": values,
                                "evidence_status": "AUTO-CODED / MANUAL REVIEW REQUIRED",
                                "manual_review_required": True,
                                "sampling_status": "CATEGORY-SHARD DISCOVERY SAMPLE / NOT POPULATION-REPRESENTATIVE",
                            }
                            candidates[product].append(rec)
                            shard_counts[product] += 1
                row_base += n
            scan_log.append({
                "folder": folder,
                "shard": shard,
                "rows_scanned": rows_scanned,
                "broad_hits": broad_hits,
                "candidate_counts": dict(shard_counts),
            })

    selected = []
    for product in PRODUCT_RULES:
        selected.extend(select_balanced(candidates[product], args.per_product, 20260810 + len(product)))

    # Stable IDs after selection.
    selected = sorted(selected, key=lambda r: (r["product"], r["rating_band"], r["source_shard"], r["row_in_shard"]))
    seq = defaultdict(int)
    for r in selected:
        seq[r["product"]] += 1
        prefix = {"mop":"MOP", "cleaning_brush":"BR", "squeegee":"SQ", "bucket":"BU"}[r["product"]]
        r["evidence_id"] = f"AR23-{prefix}-{seq[r['product']]:03d}"

    jsonl = outdir / "external_failure_value_corpus_v0_2.jsonl"
    with jsonl.open("w", encoding="utf-8") as f:
        for r in selected:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")

    # Aggregated matrix is non-prevalence discovery output. Counts describe this selected corpus only.
    matrix = defaultdict(lambda: {"rows":0, "failure_codes":defaultdict(int), "value_codes":defaultdict(int)})
    for r in selected:
        key = (r["product"], r["rating_band"])
        matrix[key]["rows"] += 1
        for c in r["failure_codes_auto"]: matrix[key]["failure_codes"][c] += 1
        for c in r["value_codes_auto"]: matrix[key]["value_codes"][c] += 1
    matrix_rows = []
    for (product, band), d in sorted(matrix.items()):
        matrix_rows.append({
            "product": product,
            "rating_band": band,
            "selected_rows": d["rows"],
            "failure_codes_auto": dict(sorted(d["failure_codes"].items())),
            "value_codes_auto": dict(sorted(d["value_codes"].items())),
            "evidence_status": "AUTO-CODED / MANUAL REVIEW REQUIRED",
        })
    (outdir / "product_rating_failure_value_matrix_auto_v0_2.json").write_text(json.dumps(matrix_rows, ensure_ascii=False, indent=2), encoding="utf-8")

    summary = {
        "status": "CATEGORY-SHARD DISCOVERY SAMPLE / AUTO-CODED / MANUAL REVIEW REQUIRED",
        "source_dataset": DATASET,
        "folders": SOURCE_FOLDERS,
        "selected_shards": selected_shards,
        "rows_selected_total": len(selected),
        "rows_selected_by_product": {p: sum(r["product"] == p for r in selected) for p in PRODUCT_RULES},
        "rating_band_counts": {b: sum(r["rating_band"] == b for r in selected) for b in ["1-2_failure_discovery", "3_tradeoff", "4-5_value_language", "unknown"]},
        "critical_limitations": [
            "Evenly spaced category shards are a discovery sample, not a probability sample.",
            "Product identity is inferred from review title/text because the trimmed derivative omits parent_asin/product metadata.",
            "Automatic Failure/Value coding must be manually reviewed before evidence promotion.",
            "Counts describe only this selected discovery corpus and must not be compared as market prevalence against XJ01/JD samples.",
            "No exact hue or finish preference can be inferred from this corpus without controlled CMF stimuli.",
        ],
    }
    (outdir / "corpus_summary_v0_2.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    (outdir / "scan_log_v0_2.json").write_text(json.dumps(scan_log, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
