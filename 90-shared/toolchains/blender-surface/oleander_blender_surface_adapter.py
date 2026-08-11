#!/usr/bin/env python3
"""OLEANDER Blender Surface System adapter.

Purpose:
- Resolve the globally active Surface System at execution time.
- Freeze exact version/hashes into each render manifest.
- Bind project material roles to shared archetypes/recipes.
- Keep project CMF color separate from surface/process response.

Evidence boundary: all unmeasured numeric appearance seeds are visualization hypotheses.
"""
from __future__ import annotations
import hashlib, json, os
from pathlib import Path


def _sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()


def resolve_surface_system(job: dict, project_root: Path | None = None) -> dict:
    cfg = job.get('surface_system', {})
    env_name = cfg.get('home_env', 'OLEANDER_SURFACE_SYSTEM_HOME')
    home = Path(os.environ.get(env_name, cfg.get('fallback_home', '/mnt/data/oleander_surface_system'))).resolve()
    manifest_path = home / cfg.get('active_manifest', 'ACTIVE.json')
    manifest = json.loads(manifest_path.read_text(encoding='utf-8'))
    version = manifest['active_version']

    components = manifest['components']
    arch_path = home / components['material_process_archetypes']['path']
    recipe_path = home / components['texture_node_recipes']['path']
    archetypes = json.loads(arch_path.read_text(encoding='utf-8'))
    recipes = json.loads(recipe_path.read_text(encoding='utf-8'))

    binding_path_raw = cfg.get('project_binding')
    if not binding_path_raw:
        raise RuntimeError('Surface System enabled but project_binding is missing')
    binding_path = Path(binding_path_raw)
    if not binding_path.is_absolute() and project_root:
        binding_path = project_root / binding_path
    binding_path = binding_path.resolve()
    binding = json.loads(binding_path.read_text(encoding='utf-8'))

    snapshot = {
        'system_name': manifest.get('system_name'),
        'resolved_version': version,
        'resolution_mode': cfg.get('resolution_mode', 'FOLLOW_ACTIVE_AND_RECORD_SNAPSHOT'),
        'active_manifest': str(manifest_path),
        'active_manifest_sha256': _sha256(manifest_path),
        'archetypes_path': str(arch_path),
        'archetypes_sha256': _sha256(arch_path),
        'recipes_path': str(recipe_path),
        'recipes_sha256': _sha256(recipe_path),
        'project_binding': str(binding_path),
        'project_binding_sha256': _sha256(binding_path),
        'source_status': manifest.get('source_status', {}),
        'evidence_boundary': manifest.get('evidence_boundary'),
    }
    return {
        'home': home,
        'manifest': manifest,
        'archetypes': archetypes['archetypes'],
        'recipes': recipes['recipes'],
        'binding': binding,
        'snapshot': snapshot,
    }


def _set_input(node, names, value):
    if isinstance(names, str):
        names = [names]
    for name in names:
        if name in node.inputs:
            node.inputs[name].default_value = value
            return node.inputs[name]
    return None


def _feature_scale_object_coords(feature_size_mm: float, source_units_to_meters: float) -> float:
    source_unit_mm = source_units_to_meters * 1000.0
    mm = max(float(feature_size_mm), 1e-6)
    return source_unit_mm / mm


def _noise_node(nt, vector_socket, label: str, feature_mm: float, source_units_to_meters: float, detail=2.0):
    n = nt.nodes.new('ShaderNodeTexNoise')
    n.name = label
    n.label = f'{label} | ~{feature_mm:g} mm | Surface System'
    _set_input(n, 'Scale', _feature_scale_object_coords(feature_mm, source_units_to_meters))
    _set_input(n, 'Detail', float(detail))
    nt.links.new(vector_socket, n.inputs['Vector'])
    return n


def _wave_node(nt, vector_socket, label: str, feature_mm: float, source_units_to_meters: float, rings=False):
    w = nt.nodes.new('ShaderNodeTexWave')
    w.name = label
    w.label = f'{label} | ~{feature_mm:g} mm | Surface System'
    w.wave_type = 'RINGS' if rings else 'BANDS'
    if rings:
        try: w.rings_direction = 'Z'
        except Exception: pass
    else:
        try: w.bands_direction = 'X'
        except Exception: pass
    _set_input(w, 'Scale', _feature_scale_object_coords(feature_mm, source_units_to_meters))
    _set_input(w, 'Distortion', 3.0)
    _set_input(w, 'Detail', 3.0)
    nt.links.new(vector_socket, w.inputs['Vector'])
    return w


