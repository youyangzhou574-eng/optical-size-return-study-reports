"""One isolated non-solving layout evaluation using existing protected geometry."""
import importlib.util
import json
import math
from pathlib import Path
import re
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
OLD = ROOT / 'evidence/pillar_10pt_native_preflight_20261002_01'
GIB = 1024 ** 3
PHASES = ('Initialization_and_Mesh_Bytes', 'Running_Simulation_Bytes',
          'Data_Collection_Bytes', 'FSP_Saved_Monitor_Data_Bytes')
spec = importlib.util.spec_from_file_location('preserved_native_candidate', OLD / 'native_candidate.py')
native = importlib.util.module_from_spec(spec)
spec.loader.exec_module(native)


def replace_once(text, old, new):
    if text.count(old) != 1:
        raise ValueError('Preserved template changed or replacement is ambiguous')
    return text.replace(old, new, 1)


def load_candidate():
    decision_path = ROOT / 'review_exchange/OPT-SIZE-A2-PROGRESS-20260930-01/v33/final_pro_decision_receipt.json'
    decision = json.loads(decision_path.read_text())
    if decision['recorded_wavelength_nm'] != [500] or decision['mesh_FINE_nm'] != [15, 15, 11.25]:
        raise ValueError('Final Pro sampling or mesh changed')
    proof = json.loads((ROOT / 'evidence/pillar_smallcell_feasibility_20261001_01/geometry_translation_result.json').read_text())
    if {key: native.sha256_file(ROOT / key) for key in proof['source_sha256']} != proof['source_sha256']:
        raise ValueError('Protected geometry source changed')
    plan = native.case_plan('P30_X_FINE', proof)
    plan.update(wavelengths_nm=[500], custom_frequencies_hz_ascending=[599584916000000.0],
                mesh_override_z_um=[-0.05, 9.2], mesh_mode='PER_OUTER_COATING_BBOX_XY_BUFFER_80NM',
                flat_override_z_um=[-0.05, 0.2], flat_override_axes=['z'],
                required_scientific_gates=['SINGLE_POINT_DIRECT_NET', 'SINGLE_POINT_FOUR_MATERIAL_CLOSURE',
                                          'PAIRED_500NM_FE_2_PERCENT_OR_NEAR_ZERO_ABSOLUTE_GATE'],
                no_J10_or_spectral_integral=True)
    geometry = (ROOT / 'evidence/pillar_x_pilot_authorized_prepare_20261001_02/prepared01/P30_X_FINE_geometry_halo_only.lsf').read_text()
    return plan, geometry


def mesh_block(plan, geometry):
    names = re.findall(r'set\("name","(P30_H09_Fe_periodic_halo_\d{3})"\);', geometry)
    manifest = json.loads((ROOT / 'evidence/pillar_x_pilot_authorized_prepare_20261001_02/prepared01/case_manifest.json').read_text())
    expected_count = manifest[-1]['geometry']['piece_counts'][-1]
    if len(names) != expected_count or len(set(names)) != expected_count:
        raise ValueError('Outer coated periodic pieces do not match preserved geometry')
    lines = ['select("flat_coating_mesh");delete;', f'mesh_bounds=matrix({expected_count},4);']
    for index, name in enumerate(names, 1):
        lines += [f'vv=getnamed("{name}","vertices");',
                  f'ox=getnamed("{name}","x");oy=getnamed("{name}","y");',
                  'lo_x=min(vv(:,1))+ox-80e-9;hi_x=max(vv(:,1))+ox+80e-9;',
                  'lo_y=min(vv(:,2))+oy-80e-9;hi_y=max(vv(:,2))+oy+80e-9;',
                  f'mesh_bounds({index},1)=lo_x;mesh_bounds({index},2)=hi_x;',
                  f'mesh_bounds({index},3)=lo_y;mesh_bounds({index},4)=hi_y;',
                  'addmesh;', f'set("name","PILLAR_BBOX_FINE_{index:03d}");',
                  'set("x",(lo_x+hi_x)/2);set("x span",hi_x-lo_x);',
                  'set("y",(lo_y+hi_y)/2);set("y span",hi_y-lo_y);',
                  'set("z min",-50e-9);set("z max",9.2e-6);',
                  'set("override x mesh",1);set("override y mesh",1);set("override z mesh",1);',
                  'set("set maximum mesh step",1);',
                  'set("dx",15e-9);set("dy",15e-9);set("dz",11.25e-9);']
    px, py = [value * 1e-6 for value in plan['solver_period_um']]
    lines += ['addmesh;', 'set("name","FLAT_INTERFACE_Z_ONLY");',
              'set("x",0);set("y",0);', f'set("x span",{px:.17g});set("y span",{py:.17g});',
              'set("z min",-50e-9);set("z max",200e-9);',
              'set("override x mesh",0);set("override y mesh",0);set("override z mesh",1);',
              'set("set maximum mesh step",1);set("dz",11.25e-9);']
    return '\n'.join(lines)


