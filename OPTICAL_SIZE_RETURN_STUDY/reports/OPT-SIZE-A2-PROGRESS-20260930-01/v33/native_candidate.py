"""Local candidates only. No CAD, remote connection or solver launch API."""

import hashlib
import json
import math
from pathlib import Path
import re
import sys


ROOT = Path(__file__).resolve().parents[2]
WAVELENGTHS_NM = list(range(350, 801, 50))
CASE_ORDER = ("P15_X_BASE", "P30_X_BASE", "P15_X_FINE", "P30_X_FINE")
GIB = 1024 ** 3
CPU_PHASES = (
    "Initialization_and_Mesh_Bytes",
    "Running_Simulation_Bytes",
    "Data_Collection_Bytes",
    "FSP_Saved_Monitor_Data_Bytes",
)


def finite_number(value, name, positive=False):
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(f"Missing or nonnumeric {name}")
    if not math.isfinite(value) or value < 0 or (positive and value == 0):
        raise ValueError(f"Invalid {name}")
    return float(value)


def frequencies_hz():
    return sorted(299792458.0 / (wave * 1e-9) for wave in WAVELENGTHS_NM)


def case_plan(case_name, geometry_proof):
    if case_name not in CASE_ORDER:
        raise ValueError("Not one of the four authorized X cases")
    side = 1.5 if case_name.startswith("P15_") else 3.0
    probe = geometry_proof["probes"]["P1.5_H09" if side == 1.5 else "P3_H09"]
    expected = [6.0 * side, 2.0 * math.sqrt(3.0) * side]
    original = probe["original_period_um"]
    tile = probe["candidate_period_um"]
    if len(original) != 2 or len(tile) != 2 or probe["controls_passed"] is not True:
        raise ValueError("Incomplete nominal geometry evidence")
    factors = []
    for actual, proposed, frozen in zip(original, tile, expected):
        a = finite_number(actual, "original period", positive=True)
        t = finite_number(proposed, "tile span", positive=True)
        if not math.isclose(a, frozen, rel_tol=1e-12, abs_tol=1e-12):
            raise ValueError("Nominal evidence does not match the original full solver cell")
        ratio = a / t
        if not math.isclose(ratio, round(ratio), rel_tol=1e-12, abs_tol=1e-12):
            raise ValueError("Tile does not partition the original cell into integers")
        factors.append(round(ratio))
    repetitions = math.prod(factors)
    if factors != [3, 1] or probe["area_reduction_factor"] != repetitions:
        raise ValueError("Tile repetition count disagrees with the preserved geometry result")
    matching = [trial for trial in probe["trials"]
                if trial["axis"] == "x" and trial["divisor"] == factors[0]]
    if len(matching) != 1 or matching[0]["nominal_geometry_match"] is not True:
        raise ValueError("No corresponding positive translation trial")
    if any(control["nominal_geometry_match"] is not False
           for control in probe["negative_controls"]):
        raise ValueError("Negative geometry control failed")
    return {
        "case": case_name,
        "solver_period_um": [float(x) for x in original],
        "tile_span_um": [float(x) for x in tile],
        "tile_center_um": [0.0, 0.0],
        "repetitions": repetitions,
        "mesh_override_nm": [15.0, 15.0, 11.25] if case_name.endswith("FINE")
                            else [20.0, 20.0, 15.0],
        "mesh_override_z_um": [-0.2, 9.325],
        "mesh_outside_override": "INHERIT_ORIGINAL_AUTOMATIC_MESH",
        "solver_z_um": [-11.5, 10.325],
        "control_z_um": [-10.35, 9.475],
        "source_z_um": -10.85,
        "source_band_nm": [350, 800],
        "maximum_time_fs": 2900,
        "auto_shutoff_min": 1e-8,
        "wavelengths_nm": WAVELENGTHS_NM,
        "custom_frequencies_hz_ascending": frequencies_hz(),
        "volume_fields": ["Ex", "Ey", "Ez"],
        "volume_H_or_P": False,
        "spatial_interpolation": "none",
        "downsample_xyz": [1, 1, 1],
        "volume_monitors": ["REP_TILE_E", "REP_TILE_INDEX"],
        "flux_monitors": {
            "R_below_source": -11.15,
            "T_above_coating": 9.825,
            "P_bottom_before_structure": -10.35,
            "P_top_after_structure": 9.475,
        },
        "flux_scope": "ORIGINAL_FULL_CELL",
        "material_scope": ["Fe2O3", "ITO", "PDMS", "water"],
        "nominal_geometry_only": True,
        "native_tile_pass": False,
        "tile_multiplication_enabled": False,
        "solver_ready": False,
        "required_native_gates": [
            "CPU_ALL_PHASE_RESOURCE_ADMISSION",
            "ACTUAL_FREQUENCIES_AND_NATIVE_YEE_COORDINATES",
            "GRID_MATERIAL_SOURCE_TRANSLATION_NO_INTERPOLATION",
            "NATIVE_EFFECTIVE_EPSILON_COMPONENT_PARTITION_NO_UNASSIGNED",
            "DUAL_CELL_CLIPPING_AND_PERIODIC_ENDPOINT_DEDUPLICATION",
            "STRICT_IDENTITY_NO_WRITER_AND_RUNTIME_RESOURCE_GATES",
        ],
        "required_scientific_gates": [
            "DIRECT_NET_ORIGINAL_LIMITS", "FOUR_MATERIAL_CLOSURE_ORIGINAL_LIMITS",
            "BASE_GATES_BEFORE_FINE", "PAIRED_MESH_STABILITY_10PT_NOT_SPECTRAL_CONVERGENCE",
        ],
    }


