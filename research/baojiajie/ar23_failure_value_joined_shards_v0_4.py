#!/usr/bin/env python3
"""Baojiajie AR23 joined-Parquet corpus v0.4.

Directly scans evenly spaced Parquet shards from
thulthula/Amazon-Reviews-2023-Extended. Unlike v0.2, this joined dataset includes
product_title and parent_asin, so product relevance is determined from product
metadata rather than incidental words in review text.

This remains a discovery sample, not a probability sample. Evidence excerpts
are capped at 20 words; automatic Failure/Value coding requires semantic review.
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

DATASET = "thulthula/Amazon-Reviews-2023-Extended"

PRODUCT_TITLE_RULES = {
    "mop": re.compile(r"\b(mop|mopping)\b", re.I),
    "cleaning_brush": re.compile(r"\b(scrub(?:bing)? brush|cleaning brush|grout brush|bathroom brush|dish brush|floor scrub brush|scrubber brush|cleaning scrubber)\b", re.I),
    "squeegee": re.compile(r"\bsqueegee\b", re.I),
    "bucket": re.compile(r"\b(mop bucket|cleaning bucket|wringer bucket|collapsible bucket|bucket with wringer|spin mop.*bucket|bucket.*mop)\b", re.I),
}
BROAD_TITLE_PATTERN = r"(?i)(mop|mopping|squeegee|scrub brush|scrubbing brush|cleaning brush|grout brush|bathroom brush|dish brush|floor scrub brush|scrubber brush|mop bucket|wringer bucket|collapsible bucket)"

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

def pick_evenly(files,n):
    files=sorted(files)
    if len(files)<=n:return files
    idx=[round(i*(len(files)-1)/(n-1)) for i in range(n)] if n>1 else [len(files)//2]
    return [files[i] for i in sorted(set(idx))]

def match_product(title):
    out=[]
    for p,rx in PRODUCT_TITLE_RULES.items():
        if rx.search(title): out.append(p)
    return out

def balanced(records,n,seed):
    rnd=random.Random(seed); b=defaultdict(list)
    for r in records:b[r["rating_band"]].append(r)
    for v in b.values():rnd.shuffle(v)
    target={"1-2_failure_discovery":int(n*.45),"3_tradeoff":int(n*.20)}
    target["4-5_value_language"]=n-target["1-2_failure_discovery"]-target["3_tradeoff"]
    out=[];rest=[]
    for k,v in b.items():
        z=min(target.get(k,0),len(v));out+=v[:z];rest+=v[z:]
    if len(out)<n:rnd.shuffle(rest);out+=rest[:n-len(out)]
    return out[:n]


def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--out",default="research/baojiajie/ar23_failure_value_corpus_v0_4")
    ap.add_argument("--shards",type=int,default=8); ap.add_argument("--per-product",type=int,default=120)
    ap.add_argument("--batch-size",type=int,default=100000); ap.add_argument("--max-reviews-per-parent",type=int,default=6)
    args=ap.parse_args(); outdir=Path(args.out);outdir.mkdir(parents=True,exist_ok=True)
    api=HfApi(); files=[f for f in api.list_repo_files(DATASET,repo_type="dataset") if f.endswith(".parquet")]
    shards=pick_evenly(files,args.shards)
    if not shards: raise RuntimeError("No parquet files found")
    print(f"parquet_files={len(files)} selected={shards}")
    pool=defaultdict(list); seen=defaultdict(set); parent_count=defaultdict(lambda:defaultdict(int)); scan=[]
    for shard in shards:
        local=hf_hub_download(repo_id=DATASET,filename=shard,repo_type="dataset")
        pf=pq.ParquetFile(local); base=0; broad_total=0; verified=defaultdict(int)
        names=set(pf.schema.names)
        required={"product_title","review_text","review_rating","parent_asin","asin"}
        if not required.issubset(names): raise RuntimeError(f"Missing columns in {shard}: {required-names}; names={sorted(names)}")
        cols=["product_title","review_text","review_rating","parent_asin","asin"]
        if "verified_purchase" in names: cols.append("verified_purchase")
        for batch in pf.iter_batches(columns=cols,batch_size=args.batch_size):
            title=pc.fill_null(batch.column("product_title"),"")
            mask=pc.match_substring_regex(title,BROAD_TITLE_PATTERN)
            idxs=pc.indices_nonzero(mask).to_pylist(); broad_total+=len(idxs)
            if idxs:
                d=batch.to_pydict()
                for i in idxs:
                    pt=norm(d["product_title"][i]); products=match_product(pt)
                    if not products:continue
                    tx=norm(d["review_text"][i]); parent=norm(d["parent_asin"][i])
                    if not tx:continue
                    for product in products:
                        h=hashlib.sha1((parent+"\n"+tx).lower().encode()).hexdigest()
                        if h in seen[product]:continue
                        if parent_count[product][parent]>=args.max_reviews_per_parent:continue
                        seen[product].add(h);parent_count[product][parent]+=1
                        fs,vs=codes(tx)
                        r={"corpus_version":"v0.4","source_dataset":DATASET,"source_shard":shard,"row_in_shard":base+i,
                           "product":product,"product_title":excerpt(pt,18),"parent_asin":parent,"asin":norm(d["asin"][i]),
                           "rating":d["review_rating"][i],"rating_band":band(d["review_rating"][i]),
                           "verified_purchase":d.get("verified_purchase",[None]*batch.num_rows)[i] if "verified_purchase" in d else None,
                           "evidence_excerpt":excerpt(tx,20),"review_sha1":h,"failure_codes_auto":fs,"value_codes_auto":vs,
                           "evidence_status":"PRODUCT-METADATA VERIFIED / AUTO-CODED / SEMANTIC REVIEW REQUIRED",
                           "semantic_review_required":True,"sampling_status":"EVENLY-SPACED JOINED-PARQUET SHARD DISCOVERY SAMPLE / NOT POPULATION-REPRESENTATIVE"}
                        pool[product].append(r);verified[product]+=1
            base += batch.num_rows
        scan.append({"shard":shard,"rows":base,"broad_title_hits":broad_total,"product_verified_candidates":dict(verified)})
    selected=[]
    for p in PRODUCT_TITLE_RULES:selected+=balanced(pool[p],args.per_product,20260810+len(p))
    selected=sorted(selected,key=lambda r:(r["product"],r["rating_band"],r["parent_asin"],r["review_sha1"]))
    seq=defaultdict(int);pref={"mop":"MOP","cleaning_brush":"BR","squeegee":"SQ","bucket":"BU"}
    for r in selected:seq[r["product"]]+=1;r["evidence_id"]=f"AR23M-{pref[r['product']]}-{seq[r['product']]:03d}"
    with (outdir/"external_failure_value_corpus_v0_4.jsonl").open("w",encoding="utf-8") as f:
        for r in selected:f.write(json.dumps(r,ensure_ascii=False)+"\n")
    matrix=defaultdict(lambda:{"rows":0,"failure":defaultdict(int),"value":defaultdict(int),"parents":set()})
    for r in selected:
        d=matrix[(r["product"],r["rating_band"])];d["rows"]+=1;d["parents"].add(r["parent_asin"])
        for c in r["failure_codes_auto"]:d["failure"][c]+=1
        for c in r["value_codes_auto"]:d["value"][c]+=1
    m=[]
    for (p,b),d in sorted(matrix.items()):m.append({"product":p,"rating_band":b,"selected_rows":d["rows"],"unique_parent_asin":len(d["parents"]),"failure_codes_auto":dict(sorted(d["failure"].items())),"value_codes_auto":dict(sorted(d["value"].items())),"evidence_status":"PRODUCT-METADATA VERIFIED / AUTO-CODED / SEMANTIC REVIEW REQUIRED"})
    (outdir/"product_rating_failure_value_matrix_auto_v0_4.json").write_text(json.dumps(m,ensure_ascii=False,indent=2),encoding="utf-8")
    summary={"status":"PRODUCT-METADATA VERIFIED / AUTO-CODED / SEMANTIC REVIEW REQUIRED","source_dataset":DATASET,
             "parquet_files_available":len(files),"selected_shards":shards,"rows_selected_total":len(selected),
             "rows_selected_by_product":{p:sum(r["product"]==p for r in selected) for p in PRODUCT_TITLE_RULES},
             "unique_parent_asin_by_product":{p:len({r["parent_asin"] for r in selected if r["product"]==p}) for p in PRODUCT_TITLE_RULES},
             "rating_band_counts":{b:sum(r["rating_band"]==b for r in selected) for b in ["1-2_failure_discovery","3_tradeoff","4-5_value_language","unknown"]},
             "critical_limitations":["Evenly spaced joined-data Parquet shards are a discovery sample, not a probability sample.","Product relevance is verified from product_title metadata.","Per-parent caps reduce domination but do not make the sample representative.","Automatic Failure/Value coding requires semantic review.","Counts are corpus-internal discovery counts, not prevalence.","No exact hue/finish preference can be inferred without controlled CMF stimuli."]}
    (outdir/"corpus_summary_v0_4.json").write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding="utf-8")
    (outdir/"scan_log_v0_4.json").write_text(json.dumps(scan,ensure_ascii=False,indent=2),encoding="utf-8")
    print(json.dumps(summary,ensure_ascii=False,indent=2))

if __name__=="__main__":main()