def build_script(plan, geometry):
    script = native.native_build_script(plan, geometry)
    original_lines = [line for line in script.splitlines() if line.startswith('setnamed("flat_coating_mesh",')]
    if len(original_lines) != 7:
        raise ValueError('Preserved whole-cell mesh block changed')
    script = replace_once(script, '\n'.join(original_lines), mesh_block(plan, geometry))
    readback = '''axes=struct;
axes.x=getresult("FDTD","x");
axes.y=getresult("FDTD","y");
axes.z=getresult("FDTD","z");
jsonsave("native_mesh_axes.json",axes);
mesh_audit=struct;
mesh_audit.coated_bbox_xy=mesh_bounds;
mesh_audit.bbox_count=14;
mesh_audit.mesh_accuracy=getnamed("FDTD","mesh accuracy");
mesh_audit.mesh_refinement=getnamed("FDTD","mesh refinement");
mesh_audit.mesh_type=getnamed("FDTD","mesh type");
mesh_audit.mesh_size_increase=getnamed("FDTD","mesh allowed size increase factor");
mesh_audit.flat_override_x=getnamed("FLAT_INTERFACE_Z_ONLY","override x mesh");
mesh_audit.flat_override_y=getnamed("FLAT_INTERFACE_Z_ONLY","override y mesh");
mesh_audit.flat_override_z=getnamed("FLAT_INTERFACE_Z_ONLY","override z mesh");
mesh_audit.mesh_bbox_dx=getnamed("PILLAR_BBOX_FINE_001","dx");
mesh_audit.mesh_bbox_dy=getnamed("PILLAR_BBOX_FINE_001","dy");
mesh_audit.mesh_bbox_dz=getnamed("PILLAR_BBOX_FINE_001","dz");
jsonsave("native_mesh_readback.json",mesh_audit);
completion=struct;
completion.layout_mode=layoutmode;
completion.new_solver_starts=0;
completion.frequency_samples=length(f_read);
jsonsave("layout_complete.json",completion);'''
    return replace_once(script, '?"P30_FINE_LAYOUT_SYSTEMCHECK_COMPLETE_NO_SOLVE_NO_INDEX_EXPORT";', readback)


def number(value, name):
    if isinstance(value, bool) or not isinstance(value, (float, int)) or not math.isfinite(value) or value < 0:
        raise ValueError('Invalid or missing native ' + name)
    return float(value)


