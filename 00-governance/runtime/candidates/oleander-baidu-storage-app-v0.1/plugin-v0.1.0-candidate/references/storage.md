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
- delete/share: disabled by default.
