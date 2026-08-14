import json, sys
from pathlib import Path

BASE=Path(__file__).resolve().parent
DATA=json.loads((BASE/'qjc_test_scenarios_v1.0.json').read_text(encoding='utf-8'))

results=[]
def add(test_id, ok, observations, does_not_prove):
    results.append({'test_id':test_id,'status':'PASS' if ok else 'FAIL','observations':observations,'what_it_does_not_prove':does_not_prove})
    return ok

def route_complete(s):
    return all(bool(s.get(k)) for k in ('safety','route','return','real_relation'))

def select_minimal(choices):
    viable=[c for c in choices if c.get('solves') and c.get('first_reading')!='design']
    if not viable:
        return None
    return sorted(viable,key=lambda c:c['level'])[0]['name']

def select_recovery(c):
    if not c['problem_exists']:
        return 'C0'
    if c['existing_context_sufficient']:
        return 'ExistingContext'
    if c['railing_feasible']:
        return 'RailingSupport'
    if c['larger_evidence']:
        return 'LargerCandidate'
    return 'HOLD'

# T-C10-01
route_checks={s['id']:route_complete(s) for s in DATA['route_scenarios']}
negative={'id':'negative_control','safety':True,'route':True,'return':False,'real_relation':True}
negative_detected=not route_complete(negative)
t1=all(route_checks.values()) and negative_detected
add('T-C10-01',t1,{'scenario_checks':route_checks,'negative_control_detected':negative_detected},'Does not prove real distance, duration, visibility, operations, crowd, safety or route legality.')

# T-C10-02
np=DATA['no_phone']
t2=(np['digital'] is False and np['safety'] and np['route'] and np['return'] and any(x in np['observation_sources'] for x in ('landscape','paper','human','physical_wayfinding')))
add('T-C10-02',t2,{'digital_disabled':True,'fallback_sources':np['observation_sources']},'Does not prove real signage sufficiency, staff availability, weak-network performance or accessibility.')

# T-C10-03
failure_checks={}
for f in DATA['failures']:
    ok=f['route_continues'] and len(f['fallback'])>0
    if f['id']=='rain': ok=ok and f['active_physical_hero'] is False
    if f['id']=='crowd': ok=ok and f['deep_read_in_bottleneck'] is False
    if f['id']=='return_pressure': ok=ok and f['new_deep_read'] is False
    failure_checks[f['id']]=ok
t3=all(failure_checks.values())
add('T-C10-03',t3,{'failure_checks':failure_checks},'Does not prove real emergency response, weather thresholds, closure policy, capacity or operational authority.')

# T-C10-04
attention={c['id']:select_minimal(c['choices']) for c in DATA['attention_cases']}
expected={c['id']:c['expected'] for c in DATA['attention_cases']}
t4=attention==expected
add('T-C10-04',t4,{'selected':attention,'expected':expected},'Does not prove real gaze behavior, visual salience or that a specific micro-prompt is sufficient on site.')

# T-C10-05
recovery={c['id']:select_recovery(c) for c in DATA['recovery_cases']}
recovery_expected={c['id']:c['expected'] for c in DATA['recovery_cases']}
phy01_selected=any(v=='PHY-01' for v in recovery.values())
t5=(recovery==recovery_expected and not phy01_selected)
add('T-C10-05',t5,{'selected':recovery,'expected':recovery_expected,'phy01_selected':phy01_selected},'Does not prove actual fatigue, support geometry, anchoring, clear width, maintenance or site-specific need.')

# T-C10-06
r=DATA['return_case']
t6=(r['re_recognition'] and not r['new_hero'] and not r['forced_final_task'] and r['memory_phase']=='post_visit' and r['return_priority'])
add('T-C10-06',t6,r,'Does not prove real return visibility, visitor recognition, operating window or post-visit memory behavior.')

all_pass=all(r['status']=='PASS' for r in results)
out={'suite':'QJ-C10 Remote Prototype Tests','scenario_version':DATA['version'],'all_pass':all_pass,'results':results,'promotion_ceiling':'ELIGIBLE FOR FIELD TEST' if all_pass else 'REVISE','field_pass':False}
(BASE/'qjc_prototype_test_results_v1.0.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(out,ensure_ascii=False,indent=2))
sys.exit(0 if all_pass else 1)
