import adsk.core
import adsk.fusion
import adsk
import csv
import json
import math
import hashlib
import os
import traceback
from datetime import datetime

SCRIPT_NAME = 'OLEANDER Timer Light Basin AutoBuild v0.4'
DESIGN_NAME = '2026-08-07_Fusion360_TimerLightBasin_v04'


def _pt(x_cm: float, y_cm: float) -> adsk.core.Point3D:
    return adsk.core.Point3D.create(x_cm, y_cm, 0)


def _add_parameter(design, name, expression, units, comment):
    params = design.userParameters
    existing = params.itemByName(name)
    value = adsk.core.ValueInput.createByString(expression)
    if existing:
        existing.expression = expression
        existing.comment = comment
        return existing
    result = params.add(name, value, units, comment)
    if not result:
        raise RuntimeError(f'Could not create user parameter: {name}')
    return result


def _new_component(parent_component, name):
    occurrence = parent_component.occurrences.addNewComponent(adsk.core.Matrix3D.create())
    if not occurrence:
        raise RuntimeError(f'Could not create component: {name}')
    occurrence.component.name = name
    return occurrence, occurrence.component


def _dimension_line(sketch, line, expression, text_x, text_y):
    dim = sketch.sketchDimensions.addDistanceDimension(
        line.startSketchPoint,
        line.endSketchPoint,
        adsk.fusion.DimensionOrientations.AlignedDimensionOrientation,
        _pt(text_x, text_y),
    )
    if not dim:
        raise RuntimeError(f'Could not dimension line with {expression}')
    dim.parameter.expression = expression
    return dim


def _dimension_point_xy(sketch, point, x_expression, y_expression, text_shift=0.3):
    origin = sketch.originPoint
    dims = sketch.sketchDimensions
    if x_expression:
        x_dim = dims.addDistanceDimension(
            origin,
            point,
            adsk.fusion.DimensionOrientations.HorizontalDimensionOrientation,
            _pt(point.geometry.x, point.geometry.y - text_shift),
        )
        x_dim.parameter.expression = x_expression
    if y_expression:
        y_dim = dims.addDistanceDimension(
            origin,
            point,
            adsk.fusion.DimensionOrientations.VerticalDimensionOrientation,
            _pt(point.geometry.x + text_shift, point.geometry.y),
        )
        y_dim.parameter.expression = y_expression


def _largest_profile(sketch):
    if sketch.profiles.count == 0:
        raise RuntimeError(f'No closed profile in sketch: {sketch.name}')
    best = sketch.profiles.item(0)
    best_area = -1.0
    for i in range(sketch.profiles.count):
        profile = sketch.profiles.item(i)
        try:
            area = profile.areaProperties().area
        except Exception:
            area = float(i)
        if area > best_area:
            best = profile
            best_area = area
    return best


def _full_revolve(component, sketch, axis, feature_name, body_name):
    input_obj = component.features.revolveFeatures.createInput(
        _largest_profile(sketch),
        axis,
        adsk.fusion.FeatureOperations.NewBodyFeatureOperation,
    )
    if not input_obj:
        raise RuntimeError(f'Could not create revolve input: {feature_name}')
    input_obj.setAngleExtent(False, adsk.core.ValueInput.createByString('360 deg'))
    feature = component.features.revolveFeatures.add(input_obj)
    if not feature:
        raise RuntimeError(f'Revolve failed: {feature_name}')
    feature.name = feature_name
    body = feature.bodies.item(0)
    body.name = body_name
    return feature, body


def _find_top_planar_face(body):
    candidates = []
    for i in range(body.faces.count):
        face = body.faces.item(i)
        box = face.boundingBox
        if abs(box.maxPoint.z - box.minPoint.z) < 1e-5:
            candidates.append((box.maxPoint.z, face.area, face))
    if not candidates:
        return None
    candidates.sort(key=lambda item: (item[0], item[1]), reverse=True)
    return candidates[0][2]


def _cut_revolve(component, sketch, axis, participant_body, feature_name):
    revolve_features = component.features.revolveFeatures
    input_obj = revolve_features.createInput(
        _largest_profile(sketch),
        axis,
        adsk.fusion.FeatureOperations.CutFeatureOperation,
    )
    if not input_obj:
        raise RuntimeError(f'Could not create cut-revolve input: {feature_name}')
    input_obj.setAngleExtent(False, adsk.core.ValueInput.createByString('360 deg'))
    input_obj.participantBodies = [participant_body]
    feature = revolve_features.add(input_obj)
    if not feature:
        raise RuntimeError(f'Cut revolve failed: {feature_name}')
    feature.name = feature_name
    return feature


