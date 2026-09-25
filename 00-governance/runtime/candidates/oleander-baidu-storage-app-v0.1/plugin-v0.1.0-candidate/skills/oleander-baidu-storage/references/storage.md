# Storage rules

## Authority

The Baidu app owns byte-storage operations only.

It consumes but does not own:

- Project State;
- Current artifact identity;
- Control Cards / execution checkpoints;
- Knowledge identity / KI / OE;
- Design KEEP / professional review;
- Promotion and synchronization authority.

## Root

Default allowed root: `/OLEANDER_VAULT`.

Do not browse or mutate outside it through this Skill.

## Remote review

Prefer lightweight review carriers for remote conversation:

- PDF;
- PNG/JPEG preview;
- SVG;
- small JSON/text;
- bounded model export where needed.

Native masters can remain `LOCAL_REQUIRED` while the remote session continues design review and steering.

## Risk controls

- read/search/list/meta/quota: normal;
- create/copy/remote upload: bounded write;
- move/rename: verify source/destination and affected storage class;
- overwrite: explicit acknowledgement;
- `/CURRENT/` mutation: explicit acknowledgement and owner-native project reread when project semantics are affected;
- delete: disabled by default;
- share: unsupported in v0.1 until fsid ownership can be proven inside the configured storage root before the side effect.

## Authentication boundary

Never put a Baidu access token in this plugin package, a chat message, a manifest committed to Git, or an MCP URL stored in the ZIP. Authentication is supplied by the deployed server's secret store or by a future standards-compliant OAuth connection.

