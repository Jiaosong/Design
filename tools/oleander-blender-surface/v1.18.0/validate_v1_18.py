#!/usr/bin/env python3
from pathlib import Path
import argparse,base64,gzip,json,re,sys

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--bundle',required=True); ap.add_argument('--out',required=True); a=ap.parse_args()
    raw=gzip.decompress(base64.b64decode(Path(a.bundle).read_text().strip()))
    b=json.loads(raw)
    f=b['files']
    retire=f['governance/material-archetype-retirement/MATERIAL_ARCHETYPE_RETIREMENT_REGISTER_v1.json']
    errors=[]
    if retire.get('version')!='v1.18.0': errors.append('version')
    if len(retire.get('archetypes',[]))!=6: errors.append('archetype_count')
    if len(retire.get('texture_recipes',[]))!=8: errors.append('texture_recipe_count')
    for a0 in retire['archetypes']:
        d=a0.get('decision','')
        if not ('RETIRED_FROM_AUTOBIND' in d or 'RETIRE_AND' in d): errors.append(a0['archetype_id']+':autobind_not_retired')
        mf=a0.get('legacy_values',{}).get('material_family')
        if mf in {'TPE_PU','PC_PMMA'} and not a0.get('split_required'): errors.append(a0['archetype_id']+':merged_identity_not_split')
    adapters={
      f['evidence-adapters/ADAPTER-BJ-XJ01-R02-001.json']['adapter_id']:f['evidence-adapters/ADAPTER-BJ-XJ01-R02-001.json'],
      f['evidence-adapters/ADAPTER-TIMER-HERO-CMF-001.json']['adapter_id']:f['evidence-adapters/ADAPTER-TIMER-HERO-CMF-001.json'],
    }
    binds=[f['bindings/BIND-BJ-XJ01-R02-001.json'],f['bindings/BIND-TIMER-HERO-CMF-001.json']]
    resolved=[]
    for bd in binds:
        ad=adapters.get(bd['adapter'])
        if not ad: errors.append(bd['binding_id']+':missing_adapter'); continue
        if ad['project']=='Baojiajie XJ01':
            rows=[]
            for x in ad['representation_bindings']:
                if x['target'] in bd['requested_targets']:
                    rows.append({'target':x['target'],'lane':x['lane'],'activation':'ALLOW_REPRESENTATION_ONLY','technique_permission':'LOCKED_EXISTING_IMPLEMENTATION_ONLY'})
            for x in ad['blocked_bindings']:
                if x['target'] in bd['requested_targets']:
                    rows.append({'target':x['target'],'lane':'BLOCKED','activation':'DENY','technique_permission':'NONE','why':x['why']})
        else:
            rows=[]
            for x in ad['project_visualization_profiles']:
                if x['target'] in bd['requested_targets']:
                    rows.append({'target':x['target'],'lane':x['lane'],'activation':'ALLOW_PROJECT_PROFILE','generic_archetype_binding':x['generic_archetype_binding'],'technique_permission':'PROJECT_PROFILE_ONLY / NO_GENERIC_AUTOBIND'})
        missing=set(bd['requested_targets'])-{r['target'] for r in rows}
        if missing: errors.append(bd['binding_id']+':unresolved:'+','.join(sorted(missing)))
        resolved.append({'binding_id':bd['binding_id'],'rows':rows})
    # Hard behavior assertions.
    xj=next(x for x in resolved if x['binding_id']=='BIND-BJ-XJ01-R02-001')['rows']
    assert next(r for r in xj if r['target']=='PP_PRIMARY_FIELD')['lane']=='VISUALIZATION_LOCKED'
    assert next(r for r in xj if r['target']=='IRON_VISIBLE')['lane']=='BLOCKED'
    assert next(r for r in xj if r['target']=='PU_CONTACT')['lane']=='BLOCKED'
    timer=next(x for x in resolved if x['binding_id']=='BIND-TIMER-HERO-CMF-001')['rows']
    assert all(r['lane']=='VISUALIZATION_LOCKED' for r in timer)
    assert all(r.get('technique_permission')=='PROJECT_PROFILE_ONLY / NO_GENERIC_AUTOBIND' for r in timer)
    report={'schema':'oleander.v1.18-ci-validation.v1','status':'PASS' if not errors else 'FAIL','errors':errors,'resolved':resolved,'global_rule':'No generic material archetype auto-binding.'}
    Path(a.out).parent.mkdir(parents=True,exist_ok=True); Path(a.out).write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(report,ensure_ascii=False,indent=2)); return 0 if not errors else 5
if __name__=='__main__': raise SystemExit(main())
