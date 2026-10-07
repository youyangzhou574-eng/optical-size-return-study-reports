"""V41 actual layout candidates; native preflight only, never a solver launcher."""
import copy
import csv
import hashlib
import importlib.util
import json
import math
from pathlib import Path
from shapely import Polygon, affinity, box, union_all

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]


def module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    obj = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(obj)
    return obj


GEOM = module('existing_geometry', ROOT / 'evidence/pillar_x_pilot_authorized_prepare_20261001_02/authorized_prepare.py')
SCREEN = module('existing_screen', ROOT / 'evidence/pillar_screen35_rt10_local_prepare_20261007_01/screen35_prepare.py')
UNION = module('existing_union', ROOT / 'evidence/pillar_control_volume_feasibility_20261002_01/control_audit.py')
ROLES = ['R_WATER', 'T_WATER', 'PDMS_BASE_MIDDLE', 'FIXED_INTERNAL_PILLAR_MIDDLE_CORE',
         'FIXED_INTERNAL_PILLAR_NEAR_TOP_CORE', 'FIXED_INTERNAL_PILLAR_SIDE_WATER']


def start_allowed(human, native, resource, identity):
    return all(x is True for x in (human, native, resource, identity))


def geometric_pieces(side, px, py):
    audit = json.loads((ROOT / 'evidence/a2_preflight_20260930/geometry/periodic_geometry_audit.json').read_text(encoding='utf-8-sig'))
    record = audit['cases'][f'P{side:g}_H09']
    parents = [Polygon(v) for v in record['full_parent_core_vertices_um']]
    extended = box(-px / 2, -py / 2, px / 2, py / 2).buffer(.035, join_style='mitre')
    pieces = {}
    for parent in parents:
        shape = parent.buffer(.125, join_style='mitre')
        for ix in (-1, 0, 1):
            for iy in (-1, 0, 1):
                p = affinity.translate(shape, ix * px, iy * py).intersection(extended)
                if not p.is_empty and p.area >= 1e-14:
                    pieces[p.normalize().wkb] = p
    return list(pieces.values()), parents


def difference_domain(container, excluded):
    zs = sorted({container[4], container[5]} | {b[i] for b in excluded for i in (4, 5)})
    slabs = []
    outer = box(container[0], container[2], container[1], container[3])
    for z0, z1 in zip(zs, zs[1:]):
        if z0 < container[4] or z1 > container[5]:
            continue
        cover = union_all([box(b[0], b[2], b[1], b[3]) for b in excluded if b[4] <= z0 and b[5] >= z1])
        slabs.extend(r + [z0, z1] for r in UNION.rectangles(outer.difference(cover)))
    return UNION.partition_union(slabs)


def audit_domains(domains):
    material = [b for name, bs in domains.items() if name != 'C' for b in bs]
    partition = UNION.partition_union(material)
    total = UNION.volume(material)
    balances, divergence = [], []
    for name, prisms in domains.items():
        fs = UNION.union_faces(prisms)
        balances.extend(abs(sum(f['sign'] * f['area'] for f in fs if f['axis'] == a)) for a in 'xyz')
        for axis in 'xyz':
            divergence.append(abs(sum(f['position'] * f['sign'] * f['area'] for f in fs if f['axis'] == axis) - UNION.volume(prisms)))
    return {'volume_partition_error_um3': abs(total - UNION.volume(domains['C'])),
            'max_surface_balance_um2': max(balances), 'max_divergence_error_um3': max(divergence),
            'no_integration_overlap': abs(total - UNION.volume(partition)) < 1e-8}


def canonical_faces(domains):
    # Arrange only 2D boundary patches. No full 3D coordinate/owner array.
    planes = {}
    for name, prisms in domains.items():
        for f in UNION.union_faces(prisms):
            planes.setdefault((f['axis'], f['position']), []).append((name, f))
    result = []
    for (axis, position), fs in sorted(planes.items()):
        coords0 = sorted({f['tangent_bounds'][i] for _, f in fs for i in (0, 1)})
        coords1 = sorted({f['tangent_bounds'][i] for _, f in fs for i in (2, 3)})
        groups = {}
        for a0, a1 in zip(coords0, coords0[1:]):
            for b0, b1 in zip(coords1, coords1[1:]):
                x, y = (a0 + a1) / 2, (b0 + b1) / 2
                owners = tuple(sorted((name, f['sign']) for name, f in fs
                                      if f['tangent_bounds'][0] < x < f['tangent_bounds'][1]
                                      and f['tangent_bounds'][2] < y < f['tangent_bounds'][3]))
                if owners:
                    groups.setdefault(owners, []).append(box(a0, b0, a1, b1))
        for owners, cells in sorted(groups.items()):
            for bounds in UNION.rectangles(union_all(cells)):
                key = [axis, position] + bounds
                signs = dict(owners)
                if signs.get('C', 0) != sum(v for k, v in owners if k != 'C'):
                    raise ValueError('C/U/D/W face identity is not closed')
                result.append({'name': f'COMBO_FACE_{len(result) + 1:03d}', 'key': tuple(key),
                               'axis': axis, 'position_um': position, 'tangent_bounds_um': bounds,
                               'owners': [{'domain': n, 'sign': s} for n, s in owners],
                               'native_coordinates_pending': True})
    return result


