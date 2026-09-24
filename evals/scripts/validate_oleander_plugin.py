#!/usr/bin/env python3
"""Validate the candidate OLEANDER plugin's installable file graph."""
import json
import re
from pathlib import Path

repo = Path(__file__).resolve().parents[1]
plugin = repo / "plugins" / "oleander-design"
manifest = json.loads((plugin / "plugin.json").read_text(encoding="utf-8"))
market = json.loads((repo / ".agents" / "plugins" / "marketplace.json").read_text(encoding="utf-8"))
assert manifest["$schema"] == "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json"
assert manifest["name"] == "oleander-design"
assert re.fullmatch(r"\d+\.\d+\.\d+", manifest["version"])
interface = manifest["extensions"]["com.openai"]["interface"]
assert interface["displayName"] and interface["defaultPrompt"]
assert "apps" not in manifest["extensions"]["com.openai"], "No MCP mapping is packaged yet"
entries = [x for x in market["plugins"] if x["name"] == manifest["name"]]
assert len(entries) == 1
entry = entries[0]
assert entry["policy"]["installation"] == "AVAILABLE"
assert entry["source"]["source"] == "local"
source = (repo / entry["source"]["path"]).resolve()
assert source == plugin.resolve(), "Marketplace source must resolve to this plugin root"
skill = plugin / "skills" / "oleander-session" / "SKILL.md"
body = skill.read_text(encoding="utf-8")
assert re.match(r"^---\nname: oleander-session\ndescription: .+\n---\n", body)
refs = re.findall(r"\]\((references/[^)]+)\)", body)
assert refs, "No bundled execution guide"
for ref in refs:
    target = (skill.parent / ref).resolve()
    assert target.is_relative_to(plugin.resolve()) and target.is_file(), ref
guide = (skill.parent / "references" / "execution.md").read_text(encoding="utf-8")
for requirement in ("task_id", "authority fingerprint", "actual readback", "claim ceiling", "Next allowed action"):
    assert requirement.lower() in guide.lower(), requirement
print("OLEANDER plugin packaging graph: PASS (live installation and model execution not proven)")
