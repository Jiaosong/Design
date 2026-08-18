# Restore the v1.2 portable source snapshot

The complete 16-page self-contained portable HTML is stored as four base64 text parts to keep the GitHub source recoverable without treating a preview image as the master.

## Reconstruct

```bash
cat part_00.b64 part_01.b64 part_02.b64 part_03.b64 | tr -d '\n' | base64 -d > C04_QINGJIANG_BRAND_SYSTEM_v1_2_PORTABLE.html.gz
gzip -dc C04_QINGJIANG_BRAND_SYSTEM_v1_2_PORTABLE.html.gz > C04_QINGJIANG_BRAND_SYSTEM_v1_2_PORTABLE.html
```

## Expected SHA-256

- gzip snapshot: `a6109436e993a2d7d43508e4ada147770d0c52477be67e160f83f25e1569b4db`
- restored portable HTML: `1611a32846b3bcde6c0460e4cfb77a6f0d24a9c97c08dd9e1c4c10b0237b04f4`
- local full delivery ZIP provenance: `880236f29251184f60a492f7cdd5d2d212168d500f26f4878f96850f0ba8913b`

The portable snapshot contains all 16 numbered brand-system SVG pages inline. Separate responsive identity SVGs and machine-readable tokens are also committed directly in this directory tree.

This proves recoverability/traceability only. It does not prove Design PASS, field validation, operator approval or promotion.