def build_model(side):
    if type(side) not in (int, float) or side not in (1.5, 3.0):
        raise ValueError('Only original full P15 and P30 cells are authorized')
    plan = SCREEN.make_plan(side)
    plan['geometry_halo_um'] = .035
    geometry = GEOM.periodic_geometry(side, .035)
    plan['case'] = ('P15' if side == 1.5 else 'P30') + '_X_COMBO35_A10_M500'
    px, py = plan['solver_period_um']
    cell = box(-px / 2, -py / 2, px / 2, py / 2)
    pieces, parents = geometric_pieces(side, px, py)
    if len(pieces) != geometry['piece_counts'][-1]:
        raise ValueError('True wrapped target pieces mismatch geometry builder')
    regions = []
    for i, shape in enumerate(pieces, 1):
        x0, y0, x1, y1 = shape.bounds
        bounds = [max(-px / 2, x0 - .080), min(px / 2, x1 + .080),
                  max(-py / 2, y0 - .080), min(py / 2, y1 + .080), .075, 9.175]
        regions.append({'name': f'COMBO_E_PILLAR_{i:03d}', 'bounds_um': bounds})
    regions += [{'name': 'COMBO_E_FLAT', 'bounds_um': [-px / 2, px / 2, -py / 2, py / 2, -.1, .175]},
                {'name': 'COMBO_E_BOTTOM', 'bounds_um': [-px / 2, px / 2, -py / 2, py / 2, -10.1, -9.9]}]
    u = UNION.partition_union([r['bounds_um'] for r in regions])
    c = [-px / 2, px / 2, -py / 2, py / 2, -10.35, 9.475]
    d = [-px / 2, px / 2, -py / 2, py / 2, -9.9, -.1]
    domains = {'C': [c], 'U_UPPER': [b for b in u if b[4] > -1],
               'U_BOTTOM': [b for b in u if b[5] < -9], 'D': [d], 'W': difference_domain(c, u + [d])}
    covered_xy = union_all([box(b[0], b[2], b[1], b[3]) for b in domains['U_UPPER'] if b[5] == 9.175])
    missing = union_all(pieces).intersection(cell).difference(covered_xy).area
    interior = [p for p in parents if cell.covers(p.buffer(.205, join_style='mitre'))]
    if not interior:
        raise ValueError('No fully interior logical pillar for declared plots/time points')
    core = min(interior, key=lambda p: (p.centroid.distance(cell.centroid), p.centroid.x, p.centroid.y))
    x, y = core.centroid.x, core.centroid.y
    edge = core.exterior.interpolate(core.exterior.length * .5)
    vx, vy = edge.x - x, edge.y - y
    scale = math.hypot(vx, vy)
    water = [edge.x + .25 * vx / scale, edge.y + .25 * vy / scale, 4.5]
    if union_all(pieces).covers(box(water[0] - .001, water[1] - .001, water[0] + .001, water[1] + .001)):
        raise ValueError('Declared water point still inside coating')
    xyz = [[0, 0, -11.15], [0, 0, 9.825], [0, 0, -5], [x, y, 4.5], [x, y, 8.85], water]
    model = {'plan': plan, 'geometry': {k: v for k, v in geometry.items() if k != 'lsf'},
             'geometry_lsf': geometry['lsf'], 'E_regions': regions, 'domains': domains,
             'faces': canonical_faces(domains), 'point_roles': [{'role': role, 'xyz_um': p, 'native_coordinates_pending': True}
                                                                for role, p in zip(ROLES, xyz)],
             'fixed_plot_core_vertices_um': list(core.exterior.coords),
             'coverage': {'pillar_xy_missing_area_um2': missing, 'flat_and_bottom_full_period': True,
                          'deep_PDMS_pure_geometric_domain': True, 'native_Yee_coverage_verified': False},
             'resources': {'MPI_threads': [4, 1], 'native_phase_PASS': False, 'allocation_upper_bound_pending': True},
             'native_solver_ready': False, 'full_volume_closure': 'FULL_VOLUME_CLOSURE_NOT_MEASURED',
             'native_face_snapping_and_index_detail_blocks_pending': True}
    check = audit_domains(domains)
    if missing > 1e-9 or not check['no_integration_overlap'] or max(check[k] for k in check if k != 'no_integration_overlap') > 1e-8:
        raise ValueError('Local control-domain geometry failed')
    model['domain_audit'] = check
    return model