def memory_admission(document, free, disk):
    report = document['report']
    phase_bytes = {key: number(report['Approximate_Memory_Requirements'].get(key), key) for key in PHASES}
    recommended = number(report.get('Memory_Recommended'), 'Memory_Recommended')
    nodes = float(report['Total_FDTD_Yee_Nodes'])
    if not math.isfinite(nodes) or nodes <= 0:
        raise ValueError('Invalid Yee node count')
    cap = min(64., .7 * number(free, 'startup free RAM'))
    warnings = dict(MEMORY=report['Approximate_Memory_Requirements']['Alert'],
                    GEOMETRY=report['Geometry'], MESH_OVERRIDE=report['Mesh_Override'],
                    BANDWIDTH=report['Frequency_WaveLength_Settings']['Simulation_Bandwidth']['Alert'])
    reasons = []
    for key, warning in warnings.items():
        if warning is not None and warning not in ('', [], {}):
            reasons.append('NATIVE_' + key + '_WARNING')
    peak = max(recommended, *phase_bytes.values()) / GIB
    if peak > cap:
        reasons.append('CPU_PHASE_EXCEEDS_CAP')
    minimum_disk = 50 + 2 * phase_bytes['FSP_Saved_Monitor_Data_Bytes'] / GIB
    if number(disk, 'startup disk') < minimum_disk:
        reasons.append('DISK_BELOW_FSP_ONLY_MINIMUM')
    details = report['Memory_Details']
    return dict(memory_estimate_gate_pass=not reasons, reasons=reasons, cap_gib=cap,
                cpu_phase_bytes=phase_bytes, cpu_phase_gib={k: v/GIB for k, v in phase_bytes.items()},
                recommended_gib=recommended/GIB, peak_cpu_estimate_gib=peak,
                internal_fields_index_gib=number(details['Electromagnetic_Fields_and_Refractive_Index'], 'internal fields')/GIB,
                monitor_gib={k: number(v['Memory'], k)/GIB for k, v in details['Monitors'].items()},
                minimum_fsp_only_disk_gib=minimum_disk, yee_nodes_millions=nodes,
                native_warnings=warnings, memory_report_is_estimate_not_measured_peak=True,
                full_export_analysis_allocation_gate_pass=False, solver_ready=False)


def numeric_vector(original):
    if isinstance(original, dict):
        shape = original.get('_size')
        data = original.get('_data')
        if (original.get('_type') != 'matrix' or original.get('_complex') is not False
                or not isinstance(shape, list) or not isinstance(data, list)
                or not shape or any(not isinstance(dim, int) or dim < 1 for dim in shape)
                or math.prod(shape) != len(data) or sum(dim > 1 for dim in shape) > 1):
            raise ValueError('Invalid native real vector encoding')
        values = data
    elif isinstance(original, (float, int)) and not isinstance(original, bool):
        values = [original]
    elif isinstance(original, list):
        values = [row[0] if isinstance(row, list) and len(row) == 1 else row for row in original]
    else:
        raise ValueError('Unrecognized native numeric vector')
    if not values or any(isinstance(value, bool) or not isinstance(value, (float, int)) or not math.isfinite(value) for value in values):
        raise ValueError('Non-finite or nonnumeric native vector')
    return values


def axis_summary(document):
    result = {}
    for name, original in document['axes'].items():
        values = numeric_vector(original)
        if len(values) < 2 or not all(math.isfinite(value) for value in values):
            raise ValueError('Missing or invalid axis')
        steps = [b-a for a, b in zip(values, values[1:])]
        if min(steps) <= 0:
            raise ValueError('Non-monotonic native axis')
        result[name] = dict(points=len(values), cells=len(values)-1, minimum_um=values[0]*1e6,
                            maximum_um=values[-1]*1e6, min_step_nm=min(steps)*1e9,
                            max_step_nm=max(steps)*1e9, coordinate_source='NATIVE_LAYOUT_GETRESULT')
    if set(result) != {'x', 'y', 'z'}:
        raise ValueError('Incomplete native axes')
    return result


