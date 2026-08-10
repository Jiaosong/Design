#!/usr/bin/env python3
"""Baojiajie External Failure + Value Corpus v0.3.

Uses thulthula/Amazon-Reviews-2023-Extended, a joined derivative containing
Amazon Reviews'23 review text plus product_title and parent_asin. Retrieval uses
the Hugging Face Dataset Viewer Search API, but relevance is accepted ONLY when
the PRODUCT TITLE matches a cleaning-tool rule. This fixes the v0.2 failure mode
where accessory/comparison mentions in review text were misclassified as the
reviewed product.

Evidence status: exploratory discovery corpus, not probability sample and not
prevalence estimation. Evidence excerpts are capped at 20 words. Automatic
Failure/Value codes require semantic review before promotion.
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

DATASET = "thulthula/Amazon-Reviews-2023-Extended"
SPLITS_API = "https://datasets-server.huggingface.co/splits"
SEARCH_API = "https://datasets-server.huggingface.co/search"

QUERY_MAP = {
    "mop": ["mop", "spin mop", "sponge mop", "flat mop", "spray mop", "microfiber mop", "floor mop"],
    "cleaning_brush": ["scrub brush", "cleaning brush", "grout brush", "bathroom brush", "dish brush", "floor scrub brush"],
    "squeegee": ["squeegee", "shower squeegee", "window squeegee", "floor squeegee"],
    "bucket": ["mop bucket", "cleaning bucket", "wringer bucket", "collapsible bucket"],
}

PRODUCT_TITLE_RULES = {
    "mop": re.compile(r"\b(mop|mopping)\b", re.I),
    "cleaning_brush": re.compile(r"\b(scrub(?:bing)? brush|cleaning brush|grout brush|bathroom brush|dish brush|floor scrub brush|scrubber brush|cleaning scrubber)\b", re.I),
    "squeegee": re.compile(r"\bsqueegee\b", re.I),
    "bucket": re.compile(r"\b(mop bucket|cleaning bucket|wringer bucket|collapsible bucket|bucket with wringer|spin mop.*bucket|bucket.*mop)\b", re.I),
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


def norm(s):
    return re.sub(r"\s+", " ", "" if s is None else str(s)).strip()


def excerpt(s, n=20):
    w = norm(s).split()
    return " ".join(w[:n]) + (" …" if len(w) > n else "")


def band(r):
    try: x = float(r)
    except Exception: return "unknown"
    if x <= 2: return "1-2_failure_discovery"
    if x == 3: return "3_tradeoff"
    return "4-5_value_language"


def codes(text):
    return [k for k, rx in CF.items() if rx.search(text)], [k for k, rx in CV.items() if rx.search(text)]


def get_split(session):
    r = session.get(SPLITS_API, params={"dataset": DATASET}, timeout=60)
    r.raise_for_status()
    js = r.json(); splits = js.get("splits") or []
    if not splits: raise RuntimeError(js)
    # Prefer train if present.
    s = next((x for x in splits if x.get("split") == "train"), splits[0])
    return s["config"], s["split"]


def search(session, config, split, query, max_hits):
    out=[]; offset=0; partial=False
    while len(out) < max_hits:
        length=min(100, max_hits-len(out))
        r=session.get(SEARCH_API, params={"dataset":DATASET,"config":config,"split":split,"query":query,"offset":offset,"length":length}, timeout=120)
        r.raise_for_status(); js=r.json()
        partial = partial or bool(js.get("partial", False))
        rows=js.get("rows") or []
        if not rows: break
        out.extend(rows); offset += len(rows)
        if len(rows) < length: break
        time.sleep(.1)
    return out, partial


def balanced(records, per_product, seed):
    rnd=random.Random(seed); b=defaultdict(list)
    for r in records: b[r["rating_band"]].append(r)
    for v in b.values(): rnd.shuffle(v)
    target={"1-2_failure_discovery":int(per_product*.45),"3_tradeoff":int(per_product*.20)}
    target["4-5_value_language"]=per_product-target["1-2_failure_discovery"]-target["3_tradeoff"]
    out=[]; rest=[]
    for k,v in b.items():
        n=min(target.get(k,0),len(v)); out += v[:n]; rest += v[n:]
    if len(out)<per_product:
        rnd.shuffle(rest); out += rest[:per_product-len(out)]
    return out[:per_product]


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--out", default="research/baojiajie/ar23_failure_value_corpus_v0_3")
    ap.add_argument("--hits-per-query", type=int, default=400)
    ap.add_argument("--per-product", type=int, default=120)
    ap.add_argument("--max-reviews-per-parent", type=int, default=6)
    args=ap.parse_args(); outdir=Path(args.out); outdir.mkdir(parents=True, exist_ok=True)
    sess=requests.Session(); sess.headers.update({"User-Agent":"Baojiajie-CMF-research/0.3"})
    config, split=get_split(sess)
    pool=defaultdict(list); seen=defaultdict(set); parent_count=defaultdict(lambda:defaultdict(int)); logs=[]

    for product, queries in QUERY_MAP.items():
        for q in queries:
            rows, partial=search(sess, config, split, q, args.hits_per_query)
            kept=0
            for item in rows:
                row=item.get("row") or {}
                ptitle=norm(row.get("product_title"))
                if not PRODUCT_TITLE_RULES[product].search(ptitle):
                    continue
                parent=norm(row.get("parent_asin"))
                rtext=norm(row.get("review_text"))
                if not rtext: continue
                h=hashlib.sha1((parent+"\n"+rtext).lower().encode()).hexdigest()
                if h in seen[product]: continue
                if parent and parent_count[product][parent] >= args.max_reviews_per_parent: continue
                seen[product].add(h); parent_count[product][parent]+=1
                fs,vs=codes(rtext)
                rec={
                    "corpus_version":"v0.3",
                    "source_dataset":DATASET,
                    "product":product,
                    "product_title":excerpt(ptitle,18),
                    "parent_asin":parent,
                    "asin":norm(row.get("asin")),
                    "rating":row.get("review_rating"),
                    "rating_band":band(row.get("review_rating")),
                    "verified_purchase":row.get("verified_purchase"),
                    "evidence_excerpt":excerpt(rtext,20),
                    "review_sha1":h,
                    "retrieval_query":q,
                    "failure_codes_auto":fs,
                    "value_codes_auto":vs,
                    "evidence_status":"PRODUCT-TITLE VERIFIED / AUTO-CODED / SEMANTIC REVIEW REQUIRED",
                    "semantic_review_required":True,
                    "sampling_status":"BM25 DISCOVERY SAMPLE / PRODUCT TITLE FILTERED / NOT POPULATION-REPRESENTATIVE",
                    "search_partial_flag":partial,
                }
                pool[product].append(rec); kept+=1
            logs.append({"product":product,"query":q,"rows_returned":len(rows),"product_title_verified_kept":kept,"partial":partial})

    selected=[]
    for p in QUERY_MAP: selected += balanced(pool[p], args.per_product, 20260810+len(p))
    selected=sorted(selected,key=lambda r:(r["product"],r["rating_band"],r["parent_asin"],r["review_sha1"]))
    seq=defaultdict(int)
    for r in selected:
        seq[r["product"]]+=1; pref={"mop":"MOP","cleaning_brush":"BR","squeegee":"SQ","bucket":"BU"}[r["product"]]
        r["evidence_id"]=f"AR23J-{pref}-{seq[r['product']]:03d}"

    with (outdir/"external_failure_value_corpus_v0_3.jsonl").open("w",encoding="utf-8") as f:
        for r in selected: f.write(json.dumps(r,ensure_ascii=False)+"\n")

    matrix=defaultdict(lambda:{"rows":0,"failure_codes":defaultdict(int),"value_codes":defaultdict(int),"parents":set()})
    for r in selected:
        d=matrix[(r["product"],r["rating_band"])]; d["rows"]+=1; d["parents"].add(r["parent_asin"])
        for c in r["failure_codes_auto"]: d["failure_codes"][c]+=1
        for c in r["value_codes_auto"]: d["value_codes"][c]+=1
    m=[]
    for (p,b),d in sorted(matrix.items()):
        m.append({"product":p,"rating_band":b,"selected_rows":d["rows"],"unique_parent_asin":len(d["parents"]),"failure_codes_auto":dict(sorted(d["failure_codes"].items())),"value_codes_auto":dict(sorted(d["value_codes"].items())),"evidence_status":"PRODUCT-TITLE VERIFIED / AUTO-CODED / SEMANTIC REVIEW REQUIRED"})
    (outdir/"product_rating_failure_value_matrix_auto_v0_3.json").write_text(json.dumps(m,ensure_ascii=False,indent=2),encoding="utf-8")
    summary={
        "status":"PRODUCT-TITLE VERIFIED / AUTO-CODED / SEMANTIC REVIEW REQUIRED",
        "source_dataset":DATASET,"config":config,"split":split,
        "rows_selected_total":len(selected),
        "rows_selected_by_product":{p:sum(r["product"]==p for r in selected) for p in QUERY_MAP},
        "unique_parent_asin_by_product":{p:len({r["parent_asin"] for r in selected if r["product"]==p}) for p in QUERY_MAP},
        "rating_band_counts":{b:sum(r["rating_band"]==b for r in selected) for b in ["1-2_failure_discovery","3_tradeoff","4-5_value_language","unknown"]},
        "partial_query_count":sum(bool(x["partial"]) for x in logs),
        "critical_limitations":[
            "BM25 retrieval is not a probability sample.",
            "Product relevance is verified from joined product_title, improving substantially on v0.2 text-only classification.",
            "Per-parent review caps reduce domination by a single product but do not make the sample representative.",
            "Automatic Failure/Value coding requires semantic review before evidence promotion.",
            "Counts describe the selected discovery corpus only and are not market prevalence.",
            "No exact hue/finish preference can be inferred without controlled CMF stimuli."
        ]}
    (outdir/"corpus_summary_v0_3.json").write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding="utf-8")
    (outdir/"acquisition_log_v0_3.json").write_text(json.dumps(logs,ensure_ascii=False,indent=2),encoding="utf-8")
    print(json.dumps(summary,ensure_ascii=False,indent=2))

if __name__=="__main__": main()