def empty_alert(value):
    if isinstance(value, str):
        return not value.strip()
    if isinstance(value, (list, dict)):
        return not value
    raise ValueError("Unrecognized native alert representation")


def cpu_memory_admission(report, actual_free_gib, actual_disk_free_gib):
    free = finite_number(actual_free_gib, "actual free RAM", positive=True)
    disk = finite_number(actual_disk_free_gib, "actual disk free", positive=True)
    recommended = finite_number(report.get("Memory_Recommended_Bytes"),
                                "CPU recommended bytes", positive=True)
    nodes = finite_number(report.get("Total_FDTD_Yee_Nodes"),
                          "CPU Yee nodes in millions", positive=True)
    phases = report.get("Approximate_Memory_Requirements")
    if not isinstance(phases, dict):
        raise ValueError("Missing CPU phase memory report; GPU fields are not a substitute")
    values = {name: finite_number(phases.get(name), name) for name in CPU_PHASES}
    try:
        alerts = {
            "memory": phases["Alert"],
            "geometry": report["Geometry"],
            "mesh_override": report["Mesh_Override"],
            "bandwidth": report["Frequency_WaveLength_Settings"]["Simulation_Bandwidth"]["Alert"],
        }
    except (KeyError, TypeError) as error:
        raise ValueError("Incomplete CPU warning evidence") from error
    reasons = [f"Native {name} warning" for name, value in alerts.items() if not empty_alert(value)]
    cap = min(64.0, 0.70 * free)
    peak_estimate = max(recommended, *values.values()) / GIB
    if peak_estimate > cap:
        reasons.append("CPU phase or recommended memory exceeds the unchanged cap")
    # This only admits the FSP estimate; raw exports/snapshots require their own disk calculation.
    minimum_disk = 50.0 + 2.0 * values["FSP_Saved_Monitor_Data_Bytes"] / GIB
    if disk < minimum_disk:
        reasons.append("Disk is below 2x estimated FSP monitor data plus 50 GiB")
    return {
        "memory_estimate_gate_pass": not reasons,
        "reasons": reasons,
        "cap_gib": cap,
        "peak_cpu_estimate_gib": peak_estimate,
        "minimum_fsp_only_disk_gib": minimum_disk,
        "cpu_phase_bytes": values,
        "yee_nodes_millions": nodes,
        "native_report_is_estimate_not_measured_peak": True,
        "index_export_analysis_allocation_gate_pass": False,
        "total_new_output_disk_gate_pass": False,
        "solver_ready": False,
    }


