from runtime.blender_bridge.oleander_blender_bridge import make_ole_object
from validation.validation_runner import run_basic_checks


def test_object_binding():
    obj = make_ole_object(
        "OLE-GEO-0001",
        "surface_component",
        {"purpose": "test"},
        {"system": "Blender"},
    )
    checks = run_basic_checks(obj)
    assert all(item["result"] == "PASS" for item in checks)
