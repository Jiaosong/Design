# Rhino + Grasshopper Runtime Security Boundary

Status: `ACTIVE FOR BOOTSTRAP / HOST NOT YET CONNECTED`

## Hard rules

1. **Never expose Rhino `StartScriptServer` directly to the public internet.** It is a local execution surface.
2. **Only dispatch allow-listed scripts.** `windows/run_job.ps1` rejects unknown `job_type` values instead of executing arbitrary paths from a job payload.
3. **Do not commit secrets.** Rhino.Compute tokens, API keys, license credentials and tunnel credentials belong in the host secret store / environment, never in GitHub, Notion or Drive.
4. **Do not attach an unrestricted self-hosted runner to the public `Jiaosong/Design` repository.** If GitHub-based remote dispatch is later adopted, use a private control repository or a tightly restricted runner group / environment with trusted branches and explicit approvals.
5. **No evidence promotion by transport.** A successful script dispatch, zero exit code, artifact upload or screenshot is not automatically a design / engineering PASS.
6. **Write receipts before and after side effects.** A future remote bridge must preserve run id, job id, target host, exact script, input hash, output hash, exit state and approval scope.

## Recommended remote bridge sequence

```text
Trusted OLEANDER control request
    -> authenticated bridge
    -> validate Runtime Contract
    -> allow-list job type
    -> create checkpoint
    -> rhinocode -> live Rhino
    -> collect receipt + artifacts
    -> hash outputs
    -> human/evidence gate
    -> optional archive
```

## Public repository constraint

This runtime code may be versioned in the public design repository, but **execution authority must not be inherited from arbitrary pull requests or forks**. Runtime code and runtime credentials are separate concerns.

## Rhino.Compute

If Rhino.Compute is added later:
- keep billing / API credentials outside the repository;
- bind service ports to a protected network or authenticated gateway;
- use Compute for headless solve/batch tasks, not as proof of GUI evidence such as Parameter Viewer screenshots;
- preserve the same Runtime Contract and evidence rules used by the desktop node.