def sha256_file(path):
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest().upper()


def exclusive_json(path, value):
    with path.open("x", encoding="utf-8", newline="\n") as stream:
        json.dump(value, stream, indent=2, allow_nan=False)
        stream.write("\n")


def native_build_script(plan, geometry_fragment):
    if plan["case"] != "P30_X_FINE" or plan["solver_ready"] or plan["native_tile_pass"]:
        raise ValueError("This operation prepares only the worst-case layout preflight")
    commands = "\n".join(line for line in geometry_fragment.splitlines()
                         if not line.lstrip().startswith("#"))
    if re.search(r"\b(?:run|runjobs|runanalysis|save|load|switchtolayout)\s*[;(]", commands):
        raise ValueError("Geometry fragment contains operations outside geometry creation")
    full_x, full_y = [x * 1e-6 for x in plan["solver_period_um"]]
    tile_x, tile_y = [x * 1e-6 for x in plan["tile_span_um"]]
    number = lambda value: format(value, ".15g")
    lines = [
        "# LOCAL CANDIDATE ONLY. Execute in a new admitted CAD directory, never an old run directory.",
        "# The controller must verify mother SHA and CreateNew directory before CAD starts.",
        "# No solve, no result hash, no 3D index extraction; native equivalence remains pending.",
        'load("mother_input.fsp");',
        'if(!layoutmode) { error("Mother is not the protected pre-solve layout"); }',
    ]
    for name in ("water_background", "PDMS_base", "ITO_flat", "Fe2O3_flat",
                 "E_control_raw_Yee", "index_control_raw_Yee",
                 "E_uniformity_witness_1", "E_uniformity_witness_2"):
        lines.append(f'select("{name}");delete;')
    lines.append(geometry_fragment)
    for name, value in (("x span", full_x), ("y span", full_y),
                        ("z min", -11.5e-6), ("z max", 10.325e-6)):
        lines.append(f'setnamed("FDTD","{name}",{number(value)});')
    # Preserve the inherited fit, conformal scheme, PML, source normalization and stopping policy.
    for name, value in (("x span", full_x), ("y span", full_y)):
        lines.append(f'setnamed("source_from_bottom_water_side","{name}",{number(value)});')
    for name, value in (("x span", full_x), ("y span", full_y),
                        ("z min", -0.2e-6), ("z max", 9.325e-6),
                        ("dx", 15e-9), ("dy", 15e-9), ("dz", 11.25e-9)):
        lines.append(f'setnamed("flat_coating_mesh","{name}",{number(value)});')
    sample_count = len(plan["custom_frequencies_hz_ascending"])
    lines.append(f"f10=matrix({sample_count},1);")
    for index, frequency in enumerate(plan["custom_frequencies_hz_ascending"], 1):
        lines.append(f"f10({index})={frequency:.17g};")
    lines += ['setglobalmonitor("sample spacing","custom");',
              'setglobalmonitor("custom frequency samples",f10);']
    for name, z_um in plan["flux_monitors"].items():
        for prop, value in (("x span", full_x), ("y span", full_y), ("z", z_um * 1e-6),
                            ("override global monitor settings", 0)):
            lines.append(f'setnamed("{name}","{prop}",{number(value)});')
    for name, monitor_type, x in (("REP_TILE_E", "3D", 0.0),
                                  ("E_translation_witness_1", "Linear Z", 0.0),
                                  ("E_translation_witness_2", "Linear Z", tile_x)):
        lines += ['addprofile;', f'set("name","{name}");',
                  f'set("monitor type","{monitor_type}");', f'set("x",{number(x)});',
                  'set("y",0);', 'set("z min",-1.035e-05);', 'set("z max",9.475e-06);',
                  'set("override global monitor settings",0);', 'set("spatial interpolation","none");']
        if monitor_type == "3D":
            lines += [f'set("x span",{number(tile_x)});', f'set("y span",{number(tile_y)});',
                      'set("down sample x",1);set("down sample y",1);']
        lines.append('set("down sample z",1);')
        for component in ("Ex", "Ey", "Ez", "Hx", "Hy", "Hz", "Px", "Py", "Pz"):
            enabled = int(component in plan["volume_fields"])
            lines.append(f'set("output {component}",{enabled});')
        lines.append('set("output power",0);')
    lines += ["addindex;", 'set("name","REP_TILE_INDEX");', 'set("monitor type","3D");',
              'set("x",0);set("y",0);', f'set("x span",{number(tile_x)});',
              f'set("y span",{number(tile_y)});', 'set("z min",-1.035e-05);',
              'set("z max",9.475e-06);', 'set("override global monitor settings",0);',
              'set("spatial interpolation","none");',
              'set("down sample x",1);set("down sample y",1);set("down sample z",1);',
              'f_read=getglobalmonitor("custom frequency samples");',
              f'if(length(f_read)!={sample_count}) {{ error("Monitor sample count mismatch"); }}',
              'if(max(abs(f_read-f10))/min(abs(f10))>1e-12) { error("Custom frequency readback mismatch"); }',
              'if(!layoutmode) { error("Unexpected non-layout state before system check"); }',
              'save("P30_X_FINE_candidate_input.fsp");',
              'report=runsystemcheck;', 'jsonsave("cpu_memory_report.json",report);',
              'readback=struct;', 'readback.layout_mode=layoutmode;',
              'readback.custom_frequency_samples=f_read;',
              'readback.custom_frequency_table_readback_only=1;',
              'readback.actual_index_frequency_gate_pass=0;',
              'readback.dt=getnamed("FDTD","dt");',
              'readback.source_start=getnamed("source_from_bottom_water_side","wavelength start");',
              'readback.source_stop=getnamed("source_from_bottom_water_side","wavelength stop");',
              'readback.auto_shutoff_min=getnamed("FDTD","auto shutoff min");',
              'readback.simulation_time=getnamed("FDTD","simulation time");',
              'jsonsave("small_settings_readback.json",readback);',
              'if(!layoutmode) { error("System check left layout unexpectedly"); }',
              '?"P30_FINE_LAYOUT_SYSTEMCHECK_COMPLETE_NO_SOLVE_NO_INDEX_EXPORT";',
              "exit;", ""]
    return "\n".join(lines)


