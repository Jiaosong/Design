from pathlib import Path
import json,csv,math
import numpy as np
import matplotlib.pyplot as plt

ROOT=Path(__file__).resolve().parent; RUN=ROOT/'runtime'; OUT=ROOT/'outputs'; OUT.mkdir(exist_ok=True)
C=json.loads((ROOT/'input_contract.json').read_text())
roles=[x['id'] for x in C['roles']]; intended={x['id']:x['intended_rank'] for x in C['roles']}
skies=[x['id'] for x in C['sky_scenarios']]

def readcsv(p):
    with open(p) as f:return list(csv.DictReader(f))

def spearman_rank(zone_means):
    vals=np.array([zone_means[r] for r in roles],float)
    order=np.argsort(-vals)
    ranks=np.empty(len(vals),float)
    i=0
    while i<len(vals):
        j=i; same=[order[i]]
        while j+1<len(vals) and math.isclose(vals[order[j+1]],vals[order[i]],rel_tol=1e-9,abs_tol=1e-9):
            j+=1; same.append(order[j])
        avg=(i+1+j+1)/2
        for idx in same:ranks[idx]=avg
        i=j+1
    target=np.array([intended[r] for r in roles],float)
    if np.std(ranks)==0 or np.std(target)==0:
        return float('nan')
    return float(np.corrcoef(ranks,target)[0,1])

summary=[]; all_sensor={}
for scheme in ['A','B']:
  for sky in skies:
    rows=readcsv(RUN/f'ill_{scheme}_{sky}.csv'); all_sensor[(scheme,sky)]=rows
    lux=np.array([float(r['lux']) for r in rows])
    zm={}
    for role in roles:
        arr=np.array([float(r['lux']) for r in rows if r['role']==role])
        zm[role]=float(arr.mean())
    summary.append({
      'scheme':scheme,'sky':sky,'mean_lux':float(lux.mean()),'min_lux':float(lux.min()),'max_lux':float(lux.max()),
      'u0_min_over_mean':float(lux.min()/lux.mean()) if lux.mean() else None,
      'cv_std_over_mean':float(lux.std()/lux.mean()) if lux.mean() else None,
      **{f'{r.lower()}_mean_lux':zm[r] for r in roles},
      'role_rank_spearman':spearman_rank(zm)
    })

