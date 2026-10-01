"""Offline planning arithmetic only; no CAD, remoting, process control, or solve."""
import csv
import hashlib
import json
import math
from pathlib import Path

GIB = 1024 ** 3
C = 299792458
ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent / 'forecast02'


def gib(value):
    return value / GIB


def field_bytes(points, frequencies, components):
    if min(points, frequencies, components) <= 0:
        raise ValueError('Positive point, frequency and component counts required')
    return points * frequencies * components * 16


def nodes(span_um, step_um):
    if min(span_um, step_um) <= 0:
        raise ValueError('Positive span and step required')
    return math.ceil(span_um / step_um - 1e-10) + 2


def zone_nodes(zones, lower, upper):
    cells = 0
    for lo, hi, step in zones:
        width = min(hi, upper) - max(lo, lower)
        if width > 0:
            cells += math.ceil(width / step - 1e-10)
    return cells + 2


def refine(values, ratio):
    if not 0 < ratio <= .75:
        raise ValueError('Fine/base ratio must not exceed 0.75')
    return [value * ratio for value in values]


def engine_bytes(points, bytes_per_point):
    return points * bytes_per_point


def cfl_dt(dx_um, dy_um, dz_um):
    return .99 / (C * math.sqrt(sum(1 / (v * 1e-6) ** 2
                                   for v in (dx_um, dy_um, dz_um))))


def runtime_seconds(points, iterations, nodes_per_second):
    return points * iterations / nodes_per_second


def release_gate(peak_gib, cap_gib, *, cad_verified, human_start_approved):
    return bool(cad_verified and human_start_approved and peak_gib <= cap_gib)


def read_hashed(relative_path, expected_hash):
    path = ROOT / relative_path
    raw = path.read_bytes()
    actual = hashlib.sha256(raw).hexdigest().upper()
    if actual != expected_hash:
        raise ValueError('Existing source evidence hash changed: ' + relative_path)
    return raw, actual