def prepare_local_candidates():
    proof_path = ROOT / "evidence/pillar_smallcell_feasibility_20261001_01/geometry_translation_result.json"
    proof = json.loads(proof_path.read_text(encoding="utf-8"))
    protected = {relative: sha256_file(ROOT / relative)
                 for relative in proof["source_sha256"]}
    if protected != proof["source_sha256"]:
        raise ValueError("Protected source hash differs from the preserved geometry receipt")
    mother = ROOT / "evidence/a2_preflight_20260930/F0_D3_autoshutoff_20261001/build01/F0_D3_AUTOSHUTOFF_1E8_input.fsp"
    mother_sha = sha256_file(mother)
    if mother.stat().st_size != 560994 or mother_sha != "61B24C378622FDD91E0F4D02F0E80F47BF3103E4E02AD8E45FBB0F31491D16E0":
        raise ValueError("Closed pre-solve mother identity mismatch")
    plans = [case_plan(name, proof) for name in CASE_ORDER]
    geometry_path = ROOT / "evidence/pillar_x_pilot_authorized_prepare_20261001_02/prepared01/P30_X_FINE_geometry_halo_only.lsf"
    script = native_build_script(plans[-1], geometry_path.read_text(encoding="utf-8"))
    out = Path(__file__).resolve().parent / "prepared01"
    out.mkdir(exist_ok=False)
    for plan in plans:
        exclusive_json(out / (plan["case"] + "_candidate.json"), plan)
    with (out / "P30_X_FINE_layout_systemcheck_candidate.lsf").open("x", encoding="ascii", newline="\n") as stream:
        stream.write(script)
    exclusive_json(out / "summary.json", {
        "operation": "PILLAR_10PT_NATIVE_PREFLIGHT_01",
        "state": "LOCAL_FOUR_CASE_CANDIDATES_READY_NATIVE_GATES_PENDING_NO_SOLVE",
        "pro_decision": "OPT-SIZE-PRO-PILLAR-10PT-PRODUCTION-PLAN-20261002-08",
        "native_preflight_order": ["P30_X_FINE_BUILD", "P30_X_FINE_REOPEN"],
        "solve_order_if_all_gates_pass": list(CASE_ORDER),
        "protected_source_sha256": protected,
        "geometry_proof_sha256": sha256_file(proof_path),
        "closed_mother_sha256": mother_sha,
        "closed_mother_bytes": mother.stat().st_size,
        "geometry_fragment_sha256": sha256_file(geometry_path),
        "layout_systemcheck_script_sha256": sha256_file(out / "P30_X_FINE_layout_systemcheck_candidate.lsf"),
        "script_native_execution_status": "NOT_EXECUTED_PROPERTY_SUPPORT_UNVERIFIED",
        "server_sessions": 0, "CAD_starts": 0, "solver_starts": 0,
        "budget_changed": False, "solver_ready": False,
        "native_resource_gate": "NOT_YET_TESTED",
        "native_index_Yee_translation_gate": "NOT_YET_TESTED",
        "no_FSP_or_original_source_writes": True,
    })
    if {relative: sha256_file(ROOT / relative) for relative in protected} != protected:
        raise ValueError("Protected source changed during local generation")
    return {"output": str(out), "case_count": len(plans), "solver_starts": 0,
            "protected_sources_unchanged": True, "solver_ready": False}


