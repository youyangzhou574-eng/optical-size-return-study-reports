"""Prepare one-point review artifacts locally. No remote, CAD or solve calls."""

import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
PRIOR = ROOT / "evidence/pillar_10pt_native_preflight_20261002_01"
sys.path.insert(0, str(PRIOR))
import native_candidate as candidate


def prepare():
    proof_path = ROOT / "evidence/pillar_smallcell_feasibility_20261001_01/geometry_translation_result.json"
    proof = json.loads(proof_path.read_text(encoding="utf-8"))
    protected = {relative: candidate.sha256_file(ROOT / relative)
                 for relative in proof["source_sha256"]}
    if protected != proof["source_sha256"]:
        raise ValueError("Protected geometry sources changed")
    raw_path = PRIOR / "native_corrected02/cpu_memory_report.json"
    raw_sha = candidate.sha256_file(raw_path)
    if raw_sha != "9411F62470C764996B05FE0884410642E35FF4843303DAA6750970DA71541CE1":
        raise ValueError("Original native CPU report changed")
    raw = json.loads(raw_path.read_text(encoding="utf-8"))["report"]
    details = raw["Memory_Details"]
    phases = raw["Approximate_Memory_Requirements"]
    monitors = [{"name": value["Monitor_Name"],
                 "ten_point_bytes": value["Memory"],
                 "one_point_proxy_bytes": value["Memory"] / 10.0}
                for value in details["Monitors"].values()]
    old_monitor_bytes = sum(row["ten_point_bytes"] for row in monitors)
    new_monitor_bytes = sum(row["one_point_proxy_bytes"] for row in monitors)
    fixed_bytes = phases["Running_Simulation_Bytes"] - old_monitor_bytes
    proxy = {
        "method": "Unchanged-grid scalar proxy: keep non-monitor runtime bytes; divide DFT monitor bytes by 10",
        "source_native_report_sha256": raw_sha,
        "wavelength_nm": 500,
        "frequency_hz": 299792458.0 / 500e-9,
        "native_one_point_systemcheck_performed": False,
        "electromagnetic_fields_and_index_unchanged_GiB": details["Electromagnetic_Fields_and_Refractive_Index"] / candidate.GIB,
        "non_monitor_runtime_unchanged_GiB": fixed_bytes / candidate.GIB,
        "one_point_monitors_proxy_GiB": new_monitor_bytes / candidate.GIB,
        "one_point_runtime_proxy_GiB": (fixed_bytes + new_monitor_bytes) / candidate.GIB,
        "one_point_saved_monitor_proxy_GiB": phases["FSP_Saved_Monitor_Data_Bytes"] / 10.0 / candidate.GIB,
        "collection_estimate": "UNKNOWN: not assumed proportional to monitor count",
        "monitors": monitors,
        "memory_cap_GiB": 64,
        "unchanged_solver_grid_alone_exceeds_cap": details["Electromagnetic_Fields_and_Refractive_Index"] / candidate.GIB > 64,
        "memory_gate_pass": False,
        "solver_ready": False,
    }
    plans = []
    for name in candidate.CASE_ORDER:
        plan = candidate.case_plan(name, proof)
        plan["wavelengths_nm"] = [500]
        plan["custom_frequencies_hz_ascending"] = [proxy["frequency_hz"]]
        plan["one_point_revision"] = {
            "human_requested_single_wavelength": True,
            "500nm_selected_by_executor_from_verified_legacy_component_setup": True,
            "source_band_unchanged_not_monochromatic_source": True,
            "observable": "A_Fe2O3_X_500nm (plus R/T and independently available materials)",
            "not_a_spectral_integral_or_J10": True,
            "single_point_mesh_metric_requires_Pro_ruling": True,
        }
        plan["required_scientific_gates"] = [
            "FINITE_ACTUAL_F_YEE_COORDS_MATERIAL_OWNERSHIP",
            "DIRECT_NET_ORIGINAL_LIMITS",
            "FOUR_MATERIAL_CLOSURE_ORIGINAL_LIMITS",
            "BASE_GATES_BEFORE_FINE",
            "SINGLE_POINT_MESH_COMPARISON_PENDING_PRO_RULE_NOT_J10",
        ]
        plans.append(plan)
    fragment_path = ROOT / "evidence/pillar_x_pilot_authorized_prepare_20261001_02/prepared01/P30_X_FINE_geometry_halo_only.lsf"
    script = candidate.native_build_script(plans[-1], fragment_path.read_text(encoding="utf-8"))
    out = HERE / "prepared01"
    out.mkdir(exist_ok=False)
    for plan in plans:
        candidate.exclusive_json(out / (plan["case"] + "_500nm_candidate.json"), plan)
    target = out / "P30_X_FINE_500nm_layout_candidate_NOT_EXECUTED.lsf"
    with target.open("x", encoding="ascii", newline="\n") as stream:
        stream.write(script)
    candidate.exclusive_json(out / "one_point_resource_proxy.json", proxy)
    receipt = {
        "operation": "PILLAR_500NM_LOCAL_REVISION_01",
        "state": "LOCAL_SINGLE_POINT_CANDIDATES_PREPARED_P30_FINE_GRID_RESOURCE_STOP_NO_SOLVE",
        "user_request": "Now first calculate one wavelength",
        "wavelength_nm": 500,
        "source_band_nm": [350, 800],
        "protected_sources_sha256": protected,
        "protected_sources_unchanged": {relative: candidate.sha256_file(ROOT / relative) for relative in protected} == protected,
        "native_report_sha256": raw_sha,
        "candidate_script_sha256": candidate.sha256_file(target),
        "candidate_script_native_execution": "NOT_EXECUTED",
        "new_remote_sessions": 0,
        "new_CAD_starts": 0,
        "new_solver_starts": 0,
        "cumulative_actual_CAD_starts_in_scope": 2,
        "cumulative_actual_CAD_wall_seconds_in_scope": 20.0181661,
        "cumulative_known_distinct_synthetic_inputs": 40,
        "original_synthetic_input_limit": 40,
        "new_distinct_test_input": "one 500nm sample in existing P30_FINE plan; same input reused for RED/GREEN",
        "original_science_budget": {"MAIN": 1, "DIAGNOSTIC": 4, "RECOVERY": 0, "TOTAL": 5},
        "no_smaller_solver_cell_or_mesh_or_scope_change_applied": True,
        "all_four_native_preflights_before_solver_start_rule_unchanged": True,
        "resource_gate_pass": False,
        "native_tile_pass": False,
        "solver_ready": False,
    }
    if not receipt["protected_sources_unchanged"]:
        raise ValueError("Protected source changed during preparation")
    candidate.exclusive_json(out / "receipt.json", receipt)
    return {"state": receipt["state"], "output": str(out),
            "runtime_proxy_GiB": proxy["one_point_runtime_proxy_GiB"],
            "solver_grid_alone_GiB": proxy["electromagnetic_fields_and_index_unchanged_GiB"],
            "solver_starts": 0, "CAD_starts": 0}


if __name__ == "__main__":
    print(json.dumps(prepare(), allow_nan=False))
