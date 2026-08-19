from __future__ import annotations
import importlib.util,json,unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[3]
P=ROOT/'oleander-skills'/'oleander-3d-pipeline'/'tools'/'validate_composition_determinism.py'
C=ROOT/'oleander-skills'/'oleander-3d-pipeline'/'contracts'/'COMPOSITION_DETERMINISM_CONTRACT_v1.json'
s=importlib.util.spec_from_file_location('composition',P);m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
CONTRACT=json.loads(C.read_text(encoding='utf-8'))

def sig(v=9093,e=18171,f=9080,folds=0,nm=0,target=2):
    return {'vertices':v,'edges':e,'faces':f,'bounds_or_dimensions':[4.4687,1.8454,1.15518],'folds':folds,'nonmanifold_edges':nm,'target_diagnostic_state':target}
def r():
    return {
      'schema':'oleander.3d.composition-determinism-receipt.v1','source_identity':'V59_DIGEST','parent_revision':'V72','parent_entrypoint':'run_reference_repro_v72.py','runtime_identity':'Blender 5.2.0 LTS',
      'composition_mechanism':'EXPLICIT_MODULE_CONTEXT','semantic_scope_expected_unchanged':True,'standalone_signature':sig(),'composed_signature':sig(),
      'comparison_checks':{'source_identity_match':True,'runtime_identity_match':True,'vertices_match':True,'edges_match':True,'faces_match':True,'bounds_or_dimensions_match':True,'folds_match':True,'nonmanifold_match':True,'target_diagnostic_state_match':True,'native_artifact_hash_match':False},
      'composition_result':'PASS_COMPOSITION_DETERMINISTIC','downstream_evidence_state':'VALID_FOR_DECLARED_SCOPE','preferred_recovery_route':'NONE_REQUIRED','does_not_prove':['Design KEEP']
    }

class CompositionDeterminismTests(unittest.TestCase):
    def test_exact_composition_passes(self):self.assertTrue(m.validate(r(),CONTRACT))
    def test_same_bounds_topology_drift_cannot_pass(self):
        d=r();d['composed_signature']=sig(v=8338,e=16336,f=8000,folds=94,target=2);d['comparison_checks'].update({'vertices_match':False,'edges_match':False,'faces_match':False,'folds_match':False})
        with self.assertRaises(SystemExit) as e:m.validate(d,CONTRACT)
        self.assertIn('FAIL_COMPOSITION_PASS_SIGNATURE_DRIFT',str(e.exception))
    def test_drift_requires_quarantine(self):
        d=r();d['composed_signature']=sig(v=8338,e=16336,f=8000,folds=94,target=2);d['comparison_checks'].update({'vertices_match':False,'edges_match':False,'faces_match':False,'folds_match':False});d['composition_result']='FAIL_COMPOSITION_DETERMINISM';d['downstream_evidence_state']='VALID_FOR_DECLARED_SCOPE'
        with self.assertRaises(SystemExit) as e:m.validate(d,CONTRACT)
        self.assertIn('FAIL_COMPOSITION_DRIFT_NOT_QUARANTINED',str(e.exception))
    def test_valid_drift_failure(self):
        d=r();d['composed_signature']=sig(v=8338,e=16336,f=8000,folds=94,target=2);d['comparison_checks'].update({'vertices_match':False,'edges_match':False,'faces_match':False,'folds_match':False});d['composition_result']='FAIL_COMPOSITION_DETERMINISM';d['downstream_evidence_state']='NON_PROMOTABLE_DIAGNOSTIC_PROVENANCE';d['preferred_recovery_route']='REOPEN_NATIVE_PARENT_ARTIFACT'
        self.assertTrue(m.validate(d,CONTRACT))
    def test_source_mismatch_is_hold_not_determinism_fail(self):
        d=r();d['comparison_checks']['source_identity_match']=False;d['composition_result']='HOLD_SOURCE_OR_RUNTIME_NOT_COMPARABLE';d['downstream_evidence_state']='HOLD_NOT_COMPARABLE'
        self.assertTrue(m.validate(d,CONTRACT))
    def test_reopened_parent_requires_hash(self):
        d=r();d['composition_mechanism']='REOPENED_NATIVE_PARENT_ARTIFACT';d['composition_result']='PASS_REOPENED_PARENT_WITNESS';d['comparison_checks']['native_artifact_hash_match']=False
        with self.assertRaises(SystemExit) as e:m.validate(d,CONTRACT)
        self.assertIn('FAIL_REOPEN_WITNESS_HASH',str(e.exception))
    def test_reopened_parent_valid_witness(self):
        d=r();d['composition_mechanism']='REOPENED_NATIVE_PARENT_ARTIFACT';d['composition_result']='PASS_REOPENED_PARENT_WITNESS';d['comparison_checks']['native_artifact_hash_match']=True
        self.assertTrue(m.validate(d,CONTRACT))
    def test_equal_bounds_and_target_count_do_not_mask_fold_drift(self):
        d=r();d['composed_signature']=sig(folds=94);d['comparison_checks']['folds_match']=False;d['composition_result']='FAIL_COMPOSITION_DETERMINISM';d['downstream_evidence_state']='NON_PROMOTABLE_DIAGNOSTIC_PROVENANCE'
        self.assertTrue(m.validate(d,CONTRACT))

if __name__=='__main__':unittest.main()
