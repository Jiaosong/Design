import copy
import importlib.util
import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
VALIDATOR = ROOT / "00-governance/schemas/validate_professional_domain_process.py"
STRUCTURAL = ROOT / "00-governance/schemas/structural-engineering-design-process.v1.json"
MEP = ROOT / "00-governance/schemas/building-services-mep-design-process.v1.json"
SYSTEMS = ROOT / "00-governance/schemas/systems-engineering-design-process.v1.json"
HCD = ROOT / "00-governance/schemas/digital-product-hcd-design-process.v1.json"
INTERIOR = ROOT / "00-governance/schemas/interior-design-process.v1.json"
LANDSCAPE = ROOT / "00-governance/schemas/landscape-architecture-design-process.v1.json"
LIGHTING = ROOT / "00-governance/schemas/lighting-design-process.v1.json"
ARCH_GRAPH = ROOT / "00-governance/runtime/OLEANDER_ARCHITECTURE_CONTROL_GRAPH_v2.1.json"
EXAMPLE = ROOT / "00-governance/schemas/professional-domain-process.example.json"
ARCH_BODY = ROOT / "00-governance/architecture-design-development-process-v1.0.md"
STRUCT_BODY = ROOT / "00-governance/structural-engineering-design-process-v1.0.md"
MEP_BODY = ROOT / "00-governance/building-services-mep-design-process-v1.0.md"
SYSTEMS_BODY = ROOT / "00-governance/systems-engineering-design-development-process-v1.0.md"
HCD_BODY = ROOT / "00-governance/digital-product-hcd-design-development-process-v1.0.md"

EXPECTED_BODY_ROLES = {
    "PROFESSIONAL_QUESTION_SCOPE",
    "CURRENT_CONDITION_PROBLEM",
    "AUTHORITY_KNOWLEDGE_EVIDENCE_INPUTS",
    "PROFESSIONAL_CRITERIA_INTENT",
    "DEVELOPMENT_ANALYSIS_COMPARISON_MECHANISM",
    "CROSS_DOMAIN_INTERFACES",
    "NATIVE_OUTPUT_SOURCE_OF_TRUTH",
    "ACTUAL_READBACK_FINDING",
    "FAILURE_OPEN_DOES_NOT_PROVE",
    "VERDICT_CLAIM_REOPEN_NEXT_ACTION",
}