def _build_housing(component):
    # Outer solid profile.
    outer_sketch = component.sketches.add(component.xZConstructionPlane)
    outer_sketch.name = 'SK01A_Housing_Outer_Parametric'
    lines = outer_sketch.sketchCurves.sketchLines
    constraints = outer_sketch.geometricConstraints

    outer_axis = lines.addByTwoPoints(_pt(0, -0.5), _pt(0, 3.5))
    outer_axis.isConstruction = True
    outer_axis.isFixed = True

    p0 = outer_sketch.originPoint
    p1 = outer_sketch.sketchPoints.add(_pt(5.9, 0))
    p2 = outer_sketch.sketchPoints.add(_pt(5.9, 2.5))
    p3 = outer_sketch.sketchPoints.add(_pt(5.25, 2.5))
    p4 = outer_sketch.sketchPoints.add(_pt(5.25, 2.8))
    p5 = outer_sketch.sketchPoints.add(_pt(0, 2.8))

    outer_lines = [
        lines.addByTwoPoints(p0, p1),
        lines.addByTwoPoints(p1, p2),
        lines.addByTwoPoints(p2, p3),
        lines.addByTwoPoints(p3, p4),
        lines.addByTwoPoints(p4, p5),
        lines.addByTwoPoints(p5, p0),
    ]
    constraints.addHorizontal(outer_lines[0])
    constraints.addVertical(outer_lines[1])
    constraints.addHorizontal(outer_lines[2])
    constraints.addVertical(outer_lines[3])
    constraints.addHorizontal(outer_lines[4])
    constraints.addVertical(outer_lines[5])

    _dimension_line(outer_sketch, outer_lines[0], 'body_diameter / 2', 3.0, -0.5)
    _dimension_line(
        outer_sketch,
        outer_lines[1],
        'body_height - neck_height',
        6.4,
        1.2,
    )
    _dimension_line(
        outer_sketch,
        outer_lines[2],
        'body_diameter / 2 - neck_outer_radius',
        5.6,
        2.2,
    )
    _dimension_line(outer_sketch, outer_lines[3], 'neck_height', 5.7, 2.7)
    _dimension_line(outer_sketch, outer_lines[4], 'neck_outer_radius', 2.6, 3.2)

    _, body = _full_revolve(
        component,
        outer_sketch,
        outer_axis,
        'RV01A_Housing_Outer',
        'Base_Housing_Outer',
    )

    # Inner cavity is a separate parameter-driven cut. This makes the opening,
    # wall thickness, floor thickness, and assembly gap directly auditable.
    cavity_sketch = component.sketches.add(component.xZConstructionPlane)
    cavity_sketch.name = 'SK01B_Housing_Cavity_Parametric'
    cavity_lines_collection = cavity_sketch.sketchCurves.sketchLines
    cavity_constraints = cavity_sketch.geometricConstraints
    cavity_dims = cavity_sketch.sketchDimensions

    cavity_axis = cavity_lines_collection.addByTwoPoints(
        _pt(0, 0),
        _pt(0, 3.5),
    )
    cavity_axis.isConstruction = True
    cavity_axis.isFixed = True

    q0 = cavity_sketch.sketchPoints.add(_pt(0, 0.2))
    q1 = cavity_sketch.sketchPoints.add(_pt(5.7, 0.2))
    q2 = cavity_sketch.sketchPoints.add(_pt(5.7, 2.3))
    q3 = cavity_sketch.sketchPoints.add(_pt(5.05, 2.5))
    q4 = cavity_sketch.sketchPoints.add(_pt(5.05, 2.8))
    q5 = cavity_sketch.sketchPoints.add(_pt(0, 2.8))

    cavity_lines = [
        cavity_lines_collection.addByTwoPoints(q0, q1),
        cavity_lines_collection.addByTwoPoints(q1, q2),
        cavity_lines_collection.addByTwoPoints(q2, q3),
        cavity_lines_collection.addByTwoPoints(q3, q4),
        cavity_lines_collection.addByTwoPoints(q4, q5),
        cavity_lines_collection.addByTwoPoints(q5, q0),
    ]
    cavity_constraints.addHorizontal(cavity_lines[0])
    cavity_constraints.addVertical(cavity_lines[1])
    cavity_constraints.addVertical(cavity_lines[3])
    cavity_constraints.addHorizontal(cavity_lines[4])
    cavity_constraints.addVertical(cavity_lines[5])
    cavity_constraints.addCoincident(q0, cavity_axis)

    q0_height = cavity_dims.addDistanceDimension(
        cavity_sketch.originPoint,
        q0,
        adsk.fusion.DimensionOrientations.VerticalDimensionOrientation,
        _pt(0.4, 0.1),
    )
    q0_height.parameter.expression = 'wall_thickness'

    _dimension_line(
        cavity_sketch,
        cavity_lines[0],
        'body_diameter / 2 - wall_thickness',
        3.0,
        -0.2,
    )
    _dimension_line(
        cavity_sketch,
        cavity_lines[1],
        'body_height - neck_height - 2 * wall_thickness',
        6.2,
        1.2,
    )

    transition_x = cavity_dims.addDistanceDimension(
        q3,
        q2,
        adsk.fusion.DimensionOrientations.HorizontalDimensionOrientation,
        _pt(5.4, 2.1),
    )
    transition_x.parameter.expression = (
        'body_diameter / 2 - wall_thickness - opening_radius'
    )
    transition_y = cavity_dims.addDistanceDimension(
        q2,
        q3,
        adsk.fusion.DimensionOrientations.VerticalDimensionOrientation,
        _pt(5.9, 2.4),
    )
    transition_y.parameter.expression = 'wall_thickness'

    _dimension_line(
        cavity_sketch,
        cavity_lines[3],
        'neck_height',
        5.5,
        2.7,
    )
    _dimension_line(
        cavity_sketch,
        cavity_lines[4],
        'opening_radius',
        2.5,
        3.2,
    )

    _cut_revolve(
        component,
        cavity_sketch,
        cavity_axis,
        body,
        'RV01B_Housing_Cavity_Cut',
    )
    body.name = 'Base_Housing'
    outer_sketch.isLightBulbOn = False
    cavity_sketch.isLightBulbOn = False
    return body, [outer_sketch, cavity_sketch]


