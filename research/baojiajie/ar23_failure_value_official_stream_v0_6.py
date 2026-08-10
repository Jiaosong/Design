#!/usr/bin/env python3
"""Baojiajie Amazon Reviews'23 Failure + Value Corpus v0.6.

Primary acquisition path:
1. Stream OFFICIAL McAuley-Lab Amazon Reviews'23
   `raw_meta_Home_and_Kitchen` with datasets==2.21 + trust_remote_code.
2. Identify manual cleaning-tool products from official product titles and keep
   a deterministic reservoir of parent_asin candidates.
3. Retrieve review rows by exact parent_asin + rating-band predicates from the
   Parquet-backed `gmongaras/Amazon-Reviews-2023` derivative using HF /filter.
4. Write short evidence excerpts, not full reviews; automatic Failure/Value
   codes remain pending semantic review.

This is a discovery corpus, not probability sampling or prevalence estimation.
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
from datasets import load_dataset

OFFICIAL_DATASET = "McAuley-Lab/Amazon-Reviews-2023"
REVIEW_DATASET = "gmongaras/Amazon-Reviews-2023"
FILTER_API = "https://datasets-server.huggingface.co/filter"
SPLITS_API = "https://datasets-server.huggingface.co/splits"

RULES = {
    "mop": {
        "include": re.compile(r"\b(mop|mopping)\b", re.I),
        "exclude": re.compile(r"\b(robot|robotic|vacuum|steam|electric|cordless|powered|machine|replacement|refill|pad only|mop head only)\b", re.I),
    },
    "cleaning_brush": {
        "include": re.compile(r"\b(scrub(?:bing)? brush|cleaning brush|grout brush|bathroom brush|dish brush|floor scrub brush|scrubber brush)\b", re.I),
        "exclude": re.compile(r"\b(electric|power(?:ed)?|cordless|drill attachment|replacement head|toothbrush|hair brush|makeup brush|body brush)\b", re.I),
    },
    "squeegee": {
        "include": re.compile(r"\bsqueegee\b", re.I),
        "exclude": re.compile(r"\b(replacement blade|replacement rubber|refill)\b", re.I),
    },
    "bucket": {
        "include": re.compile(r"\b(mop bucket|cleaning bucket|wringer bucket|bucket with wringer|spin mop.*bucket|bucket.*mop|collapsible cleaning bucket)\b", re.I),
        "exclude": re.compile(r"\b(replacement|toy|ice bucket|champagne|paint bucket|storage bucket)\b", re.I),
    },
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


def norm(x): return re.sub(r"\s+", " ", "" if x is None else str(x)).strip()
def excerpt(x, n=20):
    w = norm(x).split(); return " ".join(w[:n]) + (" …" if len(w) > n else "")
def rating_band(x):
    try: r = float(x)
    except Exception: return "unknown"
    return "1-2_failure_discovery" if r <= 2 else "3_tradeoff" if r == 3 else "4-5_value_language"
def auto_codes(x): return [k for k, rx in CF.items() if rx.search(x)], [k for k, rx in CV.items() if rx.search(x)]


def classify_title(title):
    out=[]
    for product, rule in RULES.items():
        if rule["include"].search(title) and not rule["exclude"].search(title): out.append(product)
    return out


def reservoir_add(res, item, seen_n, cap, rnd):
    if len(res) < cap: res.append(item)
    else:
        j = rnd.randint(0, seen_n - 1)
        if j < cap: res[j] = item


def get_review_split(session):
    r = session.get(SPLITS_API, params={"dataset": REVIEW_DATASET}, timeout=60); r.raise_for_status()
    splits = r.json().get("splits") or []
    if not splits: raise RuntimeError("No review split")
    s = next((x for x in splits if x.get("split") == "train"), splits[0])
    return s["config"], s["split"]


def filter_reviews(session, config, split, parent_asin, band_name, length):
    p = parent_asin.replace("'", "''")
    if band_name == "1-2_failure_discovery": where = f'"parent_asin"=\'{p}\' AND "rating"<=2'
    elif band_name == "3_tradeoff": where = f'"parent_asin"=\'{p}\' AND "rating"=3'
    else: where = f'"parent_asin"=\'{p}\' AND "rating">=4'
    r = session.get(FILTER_API, params={"dataset": REVIEW_DATASET, "config": config, "split": split, "where": where, "offset": 0, "length": length}, timeout=90)
    r.raise_for_status(); return r.json().get("rows") or []


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="research/baojiajie/ar23_failure_value_corpus_v0_6")
    ap.add_argument("--max-meta-rows", type=int, default=0, help="0 scans the full metadata stream")
    ap.add_argument("--reservoir-per-product", type=int, default=45)
    ap.add_argument("--per-product", type=int, default=80)
    ap.add_argument("--per-parent-band", type=int, default=6)
    args = ap.parse_args(); outdir = Path(args.out); outdir.mkdir(parents=True, exist_ok=True)

    print("loading official raw_meta_Home_and_Kitchen stream")
    meta = load_dataset(OFFICIAL_DATASET, "raw_meta_Home_and_Kitchen", split="full", streaming=True, trust_remote_code=True)
    rnd = random.Random(20260810); reservoir = defaultdict(list); title_matches = defaultdict(int)
    scanned = 0
    for row in meta:
        scanned += 1
        title = norm(row.get("title")); products = classify_title(title)
        for product in products:
            title_matches[product] += 1
            item = {"product": product, "title": title, "parent_asin": norm(row.get("parent_asin")), "store": norm(row.get("store")), "rating_number": row.get("rating_number")}
            if item["parent_asin"]:
                reservoir_add(reservoir[product], item, title_matches[product], args.reservoir_per_product, rnd)
        if args.max_meta_rows and scanned >= args.max_meta_rows: break
        if scanned % 250000 == 0:
            print("meta_scanned", scanned, "matches", dict(title_matches), flush=True)
    print("meta_complete", scanned, dict(title_matches), {p: len(reservoir[p]) for p in RULES}, flush=True)

    session = requests.Session(); session.headers.update({"User-Agent": "Baojiajie-CMF-research/0.6"})
    config, split = get_review_split(session)
    targets = {"1-2_failure_discovery": int(args.per_product * .45), "3_tradeoff": int(args.per_product * .20)}
    targets["4-5_value_language"] = args.per_product - targets["1-2_failure_discovery"] - targets["3_tradeoff"]
    selected=[]; query_log=[]
    for product in RULES:
        per_band=defaultdict(list); seen=set(); parents=list(reservoir[product]); rnd.shuffle(parents)
        for meta_row in parents:
            if all(len(per_band[b]) >= targets[b] for b in targets): break
            for b in targets:
                if len(per_band[b]) >= targets[b]: continue
                try:
                    rows = filter_reviews(session, config, split, meta_row["parent_asin"], b, args.per_parent_band)
                except Exception as e:
                    query_log.append({"product":product,"parent_asin":meta_row["parent_asin"],"band":b,"error":repr(e)}); continue
                kept=0
                for item in rows:
                    row=item.get("row") or {}; text=norm(row.get("text"));
                    if not text: continue
                    h=hashlib.sha1((meta_row["parent_asin"] + "\n" + text).lower().encode()).hexdigest()
                    if h in seen: continue
                    seen.add(h); fs,vs=auto_codes(text)
                    per_band[b].append({
                        "corpus_version":"v0.6","source_meta_dataset":OFFICIAL_DATASET,"source_review_dataset":REVIEW_DATASET,
                        "product":product,"product_title":excerpt(meta_row["title"],18),"parent_asin":meta_row["parent_asin"],"asin":norm(row.get("asin")),
                        "rating":row.get("rating"),"rating_band":rating_band(row.get("rating")),"verified_purchase":row.get("verified_purchase"),"helpful_vote":row.get("helpful_vote"),
                        "evidence_excerpt":excerpt(text,20),"review_sha1":h,"failure_codes_auto":fs,"value_codes_auto":vs,
                        "evidence_status":"OFFICIAL PRODUCT METADATA LINKED BY PARENT_ASIN / AUTO-CODED / SEMANTIC REVIEW REQUIRED",
                        "semantic_review_required":True,"sampling_status":"OFFICIAL METADATA RESERVOIR + EXACT PARENT_ASIN FILTER DISCOVERY SAMPLE / NOT POPULATION-REPRESENTATIVE"
                    }); kept += 1
                    if len(per_band[b]) >= targets[b]: break
                query_log.append({"product":product,"parent_asin":meta_row["parent_asin"],"band":b,"rows_returned":len(rows),"kept":kept})
                time.sleep(.05)
        for b in targets: selected.extend(per_band[b][:targets[b]])

    selected = sorted(selected, key=lambda r:(r["product"],r["rating_band"],r["parent_asin"],r["review_sha1"]))
    seq=defaultdict(int); pref={"mop":"MOP","cleaning_brush":"BR","squeegee":"SQ","bucket":"BU"}
    for r in selected: seq[r["product"]]+=1; r["evidence_id"] = f"AR23-{pref[r['product']]}-{seq[r['product']]:03d}"
    with (outdir/"external_failure_value_corpus_v0_6.jsonl").open("w", encoding="utf-8") as f:
        for r in selected: f.write(json.dumps(r, ensure_ascii=False) + "\n")

    matrix=defaultdict(lambda:{"rows":0,"parents":set(),"failure":defaultdict(int),"value":defaultdict(int)})
    for r in selected:
        d=matrix[(r["product"],r["rating_band"])]; d["rows"]+=1; d["parents"].add(r["parent_asin"])
        for c in r["failure_codes_auto"]: d["failure"][c]+=1
        for c in r["value_codes_auto"]: d["value"][c]+=1
    matrix_rows=[]
    for (p,b),d in sorted(matrix.items()):
        matrix_rows.append({"product":p,"rating_band":b,"selected_rows":d["rows"],"unique_parent_asin":len(d["parents"]),"failure_codes_auto":dict(sorted(d["failure"].items())),"value_codes_auto":dict(sorted(d["value"].items())),"evidence_status":"AUTO-CODED / SEMANTIC REVIEW REQUIRED"})
    (outdir/"product_rating_failure_value_matrix_auto_v0_6.json").write_text(json.dumps(matrix_rows,ensure_ascii=False,indent=2),encoding="utf-8")
    summary={
        "status":"OFFICIAL PRODUCT METADATA LINKED / REAL REVIEW ROWS / AUTO-CODED / SEMANTIC REVIEW REQUIRED",
        "official_metadata_rows_scanned":scanned,"metadata_title_matches":dict(title_matches),"product_reservoir_size":{p:len(reservoir[p]) for p in RULES},
        "rows_selected_total":len(selected),"rows_selected_by_product":{p:sum(r["product"]==p for r in selected) for p in RULES},
        "unique_parent_asin_by_product":{p:len({r["parent_asin"] for r in selected if r["product"]==p}) for p in RULES},
        "rating_band_counts":{b:sum(r["rating_band"]==b for r in selected) for b in ["1-2_failure_discovery","3_tradeoff","4-5_value_language","unknown"]},
        "review_filter_config":config,"review_filter_split":split,
        "critical_limitations":["Discovery sampling is not probability sampling.","Product identity is established from official Amazon Reviews'23 Home_and_Kitchen metadata and linked by parent_asin.","Review rows come from a Parquet-backed copy of Amazon Reviews'23 and are linked by exact parent_asin.","Automatic Failure/Value coding requires semantic review before evidence promotion.","Rating quotas are research-design quotas, not prevalence.","No exact hue/finish preference can be inferred without controlled CMF stimuli."]}
    (outdir/"corpus_summary_v0_6.json").write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding="utf-8")
    (outdir/"metadata_reservoir_v0_6.json").write_text(json.dumps(dict(reservoir),ensure_ascii=False,indent=2),encoding="utf-8")
    (outdir/"review_query_log_v0_6.json").write_text(json.dumps(query_log,ensure_ascii=False,indent=2),encoding="utf-8")
    print(json.dumps(summary,ensure_ascii=False,indent=2))

if __name__ == "__main__": main()