def n(value):
    return format(value * 1e-6, '.17g')


def spectral_settings(lines, field=False):
    lines.extend(['set("override global monitor settings",1);', 'set("sample spacing","custom");',
                  'set("custom frequency samples",c/500e-9);', 'set("apodization","None");'])
    for comp in ('Ex', 'Ey', 'Ez', 'Hx', 'Hy', 'Hz', 'Px', 'Py', 'Pz'):
        lines.append(f'set("output {comp}",{int(field and comp.startswith("E"))});')
    lines.append(f'set("output power",{int(not field)});')


def compose(model):
    p = model['plan']
    script = SCREEN.compose(p, model['geometry_lsf'])
    script = script.split(f'save("{p["case"]}_candidate_input.fsp");')[0]
    lines = [script, '# Nominal control faces: native snap/reopen is a mandatory later input gate.']
    for region in model['E_regions']:
        b = region['bounds_um']
        lines += ['addpower;', f'set("name","{region["name"]}");', 'set("monitor type","3D");']
        for i, axis in enumerate('xyz'):
            lines += [f'set("{axis} min",{n(b[2*i])});set("{axis} max",{n(b[2*i+1])});',
                      f'set("down sample {axis}",1);']
        lines.append('set("spatial interpolation","none");')
        spectral_settings(lines, field=True)
    for face in model['faces']:
        axis = face['axis']; tangent = [a for a in 'xyz' if a != axis]
        b = face['tangent_bounds_um']
        lines += ['addpower;', f'set("name","{face["name"]}");', f'set("monitor type","2D {axis.upper()}-normal");',
                  f'set("{axis}",{n(face["position_um"])});', 'set("spatial interpolation","nearest mesh cell");']
        for i, a in enumerate(tangent):
            lines += [f'set("{a} min",{n(b[2*i])});set("{a} max",{n(b[2*i+1])});', f'set("down sample {a}",1);']
        spectral_settings(lines)
    for point in model['point_roles']:
        lines += ['addtime;', f'set("name","TIME_{point["role"]}");', 'set("monitor type","Point");']
        for axis, v in zip('xyz', point['xyz_um']):
            lines.append(f'set("{axis}",{n(v)});')
        lines += ['set("start time",0);', 'set("min sampling per cycle",ceil(350e-9/c/getnamed("FDTD","dt")));',
                  'if(get("down sample time")!=1) { error("TIME_POINT_NOT_EVERY_DT"); }']
        for comp in ('Ex', 'Ey', 'Ez', 'Hx', 'Hy', 'Hz'):
            lines.append(f'set("output {comp}",{int(comp.startswith("E"))});')
    # Tiny persistent runtime index witnesses share the CAD-detail audit locations.
    probe = (ROOT / 'evidence/pillar_p30_screen35_parallel_user_20261007_01/representation_reopen.lsf').read_text(encoding='ascii')
    probe = probe.replace('load("draft_candidate_input.fsp");', '')
    probe = probe.replace('monitors={', 'flux_names={').replace('monitors{j}', 'flux_names{j}')
    if p['side_um'] == 1.5:
        probe = probe.replace('bounds(j,1));', 'bounds(j,1)*0.5);').replace('bounds(j,2));', 'bounds(j,2)*0.5);')
        probe = probe.replace('bounds(j,3));', 'bounds(j,3)*0.5);').replace('bounds(j,4));', 'bounds(j,4)*0.5);')
    witness = ['addindex;set("name","COMBO_INDEX_FLAT_WITNESS");set("monitor type","2D Z-normal");',
               'set("x min",-.2e-6);set("x max",.2e-6);set("y min",-.2e-6);set("y max",.2e-6);set("z",115e-9);',
               'set("spatial interpolation","none");set("down sample X",1);set("down sample Y",1);',
               'set("record conformal mesh when possible",1);set("override global monitor settings",1);',
               'set("sample spacing","custom");set("custom frequency samples",c/500e-9);']
    lines += witness
    lines += ['resource_readback=struct;', 'resource_readback.native_processes=getresource("FDTD",1,"processes");',
              'resource_readback.native_threads=getresource("FDTD",1,"threads");',
              'resource_readback.requested_MPI_processes=4;resource_readback.requested_threads=1;',
              'resource_readback.four_MPI_extra_memory_verified=0;',
              'jsonsave("resource_configuration_readback.json",resource_readback);',
              f'save("{p["case"]}_candidate_input.fsp");', 'report=runsystemcheck;',
              f'jsonsave("{p["case"]}_cpu_memory_report.json",report);', 'axes=struct;',
              'axes.x=getresult("FDTD","x");axes.y=getresult("FDTD","y");axes.z=getresult("FDTD","z");',
              f'jsonsave("{p["case"]}_native_mesh_axes.json",axes);',
              'nominal=struct;nominal.native_input_released=0;nominal.face_snapping_pending=1;',
              'nominal.dt=getnamed("FDTD","dt");', f'nominal.E_count={len(model["E_regions"])};',
              f'nominal.face_count={len(model["faces"])};nominal.time_count=6;nominal.small_index_count=1;',
              f'jsonsave("{p["case"]}_layout_readback.json",nominal);', probe]
    return '\n'.join(lines) + '\n'


