# OLEANDER Baidu Storage Protocol v0.1

**Status:** CANDIDATE / STORAGE ADAPTER ONLY

## 1. Boundary

The Baidu adapter stores and retrieves bytes. It does not own the semantic state that decides whether those bytes are Current, accepted, validated, kept or promoted.

Hard separations:

`STORAGE COPY != CURRENT AUTHORITY`

`UPLOAD SUCCESS != ARTIFACT READBACK`

`ARTIFACT READBACK != DESIGN KEEP`

`REMOTE AVAILABILITY != PROJECT STATE`

`BAIDU MD5 != OLEANDER SHA256 IDENTITY`

## 2. Storage classes

The recommended Baidu root is `/OLEANDER_VAULT`.

Within a project, the following names are storage classes only:

- `CURRENT/` — remote byte copy of the artifact currently referenced by the owner-native project carrier;
- `MILESTONES/` — retained significant revisions;
- `REVIEW/` — lightweight PDFs, images, SVGs and other remote-review carriers;
- `ARCHIVE/` — historical byte storage.

No folder name can grant OLEANDER authority by itself.

## 3. Artifact binding

Existing OLEANDER artifact/project owners may reference a Baidu replica through the schema in `schemas/oleander-baidu-storage-binding.v0.1.schema.json`.

The binding is a **replica pointer**, not a new artifact registry. Stable artifact identity remains with the existing owner.

Minimum useful relation:

```text
owner-native artifact id / revision / sha256
→ BAIDU_NETDISK replica fsid / path / md5 / size
→ remote availability state
→ replica readback state
```

SHA-256 is retained on the OLEANDER side because the official Baidu MCP reports MD5 for many remote file operations. MD5 may be used as provider readback metadata but does not replace the owner-native digest.

## 4. Mutation policy

Default:

- browse/search/list/meta/quota — allowed inside `/OLEANDER_VAULT`;
- create/copy/move/rename/remote URL/text upload — allowed inside the root;
- operation mutating a `/CURRENT/` storage path — requires explicit `ACK_STORAGE_CURRENT_MUTATION`;
- overwrite semantics — require `ACK_STORAGE_OVERWRITE`;
- delete — disabled by default, and when enabled still requires `ACK_STORAGE_DELETE`;
- share-link creation — unsupported in v0.1 until every fsid can be owner-preflighted to `/OLEANDER_VAULT` before sharing.

These acknowledgements authorize only the named storage operation. They do not satisfy project mutation permission, Design KEEP or Promotion.

## 5. Cross-device use

Remote ChatGPT:

`search/browse/review/manage remote copies → storage receipt`

Local COS:

`owner-native reread → native execution → local readback → optional official stdio upload → provider readback → project owner writeback when authorized`

The official Baidu MCP exposes local-file upload only through its stdio/local implementation. This adapter therefore does not pretend that a remote ChatGPT session can read arbitrary local workstation files.

## 6. Knowledge bodies

`/OLEANDER_VAULT/KNOWLEDGE` may hold large canonical/reference bodies such as PDFs, scans and source archives. The existing Knowledge Registry remains the identity/provenance/KI/OE owner. Storage location never upgrades Knowledge state.