def prepare():
    plan, geometry = load_candidate()
    out = HERE / 'prepared01'
    if out.exists():
        raise FileExistsError('Preparation exists; inspect, do not regenerate')
    script = build_script(plan, geometry)
    mother = ROOT / 'evidence/a2_preflight_20260930/F0_D3_autoshutoff_20261001/build01/F0_D3_AUTOSHUTOFF_1E8_input.fsp'
    if native.sha256_file(mother) != '61B24C378622FDD91E0F4D02F0E80F47BF3103E4E02AD8E45FBB0F31491D16E0' or mother.stat().st_size != 560994:
        raise ValueError('Protected mother identity conflict')
    out.mkdir()
    with (out / 'P30_X_FINE_layout_systemcheck_candidate.lsf').open('x', encoding='ascii', newline='\n') as stream:
        stream.write(script)
    native.exclusive_json(out / 'candidate_plan.json', plan)
    worker = (OLD / 'remote_build_worker.ps1').read_text()
    worker = replace_once(worker, "$corrected=([IO.Path]::GetFileName($OutputRoot) -eq 'native_corrected02')", '$corrected=$false')
    start = worker.index('$scriptPath=')
    end = worker.index('$scriptText=', start)
    worker = worker[:start] + "$scriptPath=Join-Path $localRoot 'prepared01\\P30_X_FINE_layout_systemcheck_candidate.lsf'\n" + worker[end:]
    start = worker.index('$expectedScriptHash=')
    end = worker.index('if($scriptHash', start)
    worker = worker[:start] + "$expectedScriptHash='" + native.sha256_file(out / 'P30_X_FINE_layout_systemcheck_candidate.lsf') + "'\n" + worker[end:]
    worker = worker.replace('PILLAR_10PT_NATIVE_PREFLIGHT_01', 'PILLAR_500NM_BBOX_NATIVE_PREFLIGHT_01')
    worker = worker.replace('P30_FINE_NATIVE_BUILD_SYSTEMCHECK_01', 'P30_FINE_500NM_BBOX_NATIVE_EVALUATION_01')
    worker = replace_once(worker, "$r.success_marker=[IO.File]::ReadAllText($stdout).Contains('P30_FINE_LAYOUT_SYSTEMCHECK_COMPLETE_NO_SOLVE_NO_INDEX_EXPORT')", '''$r.stdout_marker_present=[IO.File]::ReadAllText($stdout).Contains('P30_FINE_LAYOUT_SYSTEMCHECK_COMPLETE_NO_SOLVE_NO_INDEX_EXPORT')
    $completePath=Join-Path $root 'layout_complete.json'
    $r.success_marker=$false
    if(Test-Path -LiteralPath $completePath){
        if((Get-Item -LiteralPath $completePath).Length -gt 4096){throw 'COMPLETION_FILE_SIZE_LIMIT'}
        $complete=[IO.File]::ReadAllText($completePath)|ConvertFrom-Json
        $r.success_marker=($complete.completion.layout_mode -eq 1 -and $complete.completion.new_solver_starts -eq 0 -and $complete.completion.frequency_samples -eq 1)
    }''')
    worker = replace_once(worker, "'cpu_memory_report.json','small_settings_readback.json','P30_X_FINE_candidate_input.fsp'", "'cpu_memory_report.json','small_settings_readback.json','native_mesh_axes.json','native_mesh_readback.json','layout_complete.json','P30_X_FINE_candidate_input.fsp','P30_X_FINE_layout_systemcheck_candidate.xml'")
    worker = replace_once(worker, "$meta=Get-Item -LiteralPath $path;$r.files+=", "$meta=Get-Item -LiteralPath $path;if($meta.Length -gt 2097152){throw 'NATIVE_SMALL_OUTPUT_SIZE_LIMIT'};$r.files+=")
    worker = replace_once(worker, "try{$r.cad_peak_working_set_gib=[double]$tracked.Process.PeakWorkingSet64/1GB}catch{$r.cad_peak_not_available_after_exit=$true}", '$r.cad_peak_not_available_after_exit=$true')
    worker = replace_once(worker, "($r.files.name -contains 'small_settings_readback.json')", "($r.files.name -contains 'small_settings_readback.json') -and ($r.files.name -contains 'native_mesh_axes.json') -and ($r.files.name -contains 'native_mesh_readback.json')")
    with (HERE / 'remote_build_worker.ps1').open('x', encoding='ascii', newline='\n') as stream:
        stream.write(worker)
    native.exclusive_json(out / 'preparation_receipt.json', dict(
        state='FOCUSED_LOCAL_PREPARATION_COMPLETE_NATIVE_EVALUATION_PENDING_NO_SOLVE',
        mother_bytes=560994, mother_sha256=native.sha256_file(mother),
        geometry_fragment_sha256=__import__('hashlib').sha256(geometry.encode()).hexdigest().upper(),
        LSF_sha256=native.sha256_file(out / 'P30_X_FINE_layout_systemcheck_candidate.lsf'),
        worker_sha256=native.sha256_file(HERE / 'remote_build_worker.ps1'),
        new_distinct_local_checks_counted_conservatively=10, cumulative_local_inputs_upper_bound=50,
        actual_new_CAD_starts=0, new_solver_starts=0))
    print(json.dumps(dict(prepared=True, native_execution=False, CAD=0, solve=0)))


