from __future__ import annotations
import importlib.util,json,unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[3]
P=ROOT/'oleander-skills'/'oleander-3d-pipeline'/'tools'/'validate_bounded_causal_iteration.py'
C=ROOT/'oleander-skills'/'oleander-3d-pipeline'/'contracts'/'BOUNDED_CAUSAL_ITERATION_CONTRACT_v1.json'
s=importlib.util.spec_from_file_location('bounded_iteration',P);m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
CONTRACT=json.loads(C.read_text(encoding='utf-8'))


def r():
    return {
      'schema':'oleander.3d.bounded-causal-iteration-receipt.v1','experiment_id':'V72_XZ_BOUNDARY',
      'baseline_revision':'V69','candidate_revision':'V72','target_metric_id':'XZ_STRADDLING_FACE_COUNT',
      'target_direction':'ZERO_REQUIRED','operation_family':'LOCAL_BISECT_SAME_CANONICAL_BOUNDARY',
      'locked_variables':['SOURCE_V59','CANONICAL_BOUNDARY','BAND','BISect_OPERATOR_FAMILY'],
      'protected_invariants':['BOUNDS','FOLDS','NONMANIFOLD','SOURCE_DIGEST'],
      'material_improvement_rule':{'type':'ABSOLUTE_DECREASE','epsilon':1.0},'max_iterations':4,
      'iterations':[
        {'before':118,'after':34,'protected_invariants':'PASS','target_reached':False},
        {'before':34,'after':4,'protected_invariants':'PASS','target_reached':False},
        {'before':4,'after':2,'protected_invariants':'PASS','target_reached':False},
        {'before':2,'after':2,'protected_invariants':'PASS','target_reached':False}
      ],
      'stop_conditions':['TARGET_REACHED','STAGNATION_NO_MATERIAL_IMPROVEMENT','PROTECTED_INVARIANT_REGRESSION','MAX_ITERATION_BUDGET_REACHED'],
      'stop_reason':'STAGNATION_NO_MATERIAL_IMPROVEMENT','result':'HOLD_STAGNATION_RECLASSIFY','rollback_lkg':'V69',
      'does_not_prove':['aperture closure','reference fidelity','Design KEEP']
    }

class BoundedIterationTests(unittest.TestCase):
    def test_v72_stagnation_sequence_is_valid(self):self.assertTrue(m.validate(r(),CONTRACT))
    def test_continuing_after_stagnation_fails(self):
        d=r();d['iterations'][-1]={'before':2,'after':2,'protected_invariants':'PASS','target_reached':False};d['iterations'].append({'before':2,'after':1,'protected_invariants':'PASS','target_reached':False});d['max_iterations']=5
        with self.assertRaises(SystemExit) as e:m.validate(d,CONTRACT)
        self.assertIn('FAIL_ITERATION_CONTINUED_AFTER_STAGNATION',str(e.exception))
    def test_protected_regression_stops(self):
        d=r();d['iterations']=d['iterations'][:2]+[{'before':4,'after':1,'protected_invariants':'FAIL','target_reached':False}];d['stop_reason']='PROTECTED_INVARIANT_REGRESSION';d['result']='FAIL_PROTECTED_INVARIANT_REGRESSION'
        self.assertTrue(m.validate(d,CONTRACT))
    def test_continue_after_protected_regression_fails(self):
        d=r();d['iterations']=[{'before':10,'after':5,'protected_invariants':'FAIL','target_reached':False},{'before':5,'after':1,'protected_invariants':'PASS','target_reached':False}];d['max_iterations']=2;d['stop_reason']='TARGET_REACHED';d['iterations'][-1]['target_reached']=True;d['result']='PASS_TARGET_REACHED'
        with self.assertRaises(SystemExit) as e:m.validate(d,CONTRACT)
        self.assertIn('FAIL_ITERATION_CONTINUED_AFTER_PROTECTED_REGRESSION',str(e.exception))
    def test_target_reached_stops(self):
        d=r();d['iterations']=[{'before':4,'after':0,'protected_invariants':'PASS','target_reached':True}];d['stop_reason']='TARGET_REACHED';d['result']='PASS_TARGET_REACHED'
        self.assertTrue(m.validate(d,CONTRACT))
    def test_continuing_after_target_reached_fails(self):
        d=r();d['iterations']=[{'before':4,'after':0,'protected_invariants':'PASS','target_reached':True},{'before':0,'after':0,'protected_invariants':'PASS','target_reached':True}];d['max_iterations']=2;d['stop_reason']='TARGET_REACHED';d['result']='PASS_TARGET_REACHED'
        with self.assertRaises(SystemExit) as e:m.validate(d,CONTRACT)
        self.assertIn('FAIL_ITERATION_CONTINUED_AFTER_TARGET_REACHED',str(e.exception))
    def test_budget_cannot_be_exceeded(self):
        d=r();d['max_iterations']=3
        with self.assertRaises(SystemExit) as e:m.validate(d,CONTRACT)
        self.assertIn('FAIL_BOUNDED_ITERATION_BUDGET_EXCEEDED',str(e.exception))
    def test_max_budget_hold_requires_full_budget(self):
        d=r();d['iterations']=d['iterations'][:3];d['stop_reason']='MAX_ITERATION_BUDGET_REACHED';d['result']='HOLD_MAX_ITERATION_BUDGET_REACHED';d['max_iterations']=4
        with self.assertRaises(SystemExit) as e:m.validate(d,CONTRACT)
        self.assertIn('FAIL_MAX_BUDGET_STOP_BEFORE_BUDGET',str(e.exception))
    def test_metric_improvement_smaller_than_epsilon_is_stagnation(self):
        d=r();d['target_direction']='LOWER_IS_BETTER';d['material_improvement_rule']['epsilon']=0.5;d['iterations']=[{'before':2.0,'after':1.8,'protected_invariants':'PASS','target_reached':False}];d['max_iterations']=1;d['stop_reason']='STAGNATION_NO_MATERIAL_IMPROVEMENT';d['result']='HOLD_STAGNATION_RECLASSIFY'
        self.assertTrue(m.validate(d,CONTRACT))

if __name__=='__main__':unittest.main()
