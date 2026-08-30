# WebGL Fragment Normal Output Witness

Status: candidate L7 runtime evidence on PR #468.

This witness reuses the existing non-axis-aligned standard/mirrored tangent-space source. It does not create a second geometry authority.

Execution chain:

`Blender 5.2 source → GLB tangent/normal/UV/w + embedded normal map → Three r179 GLTFLoader → diagnostic WebGL vertex/fragment shader → RGBA8 render target → readRenderTargetPixels → direction/readback Gate`

The diagnostic fragment shader reconstructs:

`B = w * cross(N,T)`

`P = normalize(T*q.x + B*q.y + N*q.z)`

and encodes `P` to RGB. Standard and mirrored-UV objects must remain measurably different after real fragment-shader execution.

Boundaries:

- proves only the tested diagnostic shader and WebGL/SwiftShader framebuffer carrier;
- does not prove hardware GPU/driver parity;
- does not prove the full Three `MeshStandardMaterial` PBR shader implementation;
- constant normal texture does not prove mip/filter/anisotropic behavior;
- does not promote Design KEEP.
