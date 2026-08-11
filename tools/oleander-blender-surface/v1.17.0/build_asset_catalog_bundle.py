#!/usr/bin/env python3
from __future__ import annotations
import argparse,json,re,sys
from pathlib import Path
import bpy

def parse():
    av=sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else []
    p=argparse.ArgumentParser();p.add_argument('--mode',choices=['apply','verify'],required=True);p.add_argument('--bundle',required=True);p.add_argument('--out-dir',required=True);return p.parse_args(av)
def safe(v):
    if isinstance(v,(str,int,float,bool,type(None))):return v
    try:return list(v)
    except:return str(v)
def iface(g,io):
    out=[]
    for it in getattr(g.interface,'items_tree',[]):
        if getattr(it,'item_type',None)=='SOCKET' and getattr(it,'in_out',None)==io:
            out.append({'name':it.name,'identifier':getattr(it,'identifier',''),'socket_type':getattr(it,'socket_type',''),'default':safe(getattr(it,'default_value',None)),'ui_min':safe(getattr(it,'min_value',None)),'ui_max':safe(getattr(it,'max_value',None))})
    return out
def validate_calls(bundle):
    errs=[];mat={c['call_id']:c for c in bundle['material_calls']}
    for c in bundle['material_calls']:
        refs={r.get('source_id') for r in c.get('evidence_refs',[])}
        for p in c.get('parameter_calls',[]):
            if p.get('status') in {'SUPPORTED','VISUALIZATION_ONLY'} and not p.get('evidence_ref'):errs.append(c['call_id']+':supported_without_evidence:'+p.get('parameter','?'))
            if p.get('evidence_ref') not in refs:errs.append(c['call_id']+':missing_top_level_evidence_ref:'+str(p.get('evidence_ref')))
    for c in bundle['project_calls']:
        for mid in c.get('material_calls',[]):
            if mid not in mat:errs.append(c['call_id']+':missing_material_call:'+mid)
    return errs
def write_cdf(cat,out):
    lines=['# This is an Asset Catalog Definition file for Blender.','# OLEANDER Blender Surface System v1.17.0','VERSION 1','']
    for g in cat['catalogs']:lines.append(f"{g['catalog_uuid']}:{g['catalog']}:{g['simple']}")
    (out/'blender_assets.cats.txt').write_text('\n'.join(lines)+'\n',encoding='utf-8')
def apply(bundle,out):
    cat=bundle['asset_catalog'];con=bundle['debug_contract'];can=re.compile(con['canonical_name_regex']);forb=re.compile(con['forbidden_name_regex']);rep={'mode':'apply','blender':bpy.app.version_string,'groups':[],'errors':validate_calls(bundle)}
    for spec in cat['catalogs']:
        name=spec['name'];g=bpy.data.node_groups.get(name);row={'name':name,'errors':[]}
        if not g:row['errors'].append('missing_group');rep['errors'].append(name+':missing_group');rep['groups'].append(row);continue
        if not can.match(name):row['errors'].append('canonical_name_fail')
        if forb.match(name):row['errors'].append('legacy_name_fail')
        if g.asset_data is None:g.asset_mark()
        md=g.asset_data;md.catalog_id=spec['catalog_uuid']
        try:md.description=f"{spec['role']}. OLEANDER Surface System v1.17.0. Material truth requires evidence-driven calls."
        except:pass
        for tag in spec.get('tags',[]):
            try:md.tags.new(tag,skip_if_exists=True)
            except:
                try:md.tags.new(tag)
                except:pass
        ins=iface(g,'INPUT');outs=[x['name'] for x in iface(g,'OUTPUT')];missing=[x for x in spec['debug'] if x not in outs]
        if missing:row['errors'].append('missing_debug:'+','.join(missing))
        if str(md.catalog_id)!=spec['catalog_uuid']:row['errors'].append('catalog_mismatch')
        g['OLEANDER_SYSTEM_VERSION']='v1.17.0';g['OLEANDER_CONTRACT_VERSION']='nodegroup-debug-contract.v1';g['OLEANDER_ROLE']=spec['role'];g['OLEANDER_LEGACY_LAB_ALIAS']=spec['legacy'];g['OLEANDER_DEBUG_OUTPUTS']=json.dumps(spec['debug'],ensure_ascii=False);g['OLEANDER_EVIDENCE_POLICY']='Technique source only; material/physical truth comes from evidence-driven calls.';g['OLEANDER_INPUT_CONTRACT']=json.dumps(ins,ensure_ascii=False)
        row.update({'catalog_id':str(md.catalog_id),'tags':[t.name for t in md.tags],'inputs':ins,'outputs':outs,'debug':spec['debug']});rep['errors'] += [name+':'+e for e in row['errors']];rep['groups'].append(row)
    write_cdf(cat,out);rep['status']='PASS' if not rep['errors'] else 'FAIL';(out/'ASSET_DEBUG_APPLY_REPORT.json').write_text(json.dumps(rep,ensure_ascii=False,indent=2)+'\n');bpy.ops.wm.save_as_mainfile(filepath=str((out/'OLEANDER_Blender_Surface_Assets_v1.17.0_bundle.blend').resolve()));return rep
def verify(bundle,out):
    cat=bundle['asset_catalog'];rep={'mode':'verify-reopen','blender':bpy.app.version_string,'groups':[],'errors':validate_calls(bundle)}
    for spec in cat['catalogs']:
        g=bpy.data.node_groups.get(spec['name']);row={'name':spec['name'],'errors':[]}
        if not g:row['errors'].append('missing_group')
        else:
            if g.asset_data is None:row['errors'].append('not_asset')
            elif str(g.asset_data.catalog_id)!=spec['catalog_uuid']:row['errors'].append('catalog_mismatch')
            for k in ['OLEANDER_SYSTEM_VERSION','OLEANDER_CONTRACT_VERSION','OLEANDER_ROLE','OLEANDER_LEGACY_LAB_ALIAS','OLEANDER_DEBUG_OUTPUTS','OLEANDER_EVIDENCE_POLICY','OLEANDER_INPUT_CONTRACT']:
                if k not in g:row['errors'].append('missing_prop:'+k)
        rep['errors'] += [spec['name']+':'+e for e in row['errors']];rep['groups'].append(row)
    rep['status']='PASS' if not rep['errors'] else 'FAIL';(out/'ASSET_DEBUG_REOPEN_REPORT.json').write_text(json.dumps(rep,ensure_ascii=False,indent=2)+'\n');return rep
def main():
    a=parse();out=Path(a.out_dir).resolve();out.mkdir(parents=True,exist_ok=True);bundle=json.loads(Path(a.bundle).read_text())
    rep=apply(bundle,out) if a.mode=='apply' else verify(bundle,out);print(json.dumps(rep,ensure_ascii=False,indent=2));return 0 if rep['status']=='PASS' else 5
if __name__=='__main__':raise SystemExit(main())