def prepare_line_fix():
    here = Path(__file__).resolve().parent
    original = here / "prepared01/P30_X_FINE_layout_systemcheck_candidate.lsf"
    if sha256_file(original) != "0FE0E34992AFD5EAA5880539AB2387706E5251F533F9E1E4687527B4D9C6E40A":
        raise ValueError("Original failed script changed")
    plan = json.loads((here / "prepared01/P30_X_FINE_candidate.json").read_text(encoding="utf-8"))
    fragment_path = ROOT / "evidence/pillar_x_pilot_authorized_prepare_20261001_02/prepared01/P30_X_FINE_geometry_halo_only.lsf"
    script = native_build_script(plan, fragment_path.read_text(encoding="utf-8"))
    out = here / "corrected_layout01"
    out.mkdir(exist_ok=False)
    target = out / "P30_X_FINE_layout_systemcheck_corrected.lsf"
    with target.open("x", encoding="ascii", newline="\n") as stream:
        stream.write(script)
    result = {
        "state": "LOCAL_LINEAR_Z_INACTIVE_XY_PROPERTY_FIX_NOT_NATIVE_VALIDATED",
        "native_error": "in set, the requested property 'down sample x' is inactive",
        "native_error_original_line": 641,
        "fix": "Linear Z monitors set only down sample z=1; 3D E/index still use x/y/z=1",
        "original_failed_script_sha256": sha256_file(original),
        "corrected_script_sha256": sha256_file(target),
        "physics_mesh_source_spectrum_volume_sampling_unchanged": True,
        "server_sessions": 0, "CAD_starts": 0, "solve_starts": 0,
        "native_validation": "NOT_YET_TESTED",
        "automatic_native_retry": False,
    }
    exclusive_json(out / "receipt.json", result)
    return result


if __name__ == "__main__":
    result = prepare_line_fix() if sys.argv[1:] == ["--prepare-line-fix"] else prepare_local_candidates()
    print(json.dumps(result, allow_nan=False))