def _offset_signal(nt, signal, amplitude: float, x: float, y: float):
    mul = nt.nodes.new('ShaderNodeMath'); mul.operation = 'MULTIPLY'; mul.location = (x, y)
    mul.inputs[1].default_value = float(amplitude) * 2.0
    nt.links.new(signal, mul.inputs[0])
    add = nt.nodes.new('ShaderNodeMath'); add.operation = 'ADD'; add.location = (x + 150, y)
    add.inputs[1].default_value = -float(amplitude)
    nt.links.new(mul.outputs[0], add.inputs[0])
    return add.outputs[0]


def _resolve_role_spec(surface_ctx: dict, mask: str) -> dict:
    binding = surface_ctx['binding']['roles'][mask]
    spec = {}
    archetype_id = binding.get('archetype_id')
    if archetype_id:
        if archetype_id not in surface_ctx['archetypes']:
            raise KeyError(f'Unknown Surface System archetype {archetype_id} for {mask}')
        spec.update(surface_ctx['archetypes'][archetype_id])
    recipe_id = binding.get('recipe_id')
    recipe = None
    if recipe_id:
        if recipe_id not in surface_ctx['recipes']:
            raise KeyError(f'Unknown Surface System recipe {recipe_id} for {mask}')
        recipe = surface_ctx['recipes'][recipe_id]
    spec.update(binding.get('appearance_overrides', {}))
    spec['_archetype_id'] = archetype_id
    spec['_recipe_id'] = recipe_id
    spec['_recipe'] = recipe
    spec['_binding'] = binding
    return spec


