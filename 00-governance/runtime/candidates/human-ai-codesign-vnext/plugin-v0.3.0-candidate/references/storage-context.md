# Storage / Context Routing v0.2

The Session Kernel routes to existing stores; it owns none of them.

## One rule

`IDENTITY / AUTHORITY / ROLE → RESOLVE EXISTING LOCATOR → WRITE ONLY THROUGH EXISTING OWNER`.

Never create a plugin-owned `projects/`, `state/`, `checkpoints/`, `latest/` or `final/` tree as a second source of truth.

## What survives where

| Need | Owner | Kernel behavior |
| --- | --- | --- |
| conversational scratch | ephemeral session | reconstruct later from Current |
| resumable frontier | Execution Receipt / Control Card / Project State by existing precedence | write only when its persistence trigger applies |
| design/project decision | existing project/design owner | write there and read back |
| native artifact | resolved workface/native owner | keep logical identity and representation role |
| preview/readback | project derivative/readback role | never reverse authority over native master |
| durable production binary | PAP | independent verification when triggered |
| framework/plugin implementation | canonical OLEANDER repo/Skill owner | never copy live project state into plugin package |

## Representation roles

`SOURCE / NATIVE / CANONICAL / PREVIEW / PACKAGE / READBACK / RECEIPT / TEMP_TEST / PRESENTATION`.

Newest/prettiest is not Current. PNG/render/PPT is not automatically native design authority.

## Save intent

- `保存进度 / 下次继续` → existing continuation carrier only if trigger applies;
- `保存这个设计` → resolved active workface/role;
- `保存为 candidate` → stable identity/revision/status/parent binding;
- durable release binary → PAP;
- plugin/framework change → canonical framework/plugin source, never project folder.

Default migration behavior is `LOCATOR_ONLY_NO_MOVE`. Never reorganize a mature project just to satisfy plugin folder conventions.