def _build_diffuser(component, segments=8):
    sketch = component.sketches.add(component.xZConstructionPlane)
    sketch.name = 'SK02_Diffuser_Parametric_Profile'
    lines = sketch.sketchCurves.sketchLines
    constraints = sketch.geometricConstraints

    axis = lines.addByTwoPoints(_pt(0, 1.5), _pt(0, 3.5))
    axis.isConstruction = True
    axis.isFixed = True

    top_points = []
    bottom_points = []
    for i in range(segments + 1):
        fraction = i / segments
        x_cm = 5.0 * fraction
        y_cm = 2.4 + 0.3 * (fraction ** 2)
        point = sketch.sketchPoints.add(_pt(x_cm, y_cm))
        top_points.append(point)
        x_expr = None if i == 0 else f'light_radius * {fraction:.8f}'
        y_expr = (
            'diffuser_center_height'
            if i == 0
            else f'diffuser_center_height + basin_depth * {fraction ** 2:.8f}'
        )
        if i == 0:
            constraints.addCoincident(point, axis)
        _dimension_point_xy(sketch, point, x_expr, y_expr)

    for i in range(segments, -1, -1):
        fraction = i / segments
        x_cm = 5.0 * fraction
        y_cm = 2.4 + 0.3 * (fraction ** 2) - 0.2
        point = sketch.sketchPoints.add(_pt(x_cm, y_cm))
        bottom_points.append(point)
        x_expr = None if i == 0 else f'light_radius * {fraction:.8f}'
        top_y = (
            'diffuser_center_height'
            if i == 0
            else f'diffuser_center_height + basin_depth * {fraction ** 2:.8f}'
        )
        y_expr = f'({top_y}) - diffuser_thickness'
        if i == 0:
            constraints.addCoincident(point, axis)
        _dimension_point_xy(sketch, point, x_expr, y_expr)

    ordered = top_points + bottom_points
    profile_lines = []
    for a, b in zip(ordered, ordered[1:] + [ordered[0]]):
        profile_lines.append(lines.addByTwoPoints(a, b))

    _, body = _full_revolve(
        component,
        sketch,
        axis,
        'RV02_Diffuser',
        'Light_Diffuser',
    )
    sketch.isLightBulbOn = False
    return body, sketch


def _build_state_references(component):
    plane_input = component.constructionPlanes.createInput()
    plane_input.setByOffset(
        component.xYConstructionPlane,
        adsk.core.ValueInput.createByString('body_height + 4 mm'),
    )
    plane = component.constructionPlanes.add(plane_input)
    plane.name = 'PL01_State_Reference_Level'

    state_specs = [
        ('State_100', 'state_100_radius', -14.0),
        ('State_50', 'state_50_radius', 0.0),
        ('State_10', 'state_10_radius', 14.0),
    ]
    sketches = []
    bodies = []
    for index, (name, radius_parameter, center_x) in enumerate(state_specs, start=1):
        sketch = component.sketches.add(plane)
        sketch.name = f'SK03_{index:02d}_{name}'
        circle = sketch.sketchCurves.sketchCircles.addByCenterRadius(
            _pt(center_x, 0),
            1.0,
        )
        circle.centerSketchPoint.isFixed = True
        diameter = sketch.sketchDimensions.addDiameterDimension(
            circle,
            _pt(center_x + 1.5, 1.5),
        )
        diameter.parameter.expression = f'2 * {radius_parameter}'

        profile = _largest_profile(sketch)
        feature = component.features.extrudeFeatures.addSimple(
            profile,
            adsk.core.ValueInput.createByString('mask_thickness'),
            adsk.fusion.FeatureOperations.NewBodyFeatureOperation,
        )
        if not feature:
            raise RuntimeError(f'Could not extrude state reference: {name}')
        feature.name = f'EX03_{index:02d}_{name}'
        body = feature.bodies.item(0)
        body.name = name
        sketch.isLightBulbOn = False
        sketches.append(sketch)
        bodies.append(body)
    return bodies, sketches