def build_surface_material(bpy, material_name: str, mask: str, linear_rgba, surface_ctx: dict, source_units_to_meters: float):
    """Build one project material from the active shared Surface System."""
    spec = _resolve_role_spec(surface_ctx, mask)
    binding = spec['_binding']
    recipe = spec['_recipe']

    mat = bpy.data.materials.get(material_name) or bpy.data.materials.new(material_name)
    mat.use_nodes = True
    nt = mat.node_tree
    nt.nodes.clear()
    out = nt.nodes.new('ShaderNodeOutputMaterial'); out.name = 'OL_SURFACE_OUTPUT'; out.location = (720, 0)
    bs = nt.nodes.new('ShaderNodeBsdfPrincipled'); bs.name = 'OL_BASE_OPTICAL_MODEL'; bs.location = (430, 40)
    _set_input(bs, 'Base Color', linear_rgba)

    rough = float(spec.get('roughness_base', spec.get('base_roughness', 0.5)))
    _set_input(bs, 'Roughness', rough)
    optical = spec.get('optical_model', 'DIELECTRIC')
    metallic = float(spec.get('metallic_visible_surface', 1.0 if optical == 'METAL_CONDUCTOR' else 0.0))
    _set_input(bs, 'Metallic', metallic)
    _set_input(bs, ['Transmission Weight', 'Transmission'], float(spec.get('transmission', spec.get('transmission_weight', 0.0))))
    _set_input(bs, ['Coat Weight', 'Clearcoat'], float(spec.get('coat_weight', 0.0)))
    _set_input(bs, ['Coat Roughness', 'Clearcoat Roughness'], float(spec.get('coat_roughness', 0.25)))
    _set_input(bs, ['Anisotropic IOR Level', 'Anisotropic'], float(spec.get('anisotropy', 0.0)))
    nt.links.new(bs.outputs['BSDF'], out.inputs['Surface'])

    applied = {'roughness_base': rough, 'metallic': metallic, 'micro_signals': [], 'micro_bump': None}

    if binding.get('microstructure_enabled', False) and recipe:
        tc = nt.nodes.new('ShaderNodeTexCoord'); tc.name = 'OL_COORDINATES'; tc.location = (-1100, 30)
        mapping = nt.nodes.new('ShaderNodeMapping'); mapping.name = 'OL_SCALE_DIRECTION'; mapping.location = (-900, 30)
        nt.links.new(tc.outputs['Object'], mapping.inputs['Vector'])
        signals = []
        for idx, level in enumerate(('macro','meso','micro')):
            layer = recipe.get(level)
            if not layer:
                continue
            gen = layer.get('generator','NOISE')
            feature = float(layer.get('feature_size_mm', 1.0))
            if gen == 'NOISE':
                n = _noise_node(nt, mapping.outputs['Vector'], f'OL_{level.upper()}_NOISE', feature, source_units_to_meters, detail=2.0 + idx*0.5)
                sig = n.outputs['Fac']
            elif 'WAVE_RINGS' in gen:
                n = _wave_node(nt, mapping.outputs['Vector'], f'OL_{level.upper()}_RINGS', feature, source_units_to_meters, rings=True)
                sig = n.outputs.get('Color') or n.outputs.get('Fac')
            elif 'WAVE' in gen:
                n = _wave_node(nt, mapping.outputs['Vector'], f'OL_{level.upper()}_BANDS', feature, source_units_to_meters, rings=False)
                sig = n.outputs.get('Color') or n.outputs.get('Fac')
            else:
                applied['micro_signals'].append({'level':level,'generator':gen,'status':'NOT_APPLIED_UNDEFINED_PRODUCTION_CONSTRUCTION'})
                continue
            amp = float(layer.get('roughness_amplitude', layer.get('amplitude', recipe.get('roughness_amplitude', 0.0))))
            role = layer.get('role','')
            if 'ROUGHNESS' in role and amp > 0:
                signals.append((sig, amp, level, gen, feature))
            applied['micro_signals'].append({'level':level,'generator':gen,'feature_size_mm':feature,'roughness_amplitude':amp,'status':'APPLIED' if ('ROUGHNESS' in role and amp > 0) else 'SIGNAL_BUILT_NOT_ROUGHNESS'})

        if signals:
            base = nt.nodes.new('ShaderNodeValue'); base.name='OL_ROUGHNESS_BASE'; base.outputs[0].default_value = rough; base.location=(-250,220)
            current = base.outputs[0]
            for i,(sig,amp,level,gen,feature) in enumerate(signals):
                off = _offset_signal(nt, sig, amp, -500 + i*20, 180 - i*120)
                add = nt.nodes.new('ShaderNodeMath'); add.operation='ADD'; add.location=(20+i*80,180-i*80)
                nt.links.new(current, add.inputs[0]); nt.links.new(off, add.inputs[1]); current = add.outputs[0]
            clamp = nt.nodes.new('ShaderNodeClamp'); clamp.name='OL_ROUGHNESS_CLAMP'; clamp.location=(260,180)
            nt.links.new(current, clamp.inputs['Value']); nt.links.new(clamp.outputs['Result'], bs.inputs['Roughness'])

            bump_strength = float(recipe.get('bump_strength', 0.0))
            micro = recipe.get('micro') or {}
            bump_strength = max(bump_strength, float(micro.get('bump_strength', 0.0)))
            if bump_strength > 0 and binding.get('micro_bump_enabled', True):
                bump_source = signals[-1][0]
                bump = nt.nodes.new('ShaderNodeBump'); bump.name='OL_MICRO_BUMP'; bump.location=(250,-170)
                _set_input(bump,'Strength',bump_strength)
                _set_input(bump,'Distance',float(binding.get('bump_distance_m',0.00003)))
                nt.links.new(bump_source,bump.inputs['Height'])
                if 'Normal' in bs.inputs: nt.links.new(bump.outputs['Normal'],bs.inputs['Normal'])
                applied['micro_bump']={'strength':bump_strength,'distance_m':float(binding.get('bump_distance_m',0.00003))}

    mat['OLEANDER_SURFACE_SYSTEM_VERSION'] = surface_ctx['snapshot']['resolved_version']
    mat['OLEANDER_SURFACE_MASK'] = mask
    mat['OLEANDER_SURFACE_ARCHETYPE'] = spec.get('_archetype_id') or 'PROJECT_FALLBACK'
    mat['OLEANDER_SURFACE_RECIPE'] = spec.get('_recipe_id') or 'NONE'
    mat['OLEANDER_SURFACE_EVIDENCE'] = binding.get('evidence','VISUALIZATION_HYPOTHESIS')
    return mat, {'mask':mask,'archetype_id':spec.get('_archetype_id'),'recipe_id':spec.get('_recipe_id'),'binding_evidence':binding.get('evidence'),'process_status':binding.get('process_status'),'applied':applied}