def load_validator():
    spec = importlib.util.spec_from_file_location(
        "professional_domain_process_validator", VALIDATOR
    )
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class ProfessionalDomainProcessContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.validator = load_validator()
        cls.structural = json.loads(STRUCTURAL.read_text(encoding="utf-8"))
        cls.mep = json.loads(MEP.read_text(encoding="utf-8"))
        cls.systems = json.loads(SYSTEMS.read_text(encoding="utf-8"))
        cls.hcd = json.loads(HCD.read_text(encoding="utf-8"))
        cls.interior = json.loads(INTERIOR.read_text(encoding="utf-8"))
        cls.landscape = json.loads(LANDSCAPE.read_text(encoding="utf-8"))
        cls.lighting = json.loads(LIGHTING.read_text(encoding="utf-8"))
        cls.arch_graph = json.loads(ARCH_GRAPH.read_text(encoding="utf-8"))
        cls.example = json.loads(EXAMPLE.read_text(encoding="utf-8"))

    def current_definitions(self):
        return (self.structural, self.mep)

    def test_systems_engineering_candidate_validates_without_currentizing(self):
        self.assertEqual(self.validator.validate_payload(self.systems), [])
        self.assertEqual(self.validator.validate_fallback_structure(self.systems), [])
        self.assertIn("CANDIDATE", self.systems["authority_position"])
        self.assertIn("not Current", self.systems["authority_position"])

        systems_state = next(
            row
            for row in self.arch_graph["professional_domain_process_state"]
            if row["domain"] == "Systems Engineering"
        )
        self.assertEqual(
            systems_state["state"], "CONTRACT_ENVELOPE_AVAILABLE_PROCESS_OPEN"
        )
        self.assertIsNone(systems_state["current_process_ref"])

    def test_systems_engineering_candidate_has_domain_native_stage_chain(self):
        self.assertEqual(
            [stage["stage_id"] for stage in self.systems["stages"]],
            [
                "SYS-00",
                "SYS-01",
                "SYS-02",
                "SYS-03",
                "SYS-04",
                "SYS-05",
                "SYS-06",
                "SYS-07",
                "SYS-08",
            ],
        )
        for stage in self.systems["stages"]:
            with self.subTest(stage_id=stage["stage_id"]):
                roles = stage["stage_body_contract"]["required_semantic_sections"]
                self.assertEqual(set(roles), EXPECTED_BODY_ROLES)
                self.assertEqual(len(roles), 10)
                self.assertIn(stage["stage_id"], stage["stage_body_contract"]["title_rule"])
                self.assertTrue(stage["interface_binding_requirements"])
                self.assertNotIn("interface_bindings", stage)

    def test_systems_engineering_candidate_preserves_integration_and_transfer_boundaries(self):
        interface_policy = self.systems["interface_contract"]["interface_maturity_policy"]
        self.assertIn("R-F", interface_policy)
        self.assertIn("never inferred", interface_policy)

        scope_out = " ".join(self.systems["scope_out"])
        self.assertIn("V-model", scope_out)
        self.assertIn("R-F interface maturity", scope_out)

        in_use = self.systems["stages"][-1]
        self.assertIn("G9", " ".join(in_use["interface_requirements"]))
        self.assertTrue(
            any("causality" in item for item in in_use["does_not_prove"])
        )
        self.assertTrue(
            any("transferable knowledge" in item for item in in_use["does_not_prove"])
        )

    def test_hcd_candidate_validates_without_currentizing(self):
        self.assertEqual(self.validator.validate_payload(self.hcd), [])
        self.assertEqual(self.validator.validate_fallback_structure(self.hcd), [])
        self.assertIn("CANDIDATE", self.hcd["authority_position"])
        self.assertIn("not Current", self.hcd["authority_position"])

        hcd_state = next(
            row
            for row in self.arch_graph["professional_domain_process_state"]
            if row["domain"] == "Digital Product / HCD"
        )
        self.assertEqual(
            hcd_state["state"], "CONTRACT_ENVELOPE_AVAILABLE_PROCESS_OPEN"
        )
        self.assertIsNone(hcd_state["current_process_ref"])

    def test_hcd_candidate_has_domain_native_stage_chain(self):
        self.assertEqual(
            [stage["stage_id"] for stage in self.hcd["stages"]],
            [
                "HCD-00",
                "HCD-01",
                "HCD-02",
                "HCD-03",
                "HCD-04",
                "HCD-05",
                "HCD-06",
                "HCD-07",
                "HCD-08",
            ],
        )
        for stage in self.hcd["stages"]:
            with self.subTest(stage_id=stage["stage_id"]):
                roles = stage["stage_body_contract"]["required_semantic_sections"]
                self.assertEqual(set(roles), EXPECTED_BODY_ROLES)
                self.assertEqual(len(roles), 10)
                self.assertIn(stage["stage_id"], stage["stage_body_contract"]["title_rule"])
                self.assertTrue(stage["interface_binding_requirements"])
                self.assertNotIn("interface_bindings", stage)

    def test_hcd_candidate_preserves_human_evidence_accessibility_and_owner_boundaries(self):
        scope_out = " ".join(self.hcd["scope_out"])
        self.assertIn("software/backend/data correctness authority", scope_out)
        self.assertIn("accessibility/legal/statutory certification", scope_out)
        self.assertIn("R-F interface maturity", scope_out)

        interface_policy = self.hcd["interface_contract"]["interface_maturity_policy"]
        self.assertIn("R-F", interface_policy)
        self.assertIn("never inferred", interface_policy)

        evaluation = next(
            stage for stage in self.hcd["stages"] if stage["stage_id"] == "HCD-07"
        )
        evaluation_does_not_prove = " ".join(evaluation["does_not_prove"])
        self.assertIn("accessibility certification", evaluation_does_not_prove)
        self.assertIn("universal usability", evaluation_does_not_prove)

        in_use_does_not_prove = " ".join(self.hcd["stages"][-1]["does_not_prove"])
        self.assertIn("causality from correlation", in_use_does_not_prove)
        self.assertIn("transferable knowledge", in_use_does_not_prove)
        self.assertIn("Current Knowledge", in_use_does_not_prove)

    def test_spatial_professional_candidates_validate_without_currentizing(self):
        candidates = {
            "Interior Design": self.interior,
            "Landscape Architecture": self.landscape,
            "Lighting Design": self.lighting,
        }
        for domain, definition in candidates.items():
            with self.subTest(domain=domain):
                self.assertEqual(self.validator.validate_payload(definition), [])
                self.assertEqual(self.validator.validate_fallback_structure(definition), [])
                self.assertIn("CANDIDATE", definition["authority_position"])
                self.assertIn("not Current", definition["authority_position"])
                current = next(
                    row
                    for row in self.arch_graph["professional_domain_process_state"]
                    if row["domain"] == domain
                )
                self.assertEqual(
                    current["state"], "CONTRACT_ENVELOPE_AVAILABLE_PROCESS_OPEN"
                )
                self.assertIsNone(current["current_process_ref"])

    def test_interior_candidate_is_materially_interior_native(self):
        self.assertEqual(
            [stage["stage_id"] for stage in self.interior["stages"]],
            [f"INT-{i:02d}" for i in range(10)],
        )
        text = json.dumps(self.interior, ensure_ascii=False)
        for phrase in ("FF&E", "storage", "material", "joinery", "wet", "mockup", "maintenance"):
            self.assertIn(phrase, text)
        self.assertIn("R-F", self.interior["interface_contract"]["interface_maturity_policy"])
        for stage in self.interior["stages"]:
            self.assertNotIn("interface_bindings", stage)

    def test_landscape_candidate_is_living_site_system_not_decorative_planting(self):
        self.assertEqual(
            [stage["stage_id"] for stage in self.landscape["stages"]],
            [f"LAN-{i:02d}" for i in range(10)],
        )
        text = json.dumps(self.landscape, ensure_ascii=False)
        for phrase in ("grading", "water", "soil", "root", "planting", "microclimate", "establishment", "seasonal"):
            self.assertIn(phrase, text)
        in_use = " ".join(self.landscape["stages"][-1]["does_not_prove"])
        self.assertIn("causal", in_use)
        self.assertIn("Current Knowledge", in_use)

    def test_lighting_candidate_keeps_photometry_and_specialist_claims_bounded(self):
        self.assertEqual(
            [stage["stage_id"] for stage in self.lighting["stages"]],
            [f"LGT-{i:02d}" for i in range(10)],
        )
        text = json.dumps(self.lighting, ensure_ascii=False)
        for phrase in ("visual task", "daylight", "photometric", "glare", "controls", "mockup", "aiming", "night"):
            self.assertIn(phrase, text)
        self.assertTrue(any("electrical" in item.lower() for item in self.lighting["scope_out"]))
        self.assertTrue(any("universal" in item.lower() and "UGR" in item for item in self.lighting["scope_out"]))

    def test_stage9_machine_mirrors_preserve_ordered_professional_semantics(self):
        lan04 = next(stage for stage in self.landscape["stages"] if stage["stage_id"] == "LAN-04")
        lan09 = next(stage for stage in self.landscape["stages"] if stage["stage_id"] == "LAN-09")
        lgt04 = next(stage for stage in self.lighting["stages"] if stage["stage_id"] == "LGT-04")

        lan04_readback = " ".join(lan04["required_readback"])
        self.assertIn("installation → establishment → mature", lan04_readback)
        self.assertIn("effective 3D rootable soil continuity", lan04_readback)

        lan09_readback = " ".join(lan09["required_readback"])
        for phrase in (
            "pre-action observation → competing explanations",
            "bounded intervention → expected consequence",
            "follow-up readback → retain/reverse/escalate",
        ):
            self.assertIn(phrase, lan09_readback)

        lgt04_readback = " ".join(lgt04["required_readback"])
        for phrase in (
            "initiating input/condition → prerequisites → priority/arbitration",
            "transition/ramp → hold/delay/timeout",
            "fail/degraded state → reset/recovery",
            "simultaneous-input and power/network-restart behavior",
        ):
            self.assertIn(phrase, lgt04_readback)

        for text in (lan04_readback, lan09_readback, lgt04_readback):
            self.assertNotIn("?", text)

    def test_stage10_deep_professional_mechanisms_are_machine_projected(self):
        expected = (
            (self.structural, {
                "SE-SPW4": ("nonlinear/path-dependent/staged-analysis", "fatigue/cyclic"),
                "SE-SPW5": ("nonconformance", "repaired/as-accepted"),
            }),
            (self.mep, {
                "BSP-TECHNICAL": ("part-load/degraded/restart", "multi-source electrical protection/selectivity"),
                "BSP-CONSTRUCTION-CX": ("field deviation", "retest/recommission"),
            }),
            (self.systems, {
                "SYS-04": ("reproducible behavior/evidence set", "as-tested/as-operated"),
                "SYS-05": ("verification coverage", "orphan"),
                "SYS-06": ("reverification scope", "stale evidence"),
            }),
            (self.hcd, {
                "HCD-05": ("service recovery", "consent"),
                "HCD-08": ("longitudinal adoption", "episode-level usability"),
            }),
            (self.interior, {
                "INT-04": ("specialist-controlled detail continuity", "fire/acoustic/waterproofing/MEP"),
                "INT-09": ("in-use aging", "user adaptation"),
            }),
            (self.landscape, {
                "LAN-01": ("seasonal/degraded public-space safety", "diversion/closure"),
                "LAN-04": ("soil investigation", "tree stock/planting/establishment"),
            }),
            (self.lighting, {
                "LGT-04": ("temporal light quality", "blind/shade"),
                "LGT-08": ("measurement uncertainty", "maintenance/re-aim recovery"),
            }),
        )
        for definition, stages in expected:
            stage_map = {stage["stage_id"]: stage for stage in definition["stages"]}
            for stage_id, phrases in stages.items():
                with self.subTest(process_id=definition["process_id"], stage_id=stage_id):
                    stage = stage_map[stage_id]
                    projection = " ".join(
                        stage["required_readback"] + stage["technical_consequences"]
                    )
                    for phrase in phrases:
                        self.assertIn(phrase, projection)

    def test_stage10_machine_mirrors_preserve_ordered_professional_semantics(self):
        stage_sets = {
            "structural": (self.structural, "SE-SPW4"),
            "systems_human": (self.systems, "SYS-02"),
            "systems_coverage": (self.systems, "SYS-05"),
            "systems_change": (self.systems, "SYS-06"),
            "hcd_research": (self.hcd, "HCD-01"),
            "hcd_recovery": (self.hcd, "HCD-05"),
            "landscape": (self.landscape, "LAN-03"),
            "lighting_controls": (self.lighting, "LGT-04"),
            "lighting_field": (self.lighting, "LGT-08"),
        }
        projections = {}
        for key, (definition, stage_id) in stage_sets.items():
            stage = next(stage for stage in definition["stages"] if stage["stage_id"] == stage_id)
            projections[key] = " ".join(stage["required_readback"] + stage["technical_consequences"])

        self.assertIn("global → local model reconciliation", projections["structural"])
        self.assertIn("human ↔ automation allocation", projections["systems_human"])
        self.assertIn("detect → interpret/decide → command/act → confirm/prove → recover", projections["systems_human"])
        self.assertIn("emergent behavior → configuration → state/environment → failure mechanism → proof/observable/evidence", projections["systems_coverage"])
        self.assertIn("changed item → dependent functions/requirements → coupled interfaces/resources → emergent behavior → stale evidence → regression/revalidation set", projections["systems_change"])
        self.assertIn("each method's population", projections["hcd_research"])
        self.assertIn("failure detection → truthful status/ownership → fallback or human handoff → repair/redress → restored-state proof → re-entry", projections["hcd_recovery"])
        self.assertIn("establishment → mature states", projections["landscape"])
        self.assertIn("daylight shade ↔ electric-light shared-control", projections["lighting_controls"])
        self.assertIn("exterior/façade final aim", projections["lighting_field"])

        for text in projections.values():
            self.assertNotIn("?", text)
            self.assertNotIn("\ufffd", text)

    def test_stage10_bodies_retain_specific_non_framework_design_depth(self):
        body_requirements = {
            ROOT / "00-governance/architecture-design-development-process-v1.0.md": (
                "continuous layer transitions",
                "inhabited section",
                "evidence-bounded hypothesis",
            ),
            ROOT / "00-governance/structural-engineering-design-process-v1.0.md": (
                "physically relevant equilibrium path",
                "deterioration path",
                "REPAIR INSTRUCTION ISSUED ≠ REPAIR VERIFIED",
            ),
            ROOT / "00-governance/building-services-mep-design-process-v1.0.md": (
                "controllable authority",
                "hydraulic capacity and hygienic operation",
                "MAINTENANCE CLEARANCE SHOWN ≠ EQUIPMENT REPLACEABLE",
            ),
            ROOT / "00-governance/systems-engineering-design-development-process-v1.0.md": (
                "minimum controlled set needed to reproduce",
                "Build verification coverage as a relation",
                "Derive reverification scope from dependency",
            ),
            ROOT / "00-governance/digital-product-hcd-design-development-process-v1.0.md": (
                "convergence, divergence and missing evidence",
                "service recovery",
                "repeated-use adoption",
            ),
            ROOT / "00-governance/interior-design-development-process-v1.0.md": (
                "specialist-controlled boundary",
                "controlled scene",
                "condition map",
            ),
            ROOT / "00-governance/landscape-architecture-design-development-process-v1.0.md": (
                "public-space safety as changing spatial operation",
                "compliant imported-soil certificate does not prove the installed root zone",
                "IRRIGATION INSTALLED ≠ ROOT-ZONE WATERING WORKS",
            ),
            ROOT / "00-governance/lighting-design-development-process-v1.0.md": (
                "temporal behavior as part of luminous quality",
                "explicit coupled state with electric lighting",
                "measurement supports closure",
            ),
        }
        for path, phrases in body_requirements.items():
            body = path.read_text(encoding="utf-8")
            for phrase in phrases:
                with self.subTest(path=str(path), phrase=phrase):
                    self.assertIn(phrase, body)

    def test_spatial_professional_candidate_bodies_are_substantive_not_stage_shells(self):
        expected = {
            "Interior Design": (
                self.interior,
                ("FF&E", "joinery", "wet", "sample", "substitution", "maintenance"),
            ),
            "Landscape Architecture": (
                self.landscape,
                ("grading", "drainage", "soil", "rooting", "planting", "establishment", "seasonal"),
            ),
            "Lighting Design": (
                self.lighting,
                ("visual task", "daylight", "photometric", "glare", "controls", "aiming", "night readback"),
            ),
        }
        for domain, (definition, required_terms) in expected.items():
            with self.subTest(domain=domain):
                body_path = ROOT / definition["current_definition_ref"]
                self.assertTrue(body_path.exists(), body_path)
                body = body_path.read_text(encoding="utf-8")
                self.assertIn("## 2｜Deep professional decision body", body)
                self.assertIn("## 4｜Professional acceptance matrix", body)
                self.assertGreaterEqual(len(body.splitlines()), 500)
                lower = body.lower()
                for term in required_terms:
                    self.assertIn(term.lower(), lower)

    def test_cross_domain_professional_bodies_retain_deep_decision_substance(self):
        expected = {
            ARCH_BODY: (
                "circulation behavior and bottleneck readback",
                "route and reserve readback",
                "deep fit-back review",
                "environmental decision depth",
                "room-use and ff&e decision depth",
                "value, area and lifecycle decision depth",
                "building-edge interface readback",
            ),
            STRUCT_BODY: (
                "concept analysis and load-model integrity",
                "spatial-coordination engineering depth",
                "technical analysis / checking integrity",
                "foundation / ground-structure coupling depth",
                "connection and local-force transfer depth",
                "production, fabrication and erection-state depth",
                "in-use diagnostic / monitoring depth",
            ),
            MEP_BODY: (
                "controls sequence engineering depth",
                "existing-system reuse / capacity evidence depth",
                "demand, load and diversity decision depth",
                "technical calculation / network-model integrity",
                "installation-readiness and pre-functional quality depth",
                "design-to-tab / measured-network reconciliation",
                "in-use performance-gap diagnosis",
            ),
            SYSTEMS_BODY: (
                "requirement quality and acceptance-architecture depth",
                "behavior, timing and resource-contention depth",
                "trade-study sensitivity and non-compensatory constraint depth",
                "interface compatibility / tolerance and coupling depth",
                "verification / validation experiment-design depth",
                "simulation / analytical evidence credibility depth",
                "anomaly diagnosis and bounded causal inference",
                "validation representativeness and operational-context depth",
                "operational change-detection and reliability evidence depth",
            ),
            HCD_BODY: (
                "research-design and evidence-strength depth",
                "evidence analysis / synthesis depth",
                "task-analysis, workload and error-depth",
                "experience-concept trade and falsification depth",
                "ia / content-structure edge-case depth",
                "interaction concurrency, latency and commit-depth",
                "evaluation-readiness fidelity attacks",
                "evaluation method, severity and interpretation depth",
                "in-use analytics and causal-inference discipline",
            ),
        }
        for path, phrases in expected.items():
            with self.subTest(path=path.name):
                body = path.read_text(encoding="utf-8").lower()
                for phrase in phrases:
                    self.assertIn(phrase.lower(), body)

    def test_machine_definitions_project_deep_readback_not_only_stage_shells(self):
        checks = (
            (self.structural, "SE-SPW4", ("foundation-ground", "connection/local-force-transfer", "model basis")),
            (self.structural, "SE-SPW7", ("competing hypotheses", "monitoring trend")),
            (self.mep, "BSP-TECHNICAL", ("part-load", "controls as trigger")),
            (self.mep, "BSP-CONSTRUCTION-CX", ("tab/balancing", "critical path")),
            (self.systems, "SYS-04", ("common units/frame/timing/tolerance", "stack-up")),
            (self.systems, "SYS-05", ("simulation", "measurement uncertainty")),
            (self.systems, "SYS-08", ("exposure denominator", "data completeness")),
            (self.hcd, "HCD-01", ("unit-of-observation", "repeated mention is not prevalence")),
            (self.hcd, "HCD-05", ("optimistic", "persistence/user-informed")),
            (self.hcd, "HCD-08", ("telemetry event semantics", "confounders")),
            (self.interior, "INT-04", ("datum hierarchy", "site-measure hold point")),
            (self.interior, "INT-08", ("pre-install site readiness", "rework")),
            (self.landscape, "LAN-03", ("blocked/saturated", "hydraulic capacity")),
            (self.landscape, "LAN-04", ("effective 3d rootable", "mature assemblage")),
            (self.lighting, "LGT-02", ("illuminance", "glare/reflection", "spectral")),
            (self.lighting, "LGT-04", ("priority/arbitration", "emergency override")),
            (self.lighting, "LGT-06", ("mockup and calculation", "pre-calibration")),
        )
        for definition, stage_id, terms in checks:
            stage = next(stage for stage in definition["stages"] if stage["stage_id"] == stage_id)
            text = " ".join(stage.get("required_readback", []) + stage.get("technical_consequences", [])).lower()
            with self.subTest(process_id=definition["process_id"], stage_id=stage_id):
                for term in terms:
                    self.assertIn(term.lower(), text)

    def test_stage11_residual_professional_mechanisms_are_machine_projected(self):
        expected = (
            (self.structural, {
                "SE-SPW1": ("mechanism-based inspection/test plan", "anomaly-driven sampling"),
                "SE-SPW4": ("initiating loss → removed function/load → alternate transfer path", "common-mode"),
                "SE-SPW4.5": ("structural state transitions", "release criteria"),
            }),
            (self.mep, {
                "BSP-CONCEPT": ("service-restoration dependency sequence", "common-dependency"),
                "BSP-TECHNICAL": ("process fault, bad measurement", "source → transmission path → receiver", "drainage air-pressure/vent/transient"),
                "BSP-CONSTRUCTION-CX": ("physical maintenance isolation boundary", "accessible isolator does not prove safe isolation"),
            }),
            (self.systems, {
                "SYS-00": ("external service", "system-of-systems common dependencies", "Cybersecurity/IT"),
            }),
            (self.hcd, {
                "HCD-02": ("cognitive demand", "diagnose/resume"),
                "HCD-04": ("orientation/route choice", "Back/Return/recovery"),
                "HCD-05": ("multi-user/shared-object", "conflict/recovery"),
            }),
            (self.interior, {
                "INT-02": ("anthropometric variability", "simultaneous-use"),
                "INT-04": ("joinery/edge/seal/wet-transition", "capillary wetting"),
                "INT-06": ("cleaning/contamination-control", "clean/dirty"),
            }),
            (self.landscape, {
                "LAN-01": ("fall/run-out envelope", "accessible approach/transfer"),
                "LAN-02": ("level-change interface", "wheel/cane/rollover"),
                "LAN-04": ("source population → dispersal/spread path", "escape/invasiveness"),
            }),
            (self.lighting, {
                "LGT-02": ("observer–subject", "facial"),
                "LGT-05": ("source → surface/path → sensitive receptor", "light-trespass"),
                "LGT-09": ("commissioned luminous-control baseline", "configuration-drift"),
            }),
        )
        for definition, stages in expected:
            stage_map = {stage["stage_id"]: stage for stage in definition["stages"]}
            for stage_id, phrases in stages.items():
                with self.subTest(process_id=definition["process_id"], stage_id=stage_id):
                    projection = " ".join(
                        stage_map[stage_id]["required_readback"]
                        + stage_map[stage_id]["technical_consequences"]
                    )
                    for phrase in phrases:
                        self.assertIn(phrase.lower(), projection.lower())
                    self.assertNotIn("?", projection)
                    self.assertNotIn("\ufffd", projection)

    def test_stage11_bodies_retain_specific_residual_design_depth(self):
        body_requirements = {
            ARCH_BODY: (
                "water source → falls/high-low points",
                "datum → tolerance stack → absorption → as-built",
            ),
            STRUCT_BODY: (
                "anomalies expand inspection/test scope",
                "shared/common-mode dependencies",
                "structural state transitions",
            ),
            MEP_BODY: (
                "Sensor / actuator fault-diagnosis depth",
                "source → transmission path → receiver",
                "service-restoration dependency chain",
                "ACCESSIBLE ISOLATOR ≠ SAFE ISOLATION PROVED",
            ),
            SYSTEMS_BODY: (
                "systems of systems",
                "Cybersecurity/IT-owner requirements",
            ),
            HCD_BODY: (
                "what the user must perceive, remember, compare, decide and retain",
                "human-visible coordination state",
                "conditions that most reduce legibility",
            ),
            ROOT / "00-governance/interior-design-development-process-v1.0.md": (
                "simultaneous-use conditions",
                "capillary wetting",
                "cleaning-critical or contamination-sensitive areas",
            ),
            ROOT / "00-governance/landscape-architecture-design-development-process-v1.0.md": (
                "source population → dispersal/spread path",
                "activity/fall/run-out envelope",
            ),
            ROOT / "00-governance/lighting-design-development-process-v1.0.md": (
                "observer–subject relation",
                "source → surface/path → receptor",
                "commissioned luminous-control baseline",
            ),
        }
        for path, phrases in body_requirements.items():
            text = path.read_text(encoding="utf-8")
            with self.subTest(path=str(path)):
                for phrase in phrases:
                    self.assertIn(phrase, text)
                self.assertNotIn("\ufffd", text)

    def test_current_structural_and_mep_definitions_validate(self):
        for definition in self.current_definitions():
            with self.subTest(process_id=definition["process_id"]):
                self.assertEqual(self.validator.validate_payload(definition), [])

    def test_every_current_stage_has_exactly_ten_body_roles(self):
        for definition in self.current_definitions():
            for stage in definition["stages"]:
                with self.subTest(
                    process_id=definition["process_id"], stage_id=stage["stage_id"]
                ):
                    roles = stage["stage_body_contract"]["required_semantic_sections"]
                    self.assertEqual(len(roles), 10)
                    self.assertEqual(len(set(roles)), 10)
                    self.assertEqual(set(roles), EXPECTED_BODY_ROLES)

    def test_current_title_rules_name_stage_identity(self):
        for definition in self.current_definitions():
            for stage in definition["stages"]:
                with self.subTest(
                    process_id=definition["process_id"], stage_id=stage["stage_id"]
                ):
                    title_rule = stage["stage_body_contract"]["title_rule"]
                    self.assertIn(stage["stage_id"], title_rule)
                    self.assertIn(stage["stage_name"], title_rule)

    def test_current_knowledge_mount_rules_keep_canonical_bodies_by_reference(self):
        for definition in self.current_definitions():
            for stage in definition["stages"]:
                with self.subTest(
                    process_id=definition["process_id"], stage_id=stage["stage_id"]
                ):
                    rule = stage["stage_body_contract"]["knowledge_mount_rule"]
                    self.assertIn("Operational Mount", rule)
                    self.assertIn("do not copy canonical knowledge bodies", rule)

    def test_interface_maturity_policy_is_accepted_by_full_and_fallback(self):
        for definition in self.current_definitions():
            with self.subTest(process_id=definition["process_id"]):
                interface_contract = definition["interface_contract"]
                self.assertIn("interface_maturity_policy", interface_contract)
                self.assertNotIn(
                    "required_interface_maturity_to_enter", interface_contract
                )
                self.assertNotIn(
                    "required_interface_maturity_to_close", interface_contract
                )
                self.assertEqual(self.validator.validate_payload(definition), [])
                self.assertEqual(
                    self.validator.validate_fallback_structure(definition), []
                )

    def test_profession_wide_interface_maturity_scalars_are_rejected(self):
        definition = copy.deepcopy(self.structural)
        interface_contract = definition["interface_contract"]
        interface_contract["required_interface_maturity_to_enter"] = "DEFINED"
        interface_contract["required_interface_maturity_to_close"] = "COORDINATED"

        errors = self.validator.validate_payload(definition)
        self.assertTrue(errors)

    def test_interface_maturity_policy_is_required(self):
        definition = copy.deepcopy(self.structural)
        interface_contract = definition["interface_contract"]
        interface_contract.pop("interface_maturity_policy", None)

        self.assertTrue(self.validator.validate_payload(definition))
        fallback_errors = self.validator.validate_fallback_structure(definition)
        self.assertTrue(
            any("interface_maturity_policy" in error for error in fallback_errors),
            fallback_errors,
        )

    def test_fallback_rejects_incomplete_stage_body_semantic_contract(self):
        definition = copy.deepcopy(self.structural)
        definition["stages"][0]["stage_body_contract"][
            "required_semantic_sections"
        ].pop()

        fallback_errors = self.validator.validate_fallback_structure(definition)
        self.assertTrue(
            any("10 semantic responsibilities exactly once" in error for error in fallback_errors),
            fallback_errors,
        )

    def test_stage_definition_requires_native_readback_exit_and_reopen_content(self):
        for key in (
            "required_inputs",
            "required_native_outputs",
            "required_readback",
            "exit_conditions",
            "reopen_triggers",
        ):
            definition = copy.deepcopy(self.structural)
            definition["stages"][0][key] = []
            for errors in (
                self.validator.validate_fallback_structure(definition),
                self.validator.validate_payload(definition),
            ):
                self.assertTrue(
                    any(f"{key} must be a non-empty array" in error for error in errors),
                    (key, errors),
                )

    def test_interface_requirement_close_maturity_cannot_regress_below_entry(self):
        definition = copy.deepcopy(self.structural)
        binding = definition["stages"][2]["interface_binding_requirements"][0]
        binding["required_maturity_to_enter"] = "EXERCISED"
        binding["required_maturity_to_close"] = "DEFINED"
        for errors in (
            self.validator.validate_fallback_structure(definition),
            self.validator.validate_payload(definition),
        ):
            self.assertTrue(
                any("required_maturity_to_close may not be lower" in error for error in errors),
                errors,
            )

    def test_interface_requirement_requires_declared_shared_variables(self):
        definition = copy.deepcopy(self.structural)
        definition["stages"][0]["interface_binding_requirements"][0]["shared_variables"] = []
        for errors in (
            self.validator.validate_fallback_structure(definition),
            self.validator.validate_payload(definition),
            ):
                self.assertTrue(any("shared_variables must be non-empty" in error for error in errors), errors)

    def test_current_use_and_exit_condition_are_orthogonal(self):
        payload = self.validator.make_closed_instance(self.example, "PASS")
        self.assertEqual(payload["current_use_state"], "CURRENT")
        self.assertEqual(payload["process_exit_condition_state"], "SATISFIED")
        self.assertEqual(payload["stage_instances"][0]["current_use_state"], "CURRENT")
        self.assertEqual(payload["stage_instances"][0]["exit_condition_state"], "SATISFIED")
        self.assertEqual(self.validator.validate_payload(payload), [])

    def test_v10_legacy_instance_shape_remains_read_compatible(self):
        payload = copy.deepcopy(self.example)
        payload["schema_version"] = "1.0"
        payload["execution_state"] = "IN_PROGRESS"
        for field in (
            "domain_state",
            "current_use_state",
            "process_exit_condition_state",
            "in_claim_blocking_open_item_count",
        ):
            payload.pop(field, None)
        for stage in payload["stage_instances"]:
            stage["execution_state"] = "IN_PROGRESS"
            for field in (
                "domain_state",
                "current_use_state",
                "stage_body_record",
                "review_bindings",
                "in_claim_blocking_open_item_count",
            ):
                stage.pop(field, None)
        self.assertEqual(self.validator.validate_payload(payload), [])

    def test_v10_legacy_definition_shape_remains_read_compatible(self):
        definition = copy.deepcopy(self.structural)
        definition["schema_version"] = "1.0"
        for stage in definition["stages"]:
            stage.pop("stage_body_contract", None)
            requirements = stage.pop("interface_binding_requirements")
            legacy = []
            for requirement in requirements:
                item = copy.deepcopy(requirement)
                item["interface_binding_id"] = item.pop("requirement_id")
                item["coupling"] = item.pop("coupling_hypothesis")
                item["criticality"] = item.pop("criticality_hypothesis")
                item["native_source_of_truth"] = item.pop(
                    "required_native_source_role"
                )
                item["change_reopen_rule"] = item.pop(
                    "requested_change_reopen_rule"
                )
                legacy.append(item)
            stage["interface_bindings"] = legacy
        self.assertEqual(self.validator.validate_payload(definition), [])

    def test_professional_pass_requires_at_least_one_pass_stage(self):
        payload = self.validator.make_closed_instance(self.example, "PASS")
        payload["stage_instances"][0]["review_verdict"] = "REVISE"
        errors = self.validator.validate_payload(payload)
        self.assertTrue(
            any("requires at least one CURRENT + SATISFIED + PASS stage" in error for error in errors),
            errors,
        )

    def test_stage_pass_requires_review_reference(self):
        payload = self.validator.make_closed_instance(self.example, "PASS")
        payload["stage_instances"][0]["review_refs"] = []
        errors = self.validator.validate_payload(payload)
        self.assertTrue(any("PASS requires review_refs" in error for error in errors), errors)

    def test_current_process_pass_cannot_be_backed_only_by_superseded_pass_stage(self):
        payload = self.validator.make_closed_instance(self.example, "PASS")
        payload["stage_instances"][0]["current_use_state"] = "SUPERSEDED"
        errors = self.validator.validate_payload(payload)
        self.assertTrue(
            any("requires at least one CURRENT + SATISFIED + PASS stage" in error for error in errors),
            errors,
        )

    def test_v11_stage_pass_requires_exact_review_binding(self):
        payload = self.validator.make_closed_instance(self.example, "PASS")
        payload["stage_instances"][0]["review_bindings"] = []
        errors = self.validator.validate_payload(payload)
        self.assertTrue(any("requires exact review_bindings" in error for error in errors), errors)

    def test_v11_stage_pass_review_binding_must_match_native_artifact(self):
        payload = self.validator.make_closed_instance(self.example, "PASS")
        payload["stage_instances"][0]["review_bindings"][0][
            "review_input_artifact_ref"
        ] = "NOT-THE-REVIEWED-NATIVE-ARTIFACT"
        errors = self.validator.validate_payload(payload)
        self.assertTrue(
            any("review_input_artifact_ref must match" in error for error in errors),
            errors,
        )

    def test_v11_stage_pass_rejects_na_native_or_readback_body_roles(self):
        for role in ("NATIVE_OUTPUT_SOURCE_OF_TRUTH", "ACTUAL_READBACK_FINDING"):
            payload = self.validator.make_closed_instance(self.example, "PASS")
            entry = next(
                item
                for item in payload["stage_instances"][0]["stage_body_record"][
                    "section_coverage"
                ]
                if item["semantic_role"] == role
            )
            entry["status"] = "NOT_APPLICABLE_WITH_REASON"
            entry["visible_heading_or_locator"] = None
            entry["reason"] = "synthetic N/A"
            errors = self.validator.validate_payload(payload)
            self.assertTrue(any(role in error for error in errors), (role, errors))

    def test_v11_satisfied_rejects_in_claim_blocker_count(self):
        payload = self.validator.make_closed_instance(self.example, "PASS")
        payload["in_claim_blocking_open_item_count"] = 1
        payload["stage_instances"][0]["in_claim_blocking_open_item_count"] = 1
        errors = self.validator.validate_payload(payload)
        self.assertTrue(
            any("in_claim_blocking_open_item_count=0" in error for error in errors),
            errors,
        )


if __name__ == "__main__":
    unittest.main()