def write_new(path, value, binary=False):
    if binary:
        with path.open('xb') as f:
            f.write(value)
    else:
        with path.open('x', encoding='ascii', newline='\n') as f:
            json.dump(value, f, indent=2, ensure_ascii=True, allow_nan=False)
            f.write('\n')


def main():
    auth = json.loads((ROOT / 'evidence/pillar_v41_user_release_stop_old_20261007_01/human_authorization.json').read_text(encoding='utf-8-sig'))
    if auth.get('approved_v41_primary_package') is not True or auth.get('approved_original_P15_P30_full_cells') is not True:
        raise ValueError('Explicit v41 primary human release missing')
    stop = json.loads((ROOT / 'evidence/pillar_v41_user_release_stop_old_20261007_01/stop02_resume_local_init/receipt.json').read_text(encoding='utf-8-sig'))
    if stop.get('query_ok') is not True or stop.get('exact_old_input_engines_after') != 0:
        raise ValueError('Old-case cancellation not confirmed')
    out = HERE / 'prepared01'
    out.mkdir(exist_ok=False)
    receipts = []
    for side in (1.5, 3.0):
        model = build_model(side)
        script = compose(model).encode('ascii')
        case = model['plan']['case']
        write_new(out / (case + '_native_build_audit.lsf'), script, True)
        del model['geometry_lsf']
        model['LSF_sha256'] = hashlib.sha256(script).hexdigest().upper()
        write_new(out / (case + '_monitor_plan.json'), model)
        with (out / (case + '_face_owners.csv')).open('x', encoding='ascii', newline='') as f:
            w = csv.writer(f);w.writerow(['monitor', 'normal_axis', 'position_um', 't0min_um', 't0max_um', 't1min_um', 't1max_um', 'domain', 'outward_sign'])
            for face in model['faces']:
                for owner in face['owners']:
                    w.writerow([face['name'], face['axis'], face['position_um'], *face['tangent_bounds_um'], owner['domain'], owner['sign']])
        receipts.append({'case': case, 'E_regions': len(model['E_regions']), 'control_faces': len(model['faces']),
                         'time_points': 6, 'runtime_small_index': 1, 'LSF_sha256': model['LSF_sha256'], 'domain_audit': model['domain_audit']})
    receipt = {'state': 'TWO_ACTUAL_S35_LAYOUT_CANDIDATES_READY_FOR_NATIVE_AUDIT_NOT_SOLVER_RELEASE',
               'cases': receipts, 'new_remote_sessions': 0, 'new_CAD': 0, 'new_MPI': 0,
               'native_coordinate_and_thin_layer_and_resource_gates': 'PENDING', 'old_case_stop_confirmed': True,
               'no_automatic_fallback': True, 'native_face_snapping_and_CAD_index_blocks_still_required': True}
    write_new(out / 'preparation_receipt.json', receipt)
    print(json.dumps(receipt))


if __name__ == '__main__':
    main()
