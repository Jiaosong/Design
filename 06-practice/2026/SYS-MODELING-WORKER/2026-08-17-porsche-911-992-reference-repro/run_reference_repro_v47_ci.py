#!/usr/bin/env python3
"""Execute V47 with the repository's canonical tail-light material key.

This wrapper changes no geometry, targets, gates or receipts. It only maps the mistaken experimental
`rear_light` material lookup to the existing `tail` material key before V47 is compiled.
"""
from pathlib import Path
HERE=Path(__file__).resolve().parent
src=(HERE/'run_reference_repro_v47.py').read_text()
needle="M['rear_light']"
if src.count(needle)!=1:
    raise SystemExit(f'expected exactly one V47 rear_light lookup, found {src.count(needle)}')
src=src.replace(needle,"M['tail']")
ns={'__file__':str(HERE/'run_reference_repro_v47.py'),'__name__':'__main__'}
exec(compile(src,str(HERE/'run_reference_repro_v47.py'),'exec'),ns)