def analyze():
    out = HERE / 'build01'
    if (out / 'evaluation_summary.json').exists():
        raise FileExistsError('Evaluation already analyzed; do not repeat')
    receipt = json.loads((out / 'receipt.json').read_text())
    if not receipt['query_ok'] or receipt['cad_pending'] or receipt['cad_exit'] != 0:
        raise ValueError('Technical native evaluation failed; no subsequent CAD')
    audit = memory_admission(json.loads((out / 'cpu_memory_report.json').read_text()),
                             receipt['free_gib_before_CAD'], receipt['disk_free_gib_before_CAD'])
    axes = axis_summary(json.loads((out / 'native_mesh_axes.json').read_text()))
    settings = json.loads((out / 'small_settings_readback.json').read_text())['readback']
    mesh = json.loads((out / 'native_mesh_readback.json').read_text())['mesh_audit']
    setting_pass = (settings['layout_mode'] == 1 and numeric_vector(settings['custom_frequency_samples']) == [599584916000000.0]
                    and math.isclose(settings['source_start'], 350e-9, rel_tol=1e-12)
                    and math.isclose(settings['source_stop'], 800e-9, rel_tol=1e-12)
                    and settings['auto_shutoff_min'] == 1e-8
                    and math.isclose(settings['simulation_time'], 2900e-15, rel_tol=1e-12)
                    and mesh['bbox_count'] == 14 and mesh['mesh_accuracy'] == 2
                    and mesh['mesh_refinement'] == 'conformal variant 0'
                    and mesh['flat_override_x'] == 0 and mesh['flat_override_y'] == 0 and mesh['flat_override_z'] == 1)
    passed = audit['memory_estimate_gate_pass'] and setting_pass
    result = dict(operation='P30_FINE_500NM_BBOX_NATIVE_EVALUATION_01',
                  state='NATIVE_ESTIMATE_PASS_ADDITIONAL_GATES_PENDING_NO_SOLVE' if passed else 'NATIVE_EVALUATION_STOP_NO_RETRY_NO_SOLVE',
                  memory=audit, native_axes=axes, native_settings_match=setting_pass,
                  inherited_mesh_size_increase=mesh['mesh_size_increase'],
                  actual_CAD_exit=receipt['cad_exit'], actual_CAD_wall_seconds=receipt['cad_wall_seconds'],
                  cumulative_CAD_count=3, cumulative_CAD_wall_seconds=20.0181661 + receipt['cad_wall_seconds'],
                  source_unchanged=receipt['source_unchanged'], new_solver_starts=0,
                  next_original_cell_CAD_permitted=passed, smaller_cell_human_authorization=False)
    native.exclusive_json(out / 'evaluation_summary.json', result)
    print(json.dumps(result))


if __name__ == '__main__':
    {'prepare': prepare, 'analyze': analyze}[sys.argv[1]]()