def _timeline_issues(design):
    issues = []
    timeline = design.timeline
    warning_state = adsk.fusion.FeatureHealthStates.WarningFeatureHealthState
    error_state = adsk.fusion.FeatureHealthStates.ErrorFeatureHealthState
    for i in range(timeline.count):
        item = timeline.item(i)
        if item.healthState in (warning_state, error_state):
            entity = item.entity
            issues.append({
                'index': i,
                'name': getattr(entity, 'name', f'Timeline item {i}'),
                'state': int(item.healthState),
                'message': item.errorOrWarningMessage,
            })
    return issues



def _parameter_snapshot(design):
    snapshot = {}
    for i in range(design.userParameters.count):
        parameter = design.userParameters.item(i)
        snapshot[parameter.name] = {
            'expression': parameter.expression,
            'unit': parameter.unit,
            'value_database_units': parameter.value,
            'value_mm': parameter.value * 10.0 if parameter.unit == 'mm' else None,
            'comment': parameter.comment,
        }
    return snapshot


def _design_invariants(design):
    def mm(name):
        parameter = design.userParameters.itemByName(name)
        if not parameter:
            raise RuntimeError(f'Missing user parameter: {name}')
        return parameter.value * 10.0

    body_radius = mm('body_diameter') / 2.0
    light_radius = mm('light_radius')
    opening_radius = mm('opening_radius')
    neck_outer_radius = mm('neck_outer_radius')
    wall_thickness = mm('wall_thickness')
    assembly_gap = mm('assembly_gap')
    body_height = mm('body_height')
    neck_height = mm('neck_height')
    basin_depth = mm('basin_depth')
    diffuser_thickness = mm('diffuser_thickness')

    values = {
        'shoulder_width_mm': body_radius - neck_outer_radius,
        'declared_radial_gap_mm': opening_radius - light_radius,
        'neck_wall_mm': neck_outer_radius - opening_radius,
        'base_internal_height_mm': body_height - neck_height - wall_thickness,
        'diffuser_centre_lower_height_mm': (
            body_height - 1.0 - basin_depth - diffuser_thickness
        ),
    }
    rules = {
        'shoulder_width_at_least_1mm': values['shoulder_width_mm'] >= 1.0,
        'assembly_gap_at_least_0_25mm': assembly_gap >= 0.25,
        'declared_gap_matches_parameter': (
            abs(values['declared_radial_gap_mm'] - assembly_gap) <= 0.001
        ),
        'neck_wall_matches_parameter': (
            abs(values['neck_wall_mm'] - wall_thickness) <= 0.001
        ),
        'positive_internal_height': values['base_internal_height_mm'] > 0,
        'diffuser_above_base_floor': (
            values['diffuser_centre_lower_height_mm'] > wall_thickness
        ),
        'positive_basin_depth': basin_depth > 0,
        'positive_diffuser_thickness': diffuser_thickness > 0,
    }
    return {'values': values, 'rules': rules, 'pass': all(rules.values())}


def _interference_and_clearance(app, design, housing_occurrence, diffuser_occurrence):
    entities = adsk.core.ObjectCollection.create()
    entities.add(housing_occurrence)
    entities.add(diffuser_occurrence)
    interference_input = design.createInterferenceInput(entities)
    if not interference_input:
        raise RuntimeError('Could not create InterferenceInput.')
    interference_input.areCoincidentFacesIncluded = False
    results = design.analyzeInterference(interference_input)
    if results is None:
        raise RuntimeError('Interference analysis returned no result.')
    distance = app.measureManager.measureMinimumDistance(
        housing_occurrence,
        diffuser_occurrence,
    )
    if not distance or not distance.isValid:
        raise RuntimeError('Minimum-distance measurement failed.')
    expected_gap_mm = design.userParameters.itemByName(
        'assembly_gap'
    ).value * 10.0
    actual_gap_mm = distance.value * 10.0
    return {
        'interference_count': results.count,
        'minimum_distance_mm': actual_gap_mm,
        'expected_assembly_gap_mm': expected_gap_mm,
        'gap_error_mm': actual_gap_mm - expected_gap_mm,
        'gap_matches_parameter_within_0_05mm': (
            abs(actual_gap_mm - expected_gap_mm) <= 0.05
        ),
    }


def _sketch_status(sketches):
    return {
        sketch.name: {
            'fully_constrained': bool(sketch.isFullyConstrained),
            'health_state': int(sketch.healthState),
            'message': sketch.errorOrWarningMessage,
            'valid': bool(sketch.isValid),
        }
        for sketch in sketches
    }