def main():
    if OUT.exists():
        raise FileExistsError('Forecast output exists; verify, do not overwrite')
    inputs = {
        'P15': ('evidence/a2_preflight_20260930/pillar_geometry_draft01/P15_H09_geometry_audit.json',
                '42061B484C81C2AF50C8448504352576C73979178E3F6D2DC5F56114D05F6669'),
        'P30': ('evidence/a2_preflight_20260930/pillar_geometry_draft01/P30_H09_geometry_audit.json',
                'BB9AEF720156AED21112DE8D9165E2BA03FF2C654B016F12119A5F47D302D4F5'),
    }
    sources = {}
    geometries = {}
    for case, (path, sha) in inputs.items():
        raw, actual = read_hashed(path, sha)
        geometries[case] = json.loads(raw.decode('utf-8-sig'))
        sources[case] = {'path': path, 'sha256': actual, 'bytes': len(raw)}
    log_path = 'evidence/a2_preflight_20260930/F0_D3_autoshutoff_20261001/closeout_review06_01/freeze01/p0.redacted.txt'
    log, log_sha = read_hashed(log_path, 'B483E147923ABED58EA6B2FEDFD069E86E9BB26D226069CEC2531FD774CB3A88')
    if b'70.6856 Mnodes/s' not in log or b'8265 iterations' not in log:
        raise ValueError('Historical throughput evidence does not match')
    sources['D3_log'] = {'path': log_path, 'sha256': log_sha, 'bytes': len(log)}

    baseline = dict(native_grid=[452, 262, 560], engine_snapshot_gib=8.74755859375,
                    solver_speed_mnodes_s=70.6856, iterations=8265,
                    fdtd_wall_seconds=7754.25, total_wall_seconds=7850.41)
    baseline['observed_bytes_per_native_grid_point'] = (
        baseline['engine_snapshot_gib'] * GIB / math.prod(baseline['native_grid']))
    rows = []
    for size in ('P15', 'P30'):
        geo = geometries[size]
        for level, scale in (('BASE', 1), ('FINE', .75)):
            dx = dy = .020 * scale
            dz = .015 * scale
            zones = [(-11.5, -10, .025 * scale), (-10, -.2, .025 * scale),
                     (-.2, 9.325, dz), (9.325, 10.325, .025 * scale)]
            nx = nodes(geo['period_x_um'], dx)
            ny = nodes(geo['period_y_um'], dy)
            # Transition/PML reserves are planning margins, not native mesher evidence.
            nz = math.ceil((zone_nodes(zones, -11.5, 10.325) + 16) * 1.10)
            nz_monitor = math.ceil(zone_nodes(zones, -10.35, 9.475) * 1.10)
            grid_points = nx * ny * nz
            monitor_points = nx * ny * nz_monitor
            electric = field_bytes(monitor_points, 91, 3)
            index = field_bytes(monitor_points, 91, 3)
            planes = field_bytes(nx * ny * 4, 91, 6)
            engine = engine_bytes(grid_points, 160)
            raw = electric + index + planes
            peak = 1.25 * (engine + 2 * raw) + 2 * GIB
            steps = math.ceil(2900e-15 / cfl_dt(dx, dy, dz))
            nominal_seconds = runtime_seconds(grid_points, steps, 70.6856e6)
            ideal_points = math.ceil((geo['volumes_um3']['ITO'] + geo['volumes_um3']['Fe'])
                                     / (dx * dy * dz))
            rows.append({
                'case': size + '_X_' + level,
                'period_x_um': geo['period_x_um'], 'period_y_um': geo['period_y_um'],
                'dx_nm': dx * 1000, 'dy_nm': dy * 1000, 'coat_dz_nm': dz * 1000,
                'bulk_pdms_dz_nm': 25 * scale, 'water_dz_nm': 25 * scale,
                'planning_nx': nx, 'planning_ny': ny, 'planning_nz': nz,
                'planning_solver_points': grid_points,
                'planning_monitor_nz': nz_monitor, 'planning_monitor_points': monitor_points,
                'engine_proxy_gib': gib(engine), 'volume_E_complex128_gib': gib(electric),
                'volume_index_complex128_gib': gib(index),
                'four_flux_planes_internal_six_components_gib': gib(planes),
                'raw_payload_gib': gib(raw), 'collect_copy_peak_model_gib': gib(peak),
                'disk_admission_gib': gib(2 * raw) + 50,
                'ideal_material_only_E_gib_NOT_IMPLEMENTED': gib(field_bytes(ideal_points, 91, 3)),
                'candidate_CFL_dt_s_NOT_NATIVE': cfl_dt(dx, dy, dz),
                'full_2900fs_steps_at_candidate_dt': steps,
                'wall_hours_D3_throughput_one_rank_scenario': nominal_seconds / 3600,
                'wall_hours_IDEAL_four_rank_scenario_NOT_GUARANTEE': nominal_seconds / 3600 / 4,
                'solver_cap_gib': 64, 'proposed_wall_admission_cap_hours': 48,
                'memory_model_gate': 'FAIL' if gib(peak) > 64 else 'FORECAST_FITS_NOT_CAD_RELEASE',
                'actual_systemcheck_available': False,
                'release_ready': release_gate(gib(peak), 64, cad_verified=False,
                                              human_start_approved=False),
            })
    order = ['P15_X_BASE', 'P30_X_BASE', 'P15_X_FINE', 'P30_X_FINE']
    rows.sort(key=lambda row: order.index(row['case']))
    summary = {
        'operation': 'PILLAR_X_PILOT_LOCAL_RESOURCE_FORECAST_01',
        'state': 'LOCAL_FORECAST_COMPLETE_RESOURCE_CONFLICT_NO_CAD_NO_SOLVE',
        'estimate_only_not_native_grid_dt_or_systemcheck': True,
        'baseline': baseline, 'sources': sources, 'case_order': order, 'cases': rows,
        'solver_proxy_bytes_per_point': 160, 'transition_padding_fraction': .10,
        'control_volume_z_um': [-10.35, 9.475],
        'source_z_um': -10.85, 'R_z_um': -11.15, 'T_z_um': 9.825,
        'native_monitor_planes_must_be_verified_before_start': True,
        'conformal_scheme': 'conformal variant 0', 'pml_layers': 8, 'pml_profile': 1,
        'double_complex_bytes': 16, 'frequencies': 91,
        'index_91_point_volume_is_conservative_export_scenario': True,
        'plane_internal_storage_is_conservative_not_vendor_measurement': True,
        'collection_peak_model_is_not_a_certified_upper_bound': True,
        'four_case_disk_free_admission_gib': sum(row['raw_payload_gib'] for row in rows) * 2 + 50,
        'current_budget': {'MAIN': 1, 'DIAGNOSTIC': 4, 'RECOVERY': 0, 'TOTAL': 5},
        'counts_if_four_cases_later_started_NOT_ACTUAL': {'MAIN': 5, 'DIAGNOSTIC': 4, 'RECOVERY': 0, 'TOTAL': 9},
        'proposed_resources': {'MPI_ranks': 4, 'threads_per_rank': 1, 'heavy_concurrency': 1,
                               'entitlement_and_account_gates_not_rechecked': True},
        'proposed_package_wall_admission_cap_hours': 192,
        'actual_CAD_actions': 0, 'actual_server_sessions': 0, 'actual_solver_starts': 0,
        'actual_budget_events_added': 0, 'human_CAD_release': False, 'human_solve_release': False,
    }
    OUT.mkdir()
    (OUT / 'summary.json').write_text(json.dumps(summary, indent=2) + '\n', encoding='ascii')
    with (OUT / 'mesh_memory_time_cases.csv').open('w', newline='', encoding='ascii') as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    print(json.dumps({'state': summary['state'], 'cases': len(rows),
        'resource_model_failures': sum(row['memory_model_gate'] == 'FAIL' for row in rows),
        'CAD': 0, 'server': 0, 'solve': 0}))


if __name__ == '__main__':
    main()
