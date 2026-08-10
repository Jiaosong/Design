#!/usr/bin/env python3
"""Baojiajie External Failure + Value Corpus v0.1.

Exploratory acquisition from an Amazon Reviews'23 derivative through the
Hugging Face Dataset Viewer Search API.

IMPORTANT: output is exploratory review-language evidence, not a probability
sample and not population prevalence. Automatic coding requires manual review.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import random
import re
import time
from collections import defaultdict
from pathlib import Path

import requests

DATASET = "bagadbilla/amazon-reviews-2023-trimmed"
SPLITS_API = "https://datasets-server.huggingface.co/splits"
SEARCH_API = "https://datasets-server.huggingface.co/search"

QUERY_MAP = {
    "mop": ["mop", "spin mop", "sponge mop", "flat mop", "spray mop", "microfiber mop", "floor mop", "dust mop"],
    "cleaning_brush": ["cleaning brush", "scrub brush", "bathroom brush", "grout brush", "tile brush", "dish brush", "floor scrub brush"],
    "squeegee": ["squeegee", "shower squeegee", "window squeegee", "floor squeegee"],
    "bucket": ["mop bucket", "cleaning bucket", "wringer bucket", "utility bucket", "collapsible bucket"],
}

EXCLUDE = {
    "cleaning_brush": re.compile(r"\b(hair ?brush|tooth ?brush|makeup brush|nail brush|body brush|shaving brush|eyelash|mascara|scalp brush)\b", re.I),
    "bucket": re.compile(r"\b(ice bucket|champagne bucket|beer bucket|cooler bucket|toy bucket|storage bucket|feed bucket|bait bucket)\b", re.I),
}

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


def norm(s: str) -> str:
    return re.sub(r"\s+", " ", (s or "")).strip()


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


def relevant(category: str, title: str, text: str) -> bool:
    blob = f"{title} {text}".lower()
    if category == "mop":
        ok = bool(re.search(r"\bmop(?:s|ping)?\b", blob))
    elif category == "cleaning_brush":
        ok = bool(re.search(r"\b(cleaning brush|scrub brush|bathroom brush|grout brush|tile brush|dish brush|floor scrub brush)\b", blob))
    elif category == "squeegee":
        ok = "squeegee" in blob
    elif category == "bucket":
        ok = bool(re.search(r"\b(mop bucket|cleaning bucket|wringer bucket|utility bucket|collapsible bucket)\b", blob))
        if not ok and "bucket" in blob:
            ok = bool(re.search(r"\b(mop|clean|floor|wring|wash|scrub)\w*\b", blob))
    else:
        ok = False
    ex = EXCLUDE.get(category)
    return ok and not (ex and ex.search(blob))


def code_text(title: str, text: str):
    blob = norm(f"{title}. {text}")
    return [k for k, rx in CF.items() if rx.search(blob)], [k for k, rx in CV.items() if rx.search(blob)]


def stable_hash(title, text):
    return hashlib.sha1(norm(title + "\n" + text).lower().encode()).hexdigest()


def get_config(session):
    r = session.get(SPLITS_API, params={"dataset": DATASET}, timeout=60)
    r.raise_for_status()
    data = r.json()
    splits = data.get("splits") or []
    if not splits:
        raise RuntimeError(f"No split returned: {data}")
    return splits[0]["config"], splits[0]["split"]


def fetch_query(session, config, split, query, max_hits):
    rows, partial_flags, offset = [], [], 0
    while len(rows) < max_hits:
        length = min(100, max_hits - len(rows))
        r = session.get(SEARCH_API, params={
            "dataset": DATASET, "config": config, "split": split,
            "query": query, "offset": offset, "length": length,
        }, timeout=120)
        r.raise_for_status()
        data = r.json()
        batch = data.get("rows") or []
        partial_flags.append(bool(data.get("partial", False)))
        if not batch:
            break
        rows.extend(batch)
        offset += len(batch)
        if len(batch) < length:
            break
        time.sleep(0.15)
    return rows, any(partial_flags)


def choose_quota(records, per_category, seed):
    rnd = random.Random(seed)
    bands = defaultdict(list)
    for rec in records:
        bands[rec["rating_band"]].append(rec)
    for vals in bands.values():
        rnd.shuffle(vals)
    targets = {
        "1-2_failure_discovery": int(per_category * 0.45),
        "3_tradeoff": int(per_category * 0.20),
        "4-5_value_language": per_category - int(per_category * 0.45) - int(per_category * 0.20),
    }
    out, unused = [], []
    for band, vals in bands.items():
        n = min(targets.get(band, 0), len(vals))
        out.extend(vals[:n]); unused.extend(vals[n:])
    if len(out) < per_category:
        rnd.shuffle(unused); out.extend(unused[:per_category-len(out)])
    return out[:per_category]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="ar23_failure_value_corpus_v0_1")
    ap.add_argument("--hits-per-query", type=int, default=100)
    ap.add_argument("--per-category", type=int, default=120)
    args = ap.parse_args()
    outdir = Path(args.out); outdir.mkdir(parents=True, exist_ok=True)
    session = requests.Session(); session.headers.update({"User-Agent": "Baojiajie-CMF-research/0.1"})
    config, split = get_config(session)
    all_records, seen = defaultdict(list), set()
    acquisition = {"dataset": DATASET, "config": config, "split": split, "population_inference_allowed": False, "queries": []}

    for product_category, queries in QUERY_MAP.items():
        for query in queries:
            rows, partial = fetch_query(session, config, split, query, args.hits_per_query)
            kept = 0
            for item in rows:
                row = item.get("row") or {}
                title, text = norm(row.get("title", "")), norm(row.get("text", ""))
                if not relevant(product_category, title, text):
                    continue
                h = stable_hash(title, text)
                if h in seen:
                    continue
                seen.add(h)
                failures, values = code_text(title, text)
                all_records[product_category].append({
                    "corpus_version": "v0.1",
                    "source": "Amazon Reviews'23 derivative: bagadbilla/amazon-reviews-2023-trimmed",
                    "evidence_type": "External Direct Review Text / Derivative Dataset",
                    "product_category": product_category,
                    "search_query": query,
                    "row_idx": item.get("row_idx"),
                    "rating": row.get("rating"),
                    "rating_band": rating_band(row.get("rating")),
                    "title": title,
                    "text": text,
                    "failure_codes_auto": failures,
                    "value_codes_auto": values,
                    "evidence_status": "AUTO-CODED / MANUAL REVIEW REQUIRED",
                    "manual_review_required": True,
                    "dedupe_hash": h,
                    "search_partial_flag": partial,
                }); kept += 1
            acquisition["queries"].append({"product_category": product_category, "query": query, "rows_returned": len(rows), "rows_kept_after_relevance_dedupe": kept, "partial": partial})

    selected = []
    for cat, recs in all_records.items():
        selected.extend(choose_quota(recs, args.per_category, 20260810 + len(cat)))

    with (outdir / "external_failure_value_corpus_v0_1.jsonl").open("w", encoding="utf-8") as f:
        for rec in selected:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")

    summary = {
        "status": "EXPLORATORY / NOT POPULATION-REPRESENTATIVE / MANUAL CODING REQUIRED",
        "selected_total": len(selected),
        "selected_by_product_category": {c: sum(r["product_category"] == c for r in selected) for c in QUERY_MAP},
        "rating_band_counts": {b: sum(r["rating_band"] == b for r in selected) for b in ["1-2_failure_discovery", "3_tradeoff", "4-5_value_language", "unknown"]},
        "failure_auto_counts": {code: sum(code in r["failure_codes_auto"] for r in selected) for code in FAILURE_PATTERNS},
        "value_auto_counts": {code: sum(code in r["value_codes_auto"] for r in selected) for code in VALUE_PATTERNS},
        "partial_query_count": sum(q["partial"] for q in acquisition["queries"]),
        "critical_limitation": "BM25-retrieved language corpus; product identity inferred from text; do not estimate prevalence or compare raw frequencies to XJ01/JD.",
    }
    (outdir / "corpus_summary_v0_1.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    (outdir / "acquisition_log_v0_1.json").write_text(json.dumps(acquisition, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