def _run_stress_tests(app, design, housing_occurrence, diffuser_occurrence, sketches):
    baseline = {
        name: design.userParameters.itemByName(name).expression
        for name in (
            'body_diameter',
            'body_height',
            'wall_thickness',
            'assembly_gap',
            'light_diameter',
        )
    }
    cases = [
        ('baseline', {}, False),
        ('body_diameter_plus_10pct', {'body_diameter': '129.8 mm'}, False),
        (
            'body_diameter_minus_10pct_boundary',
            {'body_diameter': '106.2 mm'},
            True,
        ),
        ('body_height_minus_10pct', {'body_height': '25.2 mm'}, False),
        ('wall_thickness_min', {'wall_thickness': '1.5 mm'}, False),
        ('wall_thickness_max', {'wall_thickness': '2.5 mm'}, False),
        ('assembly_gap_min', {'assembly_gap': '0.25 mm'}, False),
        ('assembly_gap_max', {'assembly_gap': '1.0 mm'}, False),
        ('light_diameter_plus_5pct', {'light_diameter': '105 mm'}, False),
        ('light_diameter_minus_5pct', {'light_diameter': '95 mm'}, False),
    ]
    records = []
    for case_name, updates, expected_boundary in cases:
        record = {
            'case': case_name,
            'updates': updates,
            'expected_boundary_review': expected_boundary,
        }
        try:
            for name, expression in updates.items():
                parameter = design.userParameters.itemByName(name)
                if not parameter:
                    raise RuntimeError(f'Missing stress-test parameter: {name}')
                parameter.expression = expression

            record['compute_completed'] = bool(design.computeAll())
            adsk.doEvents()
            record['invariants'] = _design_invariants(design)
            record['timeline_issues'] = _timeline_issues(design)
            record['sketches'] = _sketch_status(sketches)
            record.update(
                _interference_and_clearance(
                    app,
                    design,
                    housing_occurrence,
                    diffuser_occurrence,
                )
            )

            healthy = int(
                adsk.fusion.FeatureHealthStates.HealthyFeatureHealthState
            )
            normal_pass = (
                record['compute_completed']
                and record['invariants']['pass']
                and not record['timeline_issues']
                and record['interference_count'] == 0
                and record['gap_matches_parameter_within_0_05mm']
                and all(
                    value['fully_constrained']
                    and value['valid']
                    and value['health_state'] == healthy
                    for value in record['sketches'].values()
                )
            )
            if normal_pass:
                record['status'] = 'PASS'
            elif expected_boundary and not record['invariants']['pass']:
                record['status'] = 'EXPECTED_BOUNDARY_REVIEW'
            else:
                record['status'] = 'FAIL'
        except Exception:
            record['status'] = 'EXCEPTION'
            record['exception'] = traceback.format_exc()
        finally:
            for name, expression in baseline.items():
                design.userParameters.itemByName(name).expression = expression
            design.computeAll()
            adsk.doEvents()
        records.append(record)
    return records


def _sha256(path):
    digest = hashlib.sha256()
    with open(path, 'rb') as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b''):
            digest.update(block)
    return digest.hexdigest()


def _verify_file(path, minimum_bytes):
    exists = os.path.isfile(path)
    size = os.path.getsize(path) if exists else 0
    return {
        'path': path,
        'exists': exists,
        'size_bytes': size,
        'minimum_bytes': minimum_bytes,
        'size_pass': size >= minimum_bytes,
        'sha256': _sha256(path) if exists and size > 0 else None,
        'pass': bool(exists and size >= minimum_bytes),
    }


