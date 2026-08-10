#!/usr/bin/env python3
"""Baojiajie External Failure + Value Corpus v0.7.

Primary evidence path using only official McAuley-Lab Amazon Reviews'23
Home_and_Kitchen Parquet files.

Procedure
---------
1. Scan a deterministic spread of official metadata shards and identify manual
   mop / household cleaning brush / squeegee / cleaning-bucket parent_asins from
   PRODUCT TITLES.
2. Scan official Home_and_Kitchen review shards sequentially. Match only exact
   parent_asin values selected from metadata.
3. Build rating-band discovery quotas (1-2★ failure, 3★ trade-off, 4-5★ value)
   with a per-parent cap.
4. Store short evidence excerpts (<=20 words), not full review text.
5. Auto-code Failure/Value vocabulary only as a first-pass retrieval aid.

Evidence boundary
-----------------
This is a reproducible discovery sample, NOT probability sampling, market
prevalence, failure-rate estimation, or CMF preference evidence. Automatic
codes require semantic review before promotion into the project evidence base.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import random
import re
from collections import defaultdict
from pathlib import Path

import pyarrow as pa
import pyarrow.compute as pc
import pyarrow.parquet as pq
from huggingface_hub import hf_hub_download

DATASET = "McAuley-Lab/Amazon-Reviews-2023"
META_TOTAL = 21
REVIEW_TOTAL = 45

RULES = {
    "mop": {
        "include": re.compile(r"\b(mop|mopping)\b", re.I),
        "exclude": re.compile(r"\b(robot|robotic|vacuum|steam|electric|cordless|powered|machine|replacement|refill|reusable pad|mop pad|mop head|replacement head)\b", re.I),
    },
    "cleaning_brush": {
        "include": re.compile(r"\b(scrub(?:bing)? brush|cleaning brush|grout brush|bathroom brush|tile brush|floor scrub brush|toilet brush|dish scrub brush|scrubber brush)\b", re.I),
        "exclude": re.compile(r"\b(electric|power(?:ed)?|cordless|drill attachment|replacement head|toothbrush|hair brush|makeup brush|body brush|bottle brush|vegetable brush|grill brush|shoe brush|paint brush)\b", re.I),
    },
    "squeegee": {
        "include": re.compile(r"\bsqueegee\b", re.I),
        "exclude": re.compile(r"\b(replacement blade|replacement rubber|refill|screen printing|printing ink)\b", re.I),
    },
    "bucket": {
        "include": re.compile(r"\b(mop bucket|cleaning bucket|wringer bucket|bucket with wringer|spin mop.*bucket|bucket.*mop|collapsible cleaning bucket|utility cleaning bucket)\b", re.I),
        "exclude": re.compile(r"\b(replacement|toy|ice bucket|champagne|paint bucket|storage bucket|feed bucket|bait bucket)\b", re.I),
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
    "Colour Mismatch": r"\b(color mismatch|colour mismatch|wrong color|different color than|doesn't match the picture|different than pictured)\b",
    "Yellowing": r"\b(yellowed|yellowing|turned yellow)\b",
    "Hardening": r"\b(hardened|hardens|stiffened|gets? stiff|became stiff|dries? hard)\b",
    "Leakage": r"\b(leak|leaks|leaking|drips? from|water comes out)\b",
    "Instability/Tipping": r"\b(tip(?:s|ped|ping)? over|unstable|falls? over|keels? over)\b",
    "Grip Slip/Discomfort": r"\b(slippery|slips? from|uncomfortable grip|hurts? my hand|blister)\b",
    "Bristle Shedding/Wear": r"\b(bristles? (?:fall|fell|coming) out|bristle loss|bristles? wore|bristles? bent|bristles? flattened)\b",
    "Wringer Failure": r"\b(wringer|wring|spin mechanism).{0,50}\b(broke|failed|stuck|stopped|doesn't work|not work)\b",
    "Poor Cleaning/Pickup": r"\b(doesn't clean|does not clean|poor pickup|won't pick up|leaves dirt|pushes dirt around|doesn't pick up)\b",
    "Streak/Watermark": r"\b(streak|streaks|water mark|watermark|water spots? left|leaves? water)\b",
    "Storage Bulk": r"\b(bulky|takes? up too much space|hard to store|doesn't fit|does not fit)\b",
    "Head Detachment": r"\b(head (?:falls|fell|comes|came) off|head detached|keeps? popping off|mop head.*off)\b",
}

VALUE_PATTERNS = {
    "Lightness/Low Burden": r"\b(lightweight|light weight|very light|easy to carry|not heavy|less tiring|easy on my back|easy on the back)\b",
    "Clean Result": r"\b(cleans? (?:really )?well|gets? (?:the )?floor clean|picks? up (?:dirt|hair)|no streaks?|no water marks?|leaves? (?:the )?floor clean)\b",
    "Soft Contact": r"\b(soft|gentle|doesn't scratch|does not scratch)\b",
    "Compact Storage": r"\b(compact|easy to store|hangs? up|wall mount|doesn't take much space|does not take much space)\b",
    "Simple Operation": r"\b(easy to use|simple to use|easy to assemble|easy assembly|easy to wring|hands? free|one hand|simple operation)\b",
    "Reliability/Durability": r"\b(sturdy|solid|durable|well built|well-built|well made|well-made|holds? up|lasting|strong handle)\b",
    "Hygiene/Easy Maintenance": r"\b(easy to clean|easy to rinse|rinses? clean|washable|dries? quickly|easy maintenance)\b",
    "Appearance": r"\b(looks? good|nice looking|beautiful|pretty|attractive|stylish|love the color|love the colour|nice color|nice colour)\b",
    "Grip/Comfort": r"\b(comfortable|good grip|easy to hold|ergonomic|non-slip|nonslip)\b",
    "Reach/Coverage": r"\b(long handle|telescop|good reach|reaches? corners|wide head|covers? (?:a lot|more|large))\w*",
    "Water Handling/Wringing": r"\b(absorbent|absorbency|wrings? (?:out )?well|easy to wring|spin dry|less water|dries? the floor)\b",
    "Replaceability/Repairability": r"\b(replaceable|replacement head|easy to replace|refill|spare head)\b",
    "Value/Price": r"\b(good value|worth the money|worth it|good price|inexpensive|affordable)\b",
    "Fast/Immediate Use": r"\b(quick|fast|grab and go|ready to use|use it right away|convenient)\b",
}
CF={k:re.compile(v,re.I|re.S) for k,v in FAILURE_PATTERNS.items()}
CV={k:re.compile(v,re.I|re.S) for k,v in VALUE_PATTERNS.items()}


def norm(x): return re.sub(r"\s+"," ","" if x is None else str(x)).strip()
def excerpt(x,n=20):
    w=norm(x).split(); return " ".join(w[:n])+(" …" if len(w)>n else "")
def band(x):
    try:r=float(x)
    except:return "unknown"
    return "1-2_failure_discovery" if r<=2 else "3_tradeoff" if r==3 else "4-5_value_language"
def codes(x): return [k for k,r in CF.items() if r.search(x)],[k for k,r in CV.items() if r.search(x)]
def classify_title(t):
    return [p for p,r in RULES.items() if r["include"].search(t) and not r["exclude"].search(t)]

def pick_spread(total,n):
    if n>=total:return list(range(total))
    if n<=1:return [total//2]
    return sorted(set(round(i*(total-1)/(n-1)) for i in range(n)))

def reservoir_add(res,item,seen,cap,rnd):
    if len(res)<cap:res.append(item)
    else:
        j=rnd.randint(0,seen-1)
        if j<cap:res[j]=item

def targets(n):
    lo=int(n*.45); mid=int(n*.20); hi=n-lo-mid
    return {"1-2_failure_discovery":lo,"3_tradeoff":mid,"4-5_value_language":hi}


def dl(path):
    return hf_hub_download(repo_id=DATASET,filename=path,repo_type="dataset")


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--out",default="research/baojiajie/ar23_failure_value_corpus_v0_7")
    ap.add_argument("--meta-shards",type=int,default=7)
    ap.add_argument("--reservoir-per-product",type=int,default=60)
    ap.add_argument("--per-product",type=int,default=60)
    ap.add_argument("--max-reviews-per-parent",type=int,default=5)
    ap.add_argument("--batch-size",type=int,default=100000)
    args=ap.parse_args();outdir=Path(args.out);outdir.mkdir(parents=True,exist_ok=True)
    rnd=random.Random(20260810);res=defaultdict(list);seen_titles=defaultdict(int);meta_log=[]

    meta_idxs=pick_spread(META_TOTAL,args.meta_shards)
    for idx in meta_idxs:
        path=f"raw_meta_Home_and_Kitchen/full-{idx:05d}-of-{META_TOTAL:05d}.parquet"
        local=dl(path);pf=pq.ParquetFile(local);matched=defaultdict(int);rows=0
        cols=[c for c in ["title","parent_asin","rating_number","store"] if c in pf.schema.names]
        for bt in pf.iter_batches(columns=cols,batch_size=args.batch_size):
            d=bt.to_pydict();rows+=bt.num_rows
            for i,raw in enumerate(d.get("title",[])):
                title=norm(raw);ps=classify_title(title)
                for p in ps:
                    parent=norm(d.get("parent_asin",[None]*bt.num_rows)[i])
                    if not parent:continue
                    seen_titles[p]+=1;matched[p]+=1
                    item={"product":p,"product_title":title,"parent_asin":parent,"store":norm(d.get("store",[None]*bt.num_rows)[i]),"rating_number":d.get("rating_number",[None]*bt.num_rows)[i],"meta_shard":path}
                    reservoir_add(res[p],item,seen_titles[p],args.reservoir_per_product,rnd)
        meta_log.append({"shard":path,"rows_scanned":rows,"matches":dict(matched)})
        print("meta",idx,"rows",rows,"matches",dict(matched),"reservoir",{p:len(res[p]) for p in RULES},flush=True)

    parent_to_meta={}
    parent_to_product=defaultdict(set)
    for p,items in res.items():
        for x in items:
            parent_to_meta[x["parent_asin"]]=x;parent_to_product[x["parent_asin"]].add(p)
    parent_values=pa.array(list(parent_to_meta.keys()),type=pa.string())
    if len(parent_values)==0:raise RuntimeError("No candidate parent_asins from metadata")

    t=targets(args.per_product);pool=defaultdict(lambda:defaultdict(list));per_parent_count=defaultdict(int);review_log=[]
    def complete(): return all(len(pool[p][b])>=t[b] for p in RULES for b in t)

    for idx in range(REVIEW_TOTAL):
        if complete():break
        path=f"raw_review_Home_and_Kitchen/full-{idx:05d}-of-{REVIEW_TOTAL:05d}.parquet"
        local=dl(path);pf=pq.ParquetFile(local);rows=0;matched=0;accepted=defaultdict(int)
        names=set(pf.schema.names);cols=[c for c in ["rating","title","text","asin","parent_asin","verified_purchase","helpful_vote"] if c in names]
        if "parent_asin" not in names or "text" not in names or "rating" not in names:raise RuntimeError(f"unexpected review schema {sorted(names)}")
        for bt in pf.iter_batches(columns=cols,batch_size=args.batch_size):
            rows+=bt.num_rows;parents=pc.fill_null(bt.column("parent_asin"),"")
            mask=pc.is_in(parents,value_set=parent_values);idxs=pc.indices_nonzero(mask).to_pylist()
            if not idxs:continue
            d=bt.to_pydict();matched+=len(idxs)
            for i in idxs:
                parent=norm(d["parent_asin"][i]);rband=band(d["rating"][i]);
                if rband not in t:continue
                for product in parent_to_product[parent]:
                    if len(pool[product][rband])>=t[rband]:continue
                    key=(product,parent)
                    if per_parent_count[key]>=args.max_reviews_per_parent:continue
                    text=norm(d["text"][i]);
                    if not text:continue
                    h=hashlib.sha1((parent+"\n"+text).lower().encode()).hexdigest()
                    if any(x["review_sha1"]==h for x in pool[product][rband]):continue
                    fs,vs=codes(text);meta=parent_to_meta[parent]
                    pool[product][rband].append({"corpus_version":"v0.7","source_dataset":DATASET,"product":product,
                        "product_title":excerpt(meta["product_title"],18),"parent_asin":parent,"asin":norm(d.get("asin",[None]*bt.num_rows)[i]),
                        "rating":d["rating"][i],"rating_band":rband,"verified_purchase":d.get("verified_purchase",[None]*bt.num_rows)[i],"helpful_vote":d.get("helpful_vote",[None]*bt.num_rows)[i],
                        "review_title":excerpt(d.get("title",[None]*bt.num_rows)[i],12),"evidence_excerpt":excerpt(text,20),"review_sha1":h,
                        "failure_codes_auto":fs,"value_codes_auto":vs,"evidence_status":"OFFICIAL METADATA+REVIEW / AUTO-CODED / SEMANTIC REVIEW REQUIRED",
                        "semantic_review_required":True,"sampling_status":"OFFICIAL HOME_AND_KITCHEN SHARD DISCOVERY SAMPLE / NOT POPULATION-REPRESENTATIVE","review_shard":path})
                    per_parent_count[key]+=1;accepted[product]+=1
        review_log.append({"shard":path,"rows_scanned":rows,"candidate_parent_hits":matched,"accepted":dict(accepted),"current_counts":{p:{b:len(pool[p][b]) for b in t} for p in RULES}})
        print("review",idx,"parent_hits",matched,"accepted",dict(accepted),"current",{p:{b:len(pool[p][b]) for b in t} for p in RULES},flush=True)
        # free cached local file where possible; HF cache may retain blobs, but runner disk is monitored externally

    selected=[]
    for p in RULES:
        for b in t:selected.extend(pool[p][b][:t[b]])
    selected=sorted(selected,key=lambda r:(r["product"],r["rating_band"],r["parent_asin"],r["review_sha1"]))
    seq=defaultdict(int);pref={"mop":"MOP","cleaning_brush":"BR","squeegee":"SQ","bucket":"BU"}
    for r in selected:seq[r["product"]]+=1;r["evidence_id"]=f"AR23O-{pref[r['product']]}-{seq[r['product']]:03d}"
    with (outdir/"external_failure_value_corpus_v0_7.jsonl").open("w",encoding="utf-8") as f:
        for r in selected:f.write(json.dumps(r,ensure_ascii=False)+"\n")

    matrix=defaultdict(lambda:{"rows":0,"parents":set(),"failure":defaultdict(int),"value":defaultdict(int)})
    for r in selected:
        d=matrix[(r["product"],r["rating_band"])];d["rows"]+=1;d["parents"].add(r["parent_asin"])
        for c in r["failure_codes_auto"]:d["failure"][c]+=1
        for c in r["value_codes_auto"]:d["value"][c]+=1
    matrix_rows=[]
    for (p,b),d in sorted(matrix.items()):matrix_rows.append({"product":p,"rating_band":b,"selected_rows":d["rows"],"unique_parent_asin":len(d["parents"]),"failure_codes_auto":dict(sorted(d["failure"].items())),"value_codes_auto":dict(sorted(d["value"].items())),"evidence_status":"OFFICIAL ROWS / AUTO-CODED / SEMANTIC REVIEW REQUIRED"})
    (outdir/"product_rating_failure_value_matrix_auto_v0_7.json").write_text(json.dumps(matrix_rows,ensure_ascii=False,indent=2),encoding="utf-8")
    summary={"status":"OFFICIAL HOME_AND_KITCHEN ROWS / AUTO-CODED / SEMANTIC REVIEW REQUIRED","source_dataset":DATASET,
        "metadata_shards_scanned":meta_idxs,"metadata_title_matches":dict(seen_titles),"candidate_parent_asins_by_product":{p:len(res[p]) for p in RULES},
        "review_shards_scanned":len(review_log),"rows_selected_total":len(selected),"target_per_product":args.per_product,
        "rows_selected_by_product":{p:sum(r["product"]==p for r in selected) for p in RULES},"unique_parent_asin_by_product":{p:len({r["parent_asin"] for r in selected if r["product"]==p}) for p in RULES},
        "rating_band_counts":{b:sum(r["rating_band"]==b for r in selected) for b in ["1-2_failure_discovery","3_tradeoff","4-5_value_language","unknown"]},
        "critical_limitations":["Deterministically spread metadata shards plus exact-parent review scanning form a discovery sample, not probability sampling.","Product identity is based on official Home_and_Kitchen product-title metadata and exact parent_asin linkage.","Automatic Failure/Value coding requires semantic review before evidence promotion.","Per-product and rating-band quotas are research-design quotas, not prevalence.","No exact hue/finish preference can be inferred without controlled CMF stimuli."]}
    (outdir/"corpus_summary_v0_7.json").write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding="utf-8")
    (outdir/"metadata_scan_log_v0_7.json").write_text(json.dumps(meta_log,ensure_ascii=False,indent=2),encoding="utf-8")
    (outdir/"review_scan_log_v0_7.json").write_text(json.dumps(review_log,ensure_ascii=False,indent=2),encoding="utf-8")
    (outdir/"candidate_products_v0_7.json").write_text(json.dumps(dict(res),ensure_ascii=False,indent=2),encoding="utf-8")
    print(json.dumps(summary,ensure_ascii=False,indent=2))

if __name__=="__main__":main()