fields=list(summary[0])
with (OUT/'illuminance_summary.csv').open('w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=fields); w.writeheader(); w.writerows(summary)

glare=[]
for p in sorted(RUN.glob('glare_*.csv')):
    glare+=readcsv(p)
with (OUT/'glare_summary.csv').open('w',newline='') as f:
    if glare:
      w=csv.DictWriter(f,fieldnames=list(glare[0])); w.writeheader(); w.writerows(glare)

def agg_scheme(scheme):
    rows=[r for r in summary if r['scheme']==scheme]
    return {
      'mean_role_rank_spearman':float(np.mean([r['role_rank_spearman'] for r in rows])),
      'min_role_rank_spearman':float(np.min([r['role_rank_spearman'] for r in rows])),
      'mean_u0':float(np.mean([r['u0_min_over_mean'] for r in rows])),
      'mean_cv':float(np.mean([r['cv_std_over_mean'] for r in rows]))
    }
aggregate={'A':agg_scheme('A'),'B':agg_scheme('B')}
if glare:
    for scheme in ['A','B']:
        dgps=[float(r['dgp']) for r in glare if r['scheme']==scheme and r.get('dgp') not in ('','nan') and math.isfinite(float(r['dgp']))]
        aggregate[scheme]['mean_dgp_clear_EW']=float(np.mean(dgps)) if dgps else None
        aggregate[scheme]['max_dgp_clear_EW']=float(np.max(dgps)) if dgps else None

per_sky=[]
for sky in skies:
    a=next(r for r in summary if r['scheme']=='A' and r['sky']==sky)
    b=next(r for r in summary if r['scheme']=='B' and r['sky']==sky)
    per_sky.append({
        'sky':sky,
        'delta_B_minus_A_mean_lux':b['mean_lux']-a['mean_lux'],
        'delta_B_minus_A_u0':b['u0_min_over_mean']-a['u0_min_over_mean'],
        'delta_B_minus_A_cv':b['cv_std_over_mean']-a['cv_std_over_mean'],
        'delta_B_minus_A_role_rank_spearman':b['role_rank_spearman']-a['role_rank_spearman']
    })

expected_ill=all((RUN/f'ill_{s}_{k}.csv').exists() for s in ['A','B'] for k in skies)
expected_glare=all((RUN/f'glare_{s}_{k}_{r}.csv').exists() for s in ['A','B'] for k in ['CLEAR_E','CLEAR_W'] for r in roles)
finite=all(math.isfinite(r['mean_lux']) and math.isfinite(r['role_rank_spearman']) for r in summary)
comparison={
 'aggregate':aggregate,
 'per_sky_B_minus_A':per_sky,
 'exercise_interpretation':{
   'scheme_A':'control condition prioritizing even aperture distribution',
   'scheme_B':'role-sequence condition reallocating the same total aperture area',
   'role_rank_metric':'custom exercise heuristic; rank-only, not a lighting standard',
   'absolute_lux':'reported but no compliance threshold claimed because program/project criteria are absent',
   'dgp':'reported as simulation evidence only; no project comfort claim'
 }
}
(OUT/'comparison_summary.json').write_text(json.dumps(comparison,indent=2))

gate={
 'radiance_runtime_gate':'PASS' if expected_ill and finite else 'FAIL',
 'glare_runtime_gate':'PASS' if expected_glare else 'FAIL',
 'performance_interface_gate':'PASS' if expected_ill and expected_glare and finite else 'FAIL',
 'project_geometry_gate':'OPEN','project_material_gate':'OPEN','project_sky_time_gate':'OPEN','project_program_threshold_gate':'OPEN',
 'project_reality_promotion':False,
 'practice_status':'PERFORMANCE INTERFACE VERIFIED ON SYNTHETIC TEST CELL / PROJECT REALITY OPEN' if expected_ill and expected_glare and finite else 'PERFORMANCE INTERFACE INCOMPLETE',
 'final_artifact_review':'PENDING'
}
(OUT/'gate_decision.json').write_text(json.dumps(gate,indent=2))

sensors=readcsv(RUN/'sensors.csv')
xs=sorted(set(float(r['x_m']) for r in sensors)); ys=sorted(set(float(r['y_m']) for r in sensors))
def matrix_for(scheme,sky):
    rows=all_sensor[(scheme,sky)]
    d={(float(r['x_m']),float(r['y_m'])):float(r['lux']) for r in rows}
    return np.array([[d[(x,y)] for x in xs] for y in ys])

# A/B OVC maps must share a single numeric color scale so visual comparison is truthful.
ZA=matrix_for('A','OVC'); ZB=matrix_for('B','OVC')
shared_vmin=float(min(ZA.min(),ZB.min())); shared_vmax=float(max(ZA.max(),ZB.max()))
(OUT/'visual_scale_contract.json').write_text(json.dumps({
    'heatmap_pair':'A/B OVC','vmin_lux':shared_vmin,'vmax_lux':shared_vmax,
    'rule':'Both A/B OVC heatmaps use exactly the same lux color scale.'
},indent=2))
for scheme,Z in [('A',ZA),('B',ZB)]:
    fig,ax=plt.subplots(figsize=(10,4.5))
    im=ax.imshow(Z,origin='lower',extent=[min(xs),max(xs),min(ys),max(ys)],aspect='auto',vmin=shared_vmin,vmax=shared_vmax)
    ax.set_title(f'SP03-R02 | Scheme {scheme} | OVC | workplane illuminance [lux] | shared A/B scale')
    ax.set_xlabel('Sequence direction x [m]'); ax.set_ylabel('y [m]')
    for x in [3,6,9]: ax.axvline(x,linewidth=0.8)
    fig.colorbar(im,ax=ax,label='lux')
    fig.tight_layout(); fig.savefig(OUT/f'heatmap_{scheme}_OVC.png',dpi=180); plt.close(fig)

# Difference map is descriptive only: positive means B > A under the identical OVC input.
fig,ax=plt.subplots(figsize=(10,4.5))
im=ax.imshow(ZB-ZA,origin='lower',extent=[min(xs),max(xs),min(ys),max(ys)],aspect='auto')
ax.set_title('SP03-R02 | OVC | Scheme B - Scheme A workplane illuminance [lux]')
ax.set_xlabel('Sequence direction x [m]'); ax.set_ylabel('y [m]')
for x in [3,6,9]: ax.axvline(x,linewidth=0.8)
fig.colorbar(im,ax=ax,label='delta lux (B - A)')
fig.tight_layout(); fig.savefig(OUT/'heatmap_delta_B_minus_A_OVC.png',dpi=180); plt.close(fig)

for sky in skies:
    fig,ax=plt.subplots(figsize=(9,4.5))
    x=np.arange(len(roles)); width=.36
    for i,scheme in enumerate(['A','B']):
        row=next(r for r in summary if r['scheme']==scheme and r['sky']==sky)
        vals=[row[f'{rr.lower()}_mean_lux'] for rr in roles]
        ax.bar(x+(i-.5)*width,vals,width,label=f'Scheme {scheme}')
    ax.set_xticks(x,roles); ax.set_ylabel('Zone mean illuminance [lux]'); ax.set_title(f'Role-zone means | {sky}')
    ax.legend(); fig.tight_layout(); fig.savefig(OUT/f'role_means_{sky}.png',dpi=180); plt.close(fig)

# Schematic comparison plan generated from the same data contract, not a decorative rendering.
fig,ax=plt.subplots(figsize=(10,3.8))
ax.set_xlim(0,C['geometry']['room_m']['length_x']); ax.set_ylim(0,2.2)
for x in [0,3,6,9,12]: ax.axvline(x,linewidth=0.8)
for i,r in enumerate(roles): ax.text(i*3+1.5,2.0,r,ha='center',va='center')
for row_y,scheme,key in [(1.35,'A','scheme_A_uniform_widths_m'),(.65,'B','scheme_B_sequence_widths_m')]:
    ax.text(.15,row_y+0.22,f'Scheme {scheme}',ha='left',va='bottom')
    for c,w in zip(C['aperture_control']['centers_x_m'],C['aperture_control'][key]):
        ax.plot([c-w/2,c+w/2],[row_y,row_y],linewidth=8,solid_capstyle='butt')
ax.set_xlabel('Sequence direction x [m]'); ax.set_yticks([])
ax.set_title('Controlled aperture-distribution contract | same total skylight area = 7.2 m²')
fig.tight_layout(); fig.savefig(OUT/'scheme_aperture_contract.png',dpi=180); plt.close(fig)

report=['# SP03-R02 | Automated Simulation Report','',f"Runtime gate: **{gate['radiance_runtime_gate']}**",f"Glare gate: **{gate['glare_runtime_gate']}**",'', '## Aggregate']
for s in ['A','B']:
    report.append(f"- Scheme {s}: role-rank mean Spearman={aggregate[s]['mean_role_rank_spearman']:.3f}; mean U0={aggregate[s]['mean_u0']:.3f}; mean CV={aggregate[s]['mean_cv']:.3f}; max DGP(clear E/W)={aggregate[s].get('max_dgp_clear_EW')}")
report += ['', '## Truth boundary','No real project geometry, measured material reflectance/transmittance, project weather/time, program lux criterion, or user outcome is claimed. Final artifact review remains PENDING until exported plots/HDR-derived evidence are manually inspected.']
(OUT/'AUTOMATED_REPORT.md').write_text('\n'.join(report))
print(json.dumps({'gate':gate,'aggregate':aggregate,'per_sky_B_minus_A':per_sky},indent=2))