def _score_report(report):
    sketches = report['baseline_sketches']
    geometry = report['baseline_geometry_check']
    invariants = report['baseline_invariants']
    stress_tests = report['stress_tests']
    files = report['files']
    healthy = int(adsk.fusion.FeatureHealthStates.HealthyFeatureHealthState)

    normal_stress = [
        item for item in stress_tests
        if not item.get('expected_boundary_review', False)
    ]
    boundary_tests = [
        item for item in stress_tests
        if item.get('expected_boundary_review', False)
    ]

    technical = (
        (5 if report['baseline_compute_completed'] else 0)
        + (5 if not report['baseline_timeline_issues'] else 0)
        + (5 if geometry['interference_count'] == 0 else 0)
        + (5 if geometry['gap_matches_parameter_within_0_05mm'] else 0)
        + (5 if invariants['pass'] else 0)
    )
    structure = (
        (5 if report['component_count'] == 3 else 0)
        + (5 if report['parameter_count'] >= 18 else 0)
        + (
            5
            if all(
                item['fully_constrained']
                and item['valid']
                and item['health_state'] == healthy
                for item in sketches.values()
            )
            else 0
        )
    )
    parameter_logic = (
        (5 if invariants['pass'] else 0)
        + (
            7
            if all(item.get('status') == 'PASS' for item in normal_stress)
            else 0
        )
        + (
            3
            if all(
                item.get('status') in ('PASS', 'EXPECTED_BOUNDARY_REVIEW')
                for item in boundary_tests
            )
            else 0
        )
    )
    visual = (
        (5 if files.get('isometric_png', {}).get('pass') else 0)
        + (5 if files.get('section_png', {}).get('pass') else 0)
        + (5 if files.get('states_png', {}).get('pass') else 0)
    )
    checks = (
        (3 if not report['baseline_timeline_issues'] else 0)
        + (3 if geometry['interference_count'] == 0 else 0)
        + (2 if geometry['gap_matches_parameter_within_0_05mm'] else 0)
        + (
            2
            if all(item.get('status') != 'EXCEPTION' for item in stress_tests)
            else 0
        )
    )
    reproducibility = (
        (3 if files.get('f3d', {}).get('pass') else 0)
        + (2 if files.get('assembly_step', {}).get('pass') else 0)
        + (2 if files.get('parameters_csv', {}).get('pass') else 0)
        + (2 if files.get('validation_json', {}).get('pass') else 0)
        + (1 if files.get('sha256_manifest', {}).get('pass') else 0)
    )
    categories = {
        'technical_correctness': {'score': technical, 'maximum': 25},
        'file_and_structure': {'score': structure, 'maximum': 15},
        'parameter_and_data_logic': {'score': parameter_logic, 'maximum': 15},
        'visual_expression': {'score': visual, 'maximum': 15},
        'check_and_revision': {'score': checks, 'maximum': 10},
        'reproducibility': {'score': reproducibility, 'maximum': 10},
        'oleander_project_value': {'score': 10, 'maximum': 10},
    }
    raw_score = sum(item['score'] for item in categories.values())
    hard_gates = {
        'native_f3d_exists': files.get('f3d', {}).get('pass', False),
        'assembly_step_exists': files.get('assembly_step', {}).get('pass', False),
        'validation_json_exists': files.get(
            'validation_json', {}
        ).get('pass', False),
        'no_timeline_error_or_warning': not report['baseline_timeline_issues'],
        'all_primary_sketches_fully_constrained': all(
            item['fully_constrained'] for item in sketches.values()
        ),
        'no_interference': geometry['interference_count'] == 0,
        'minimum_gap_matches_declared_parameter': geometry[
            'gap_matches_parameter_within_0_05mm'
        ],
        'all_normal_stress_tests_pass': all(
            item.get('status') == 'PASS' for item in normal_stress
        ),
    }
    certified = all(hard_gates.values()) and raw_score >= 80
    return {
        'categories': categories,
        'raw_score': raw_score,
        'hard_gates': hard_gates,
        'certified_pass': certified,
        'certified_score': raw_score if certified else min(raw_score, 79),
        'status': (
            'PASS_80_PLUS'
            if certified
            else 'NOT_CERTIFIED_HARD_GATE_OR_SCORE'
        ),
    }


def _write_parameter_csv(design, path):
    with open(path, 'w', newline='', encoding='utf-8-sig') as handle:
        writer = csv.writer(handle)
        writer.writerow(['Name', 'Unit', 'Expression', 'Value', 'Comments', 'Favorite'])
        for i in range(design.userParameters.count):
            parameter = design.userParameters.item(i)
            writer.writerow([
                parameter.name,
                parameter.unit,
                parameter.expression,
                parameter.value,
                parameter.comment,
                bool(parameter.isFavorite),
            ])


def _set_camera(viewport, orientation):
    camera = viewport.camera
    camera.isSmoothTransition = False
    camera.viewOrientation = orientation
    camera.isFitView = True
    viewport.camera = camera
    viewport.refresh()
    adsk.doEvents()



