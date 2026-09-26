# OLEANDER Runtime Provider Spikes

This directory implements the candidate provider-neutral runtime seam. It does not register a new Current runtime or provider authority.

## Run

```powershell
python 00-governance/runtime/runtime_provider_spikes/run_runtime_provider_benchmark.py --pretty
```

To exercise optional Python providers from an isolated environment:

```powershell
python 00-governance/runtime/runtime_provider_spikes/run_runtime_provider_benchmark.py `
  --provider-python D:\path\to\venv\Scripts\python.exe `
  --pretty
```

DeepSeek Harness is pinned to `@deepseek-ai/dsh@0.1.5-rc.3` for this spike. Microsoft Agent Framework and PydanticAI+Temporal versions are pinned in [requirements-provider-smoke.txt](requirements-provider-smoke.txt). Missing optional dependencies return HOLD rather than causing the provider-neutral contract itself to be treated as invalid.

## What the benchmark proves

- one action envelope can be evaluated identically across providers;
- OLEANDER Action Guard runs before provider approval;
- provider approval may narrow but not widen permission;
- CONTINUE / RESUME / RECOVER remain distinct intents;
- PARTIAL remains PARTIAL;
- sensitive read-only disclosure can still be blocked;
- provider events are scrubbed of project-authority fields;
- the contract shim never mutates Project State;
- the same project/decision/artifact identities survive a provider switch.

## What it does not prove

The native smoke probes do not establish production readiness, model quality, real CAD/Figma/Blender authoring parity, long-running provider durability, or external-user value. Those are explicit next-stage evidence requirements in the generated benchmark receipt.