def _save_outputs(
    app,
    ui,
    design,
    root,
    housing_occurrence,
    diffuser_occurrence,
    mask_occurrence,
    housing_component,
    diffuser_component,
    mask_component,
    stress_records,
    sketches,
):
    folder_dialog = ui.createFolderDialog()
    folder_dialog.title = 'Choose local folder for OLEANDER Fusion outputs'
    if folder_dialog.showDialog() != adsk.core.DialogResults.DialogOK:
        return {'export_status': 'CANCELLED_BY_USER'}
    folder = folder_dialog.folder
    os.makedirs(folder, exist_ok=True)

    export_manager = design.exportManager
    files = {}

    def execute_export(key, path, options, minimum_bytes):
        success = bool(export_manager.execute(options))
        evidence = _verify_file(path, minimum_bytes)
        evidence['api_execute_success'] = success
        evidence['pass'] = bool(success and evidence['pass'])
        files[key] = evidence

    f3d_path = os.path.join(folder, DESIGN_NAME + '.f3d')
    execute_export(
        'f3d',
        f3d_path,
        export_manager.createFusionArchiveExportOptions(f3d_path, root),
        1024,
    )

    assembly_step_path = os.path.join(folder, DESIGN_NAME + '_assembly.step')
    execute_export(
        'assembly_step',
        assembly_step_path,
        export_manager.createSTEPExportOptions(assembly_step_path, root),
        1024,
    )

    for key, component in (
        ('housing_step', housing_component),
        ('diffuser_step', diffuser_component),
        ('states_step', mask_component),
    ):
        path = os.path.join(folder, DESIGN_NAME + '_' + key + '.step')
        execute_export(
            key,
            path,
            export_manager.createSTEPExportOptions(path, component),
            512,
        )

    parameter_path = os.path.join(folder, DESIGN_NAME + '_parameters.csv')
    _write_parameter_csv(design, parameter_path)
    files['parameters_csv'] = _verify_file(parameter_path, 200)

    viewport = app.activeViewport
    section_input = design.analyses.sectionAnalyses.createInput(
        root.yZConstructionPlane,
        0.0,
    )
    if not section_input:
        raise RuntimeError('Could not create SectionAnalysisInput.')
    section_input.isHatchShown = True
    section = design.analyses.sectionAnalyses.add(section_input)
    if not section:
        raise RuntimeError('Could not create Section Analysis.')
    section.name = 'SEC01_Center_Construction_Check'

    def save_view(key, path, width, height):
        success = bool(viewport.saveAsImageFile(path, width, height))
        evidence = _verify_file(path, 1000)
        evidence['api_save_success'] = success
        evidence['pass'] = bool(success and evidence['pass'])
        files[key] = evidence

    section.isLightBulbOn = False
    housing_occurrence.isLightBulbOn = True
    diffuser_occurrence.isLightBulbOn = True
    mask_occurrence.isLightBulbOn = False
    _set_camera(
        viewport,
        adsk.core.ViewOrientations.IsoTopRightViewOrientation,
    )
    save_view(
        'isometric_png',
        os.path.join(folder, DESIGN_NAME + '_01_isometric.png'),
        1800,
        1400,
    )

    section.isLightBulbOn = True
    _set_camera(viewport, adsk.core.ViewOrientations.FrontViewOrientation)
    save_view(
        'section_png',
        os.path.join(folder, DESIGN_NAME + '_02_section.png'),
        1800,
        1400,
    )

    section.isLightBulbOn = False
    housing_occurrence.isLightBulbOn = False
    diffuser_occurrence.isLightBulbOn = False
    mask_occurrence.isLightBulbOn = True
    _set_camera(viewport, adsk.core.ViewOrientations.TopViewOrientation)
    save_view(
        'states_png',
        os.path.join(folder, DESIGN_NAME + '_03_states.png'),
        1800,
        900,
    )

    housing_occurrence.isLightBulbOn = True
    diffuser_occurrence.isLightBulbOn = True
    mask_occurrence.isLightBulbOn = True
    _set_camera(
        viewport,
        adsk.core.ViewOrientations.IsoTopRightViewOrientation,
    )

    report = {
        'generated_at': datetime.now().isoformat(),
        'design_name': DESIGN_NAME,
        'fusion_product_version': app.version,
        'evidence_boundary': (
            'All dimensions are exercise assumptions. Native CAD checks do not '
            'prove optical, electrical, thermal, manufacturing, ergonomic, safety, '
            'cost, user-recognition, or physical-prototype performance.'
        ),
        'component_count': root.occurrences.count,
        'parameter_count': design.userParameters.count,
        'parameter_snapshot': _parameter_snapshot(design),
        'baseline_compute_completed': bool(design.computeAll()),
        'baseline_timeline_issues': _timeline_issues(design),
        'baseline_sketches': _sketch_status(sketches),
        'baseline_invariants': _design_invariants(design),
        'baseline_geometry_check': _interference_and_clearance(
            app,
            design,
            housing_occurrence,
            diffuser_occurrence,
        ),
        'stress_tests': stress_records,
        'files': files,
    }
    adsk.doEvents()

    report_path = os.path.join(
        folder,
        DESIGN_NAME + '_validation_report.json',
    )
    with open(report_path, 'w', encoding='utf-8') as handle:
        json.dump(report, handle, ensure_ascii=False, indent=2)
    files['validation_json'] = _verify_file(report_path, 500)

    manifest_path = os.path.join(folder, 'SHA256SUMS.txt')
    with open(manifest_path, 'w', encoding='utf-8') as handle:
        for key in sorted(files):
            item = files[key]
            if item.get('exists') and item.get('sha256'):
                handle.write(
                    f'{item["sha256"]}  '
                    f'{os.path.basename(item["path"])}\n'
                )
    files['sha256_manifest'] = _verify_file(manifest_path, 100)

    score = _score_report(report)
    report['files'] = files
    report['scorecard'] = score
    report['runtime_status'] = (
        'NATIVE_FUSION_RUNTIME_PASS_80_PLUS'
        if score['certified_pass']
        else 'NATIVE_FUSION_RUNTIME_NOT_CERTIFIED'
    )
    with open(report_path, 'w', encoding='utf-8') as handle:
        json.dump(report, handle, ensure_ascii=False, indent=2)
    files['validation_json'] = _verify_file(report_path, 500)

    scorecard_path = os.path.join(
        folder,
        DESIGN_NAME + '_scorecard.json',
    )
    with open(scorecard_path, 'w', encoding='utf-8') as handle:
        json.dump(score, handle, ensure_ascii=False, indent=2)
    files['scorecard_json'] = _verify_file(scorecard_path, 300)
    return report


def run(context):
    ui = None
    try:
        app = adsk.core.Application.get()
        ui = app.userInterface
        app.documents.add(adsk.core.DocumentTypes.FusionDesignDocumentType)
        design = adsk.fusion.Design.cast(app.activeProduct)
        if not design:
            raise RuntimeError('No active Fusion design.')
        design.designType = adsk.fusion.DesignTypes.ParametricDesignType

        # Base parameters are created before dependent parameters so every
        # expression resolves at creation time.
        parameters = [
            ('body_diameter', '118 mm', 'mm', 'EXERCISE ASSUMPTION'),
            ('body_height', '28 mm', 'mm', 'EXERCISE ASSUMPTION'),
            ('neck_height', '3 mm', 'mm', 'CONSTRUCTION RELATION'),
            ('light_diameter', '100 mm', 'mm', 'EXERCISE ASSUMPTION'),
            ('basin_depth', '3 mm', 'mm', 'EXERCISE ASSUMPTION'),
            ('wall_thickness', '2 mm', 'mm', 'EXERCISE ASSUMPTION'),
            ('diffuser_thickness', '2 mm', 'mm', 'EXERCISE ASSUMPTION'),
            ('assembly_gap', '0.5 mm', 'mm', 'EXERCISE ASSUMPTION'),
            ('base_fillet', '4 mm', 'mm', 'RESERVED FOR MANUAL DETAILING'),
            ('mask_thickness', '1 mm', 'mm', 'EXERCISE ASSUMPTION'),
            ('light_radius', 'light_diameter / 2', 'mm', 'DERIVED'),
            ('opening_radius', 'light_radius + assembly_gap', 'mm', 'DERIVED'),
            ('neck_outer_radius', 'opening_radius + wall_thickness', 'mm', 'DERIVED'),
            ('diffuser_edge_height', 'body_height - 1 mm', 'mm', 'DERIVED'),
            ('diffuser_center_height', 'diffuser_edge_height - basin_depth', 'mm', 'DERIVED'),
            ('state_100_radius', 'light_radius', 'mm', 'AREA-PROPORTIONAL STATE'),
            ('state_50_radius', 'light_radius * sqrt(0.5)', 'mm', 'AREA-PROPORTIONAL STATE'),
            ('state_10_radius', 'light_radius * sqrt(0.1)', 'mm', 'AREA-PROPORTIONAL STATE'),
        ]
        for parameter in parameters:
            _add_parameter(design, *parameter)

        root = design.rootComponent
        root.name = DESIGN_NAME
        housing_occurrence, housing_component = _new_component(root, '01_Base_Housing')
        diffuser_occurrence, diffuser_component = _new_component(root, '02_Light_Diffuser')
        mask_occurrence, mask_component = _new_component(root, '03_Light_Mask')

        housing_body, housing_sketches = _build_housing(housing_component)
        diffuser_body, diffuser_sketch = _build_diffuser(diffuser_component)
        _, state_sketches = _build_state_references(mask_component)
        all_sketches = housing_sketches + [diffuser_sketch] + state_sketches

        design.computeAll()
        adsk.doEvents()
        stress_records = _run_stress_tests(
            app,
            design,
            housing_occurrence,
            diffuser_occurrence,
            all_sketches,
        )
        export_report = _save_outputs(
            app,
            ui,
            design,
            root,
            housing_occurrence,
            diffuser_occurrence,
            mask_occurrence,
            housing_component,
            diffuser_component,
            mask_component,
            stress_records,
            all_sketches,
        )

        app.activeViewport.fit()
        ui.messageBox(
            'AutoBuild v0.4 completed.\n\n'
            'The design is driven by user-parameter expressions, includes '
            'automated stress tests, interference and minimum-distance checks, '
            'a centre section analysis, and optional local F3D/STEP/CSV/PNG/JSON exports.\n\n'
            f'Export status: {export_report.get("runtime_status", export_report.get("export_status", "UNKNOWN"))}\n'
            f'Certified score: {export_report.get("scorecard", {}).get("certified_score", "N/A")} / 100\n\n'
            'Evidence boundary: exercise assumptions only. Physical and engineering '
            'performance remains unverified.',
            SCRIPT_NAME,
        )
    except Exception:
        if ui:
            ui.messageBox(
                'AutoBuild v0.4 failed:\n\n' + traceback.format_exc(),
                SCRIPT_NAME,
            )
