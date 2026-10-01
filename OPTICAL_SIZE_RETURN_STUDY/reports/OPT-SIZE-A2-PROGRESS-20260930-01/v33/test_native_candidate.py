import copy
import json
from pathlib import Path
import re
import unittest
import native_candidate as production

ROOT = Path(__file__).resolve().parents[2]
PROOF = ROOT / "evidence/pillar_smallcell_feasibility_20261001_01/geometry_translation_result.json"


def cpu_report():
    return {
        "Memory_Recommended_Bytes": 12 * 1024 ** 3,
        "Total_FDTD_Yee_Nodes": 25.0,
        "Approximate_Memory_Requirements": {
            "Alert": "",
            "Initialization_and_Mesh_Bytes": 4 * 1024 ** 3,
            "Running_Simulation_Bytes": 12 * 1024 ** 3,
            "Data_Collection_Bytes": 10 * 1024 ** 3,
            "FSP_Saved_Monitor_Data_Bytes": 3 * 1024 ** 3,
        },
        "Geometry": [],
        "Mesh_Override": [],
        "Frequency_WaveLength_Settings": {
            "Simulation_Bandwidth": {"Alert": ""}
        },
    }


class TestNativeCandidate(unittest.TestCase):
    def test_single_500nm_sample_has_one_native_slot_and_preserves_physics(self):
        proof = json.loads(PROOF.read_text(encoding="utf-8"))
        plan = production.case_plan("P30_X_FINE", proof)
        plan["wavelengths_nm"] = [500]
        plan["custom_frequencies_hz_ascending"] = [299792458.0 / (500e-9)]
        fragment = (ROOT / "evidence/pillar_x_pilot_authorized_prepare_20261001_02/prepared01/P30_X_FINE_geometry_halo_only.lsf").read_text(encoding="utf-8")
        script = production.native_build_script(plan, fragment)
        self.assertIn("f10=matrix(1,1);", script)
        self.assertIn('if(length(f_read)!=1)', script)
        self.assertNotIn("f10(2)", script)
        self.assertEqual(plan["source_band_nm"], [350, 800])
        self.assertEqual(plan["mesh_override_nm"], [15.0, 15.0, 11.25])
        self.assertEqual(plan["solver_period_um"], [18.0, 10.392304845413264])
        self.assertFalse(plan["solver_ready"])
        self.assertFalse(plan["tile_multiplication_enabled"])

    def test_native_xml_641_inactive_linear_axes_regression(self):
        proof = json.loads(PROOF.read_text(encoding="utf-8"))
        plan = production.case_plan("P30_X_FINE", proof)
        fragment = (ROOT / "evidence/pillar_x_pilot_authorized_prepare_20261001_02/prepared01/P30_X_FINE_geometry_halo_only.lsf").read_text(encoding="utf-8")
        script = production.native_build_script(plan, fragment)
        for name, following in (("E_translation_witness_1", 'set("name","E_translation_witness_2")'),
                                ("E_translation_witness_2", "addindex;")):
            section = script.split(f'set("name","{name}");', 1)[1].split(following, 1)[0]
            self.assertNotIn('set("down sample x"', section)
            self.assertNotIn('set("down sample y"', section)
            self.assertIn('set("down sample z",1);', section)
        volume = script.split('set("name","REP_TILE_E");', 1)[1].split('addprofile;', 1)[0]
        for axis in "xyz":
            self.assertIn(f'set("down sample {axis}",1);', volume)

    def test_native_build_is_layout_only_and_has_no_large_index_read(self):
        self.assertTrue(hasattr(production, "native_build_script"), "Layout-only native candidate missing")
        proof = json.loads(PROOF.read_text(encoding="utf-8"))
        plan = production.case_plan("P30_X_FINE", proof)
        fragment = (ROOT / "evidence/pillar_x_pilot_authorized_prepare_20261001_02/prepared01/P30_X_FINE_geometry_halo_only.lsf").read_text(encoding="utf-8")
        script = production.native_build_script(plan, fragment)
        commands = "\n".join(line for line in script.splitlines() if not line.lstrip().startswith("#"))
        self.assertIsNone(re.search(r"\b(?:run|runjobs|runanalysis|switchtolayout|mpiexec)\s*[;(]", commands))
        self.assertIn("report=runsystemcheck;", commands)
        self.assertNotIn('getresult("REP_TILE_INDEX"', commands)
        self.assertIn('setglobalmonitor("custom frequency samples",f10);', commands)
        self.assertIn('setnamed("FDTD","x span",1.8e-05);', commands)
        self.assertIn('set("name","REP_TILE_E");', commands)
        self.assertIn('set("name","REP_TILE_INDEX");', commands)
        self.assertIn('setnamed("flat_coating_mesh","z min",-2e-07);', commands)
        self.assertIn('setnamed("flat_coating_mesh","z max",9.325e-06);', commands)
        self.assertEqual(commands.count('addprofile;'), 3)

    def test_sample_mapping_is_wavelength_not_uniform_frequency(self):
        # A uniform-frequency implementation must fail this wavelength identity.
        self.assertTrue(hasattr(production, "frequencies_hz"), "10-point frequency mapping missing")
        f = production.frequencies_hz()
        self.assertEqual(len(f), 10)
        self.assertEqual(sorted(f), f)
        wavelength = [299792458.0 / value * 1e9 for value in reversed(f)]
        for actual, expected in zip(wavelength, [350,400,450,500,550,600,650,700,750,800]):
            self.assertAlmostEqual(actual, expected, places=7)

    def test_tile_candidate_keeps_solver_cell_and_does_not_claim_native_pass(self):
        # Shrinking the solver along with the monitor would change the frozen representation.
        self.assertTrue(hasattr(production, "case_plan"), "Full-cell/tile separation missing")
        proof = json.loads(PROOF.read_text(encoding="utf-8"))
        plan = production.case_plan("P30_X_FINE", proof)
        self.assertEqual(plan["solver_period_um"], [18.0, 10.392304845413264])
        self.assertEqual(plan["tile_span_um"], [6.0, 10.392304845413264])
        self.assertEqual(plan["repetitions"], 3)
        self.assertEqual(plan["mesh_override_nm"], [15.0, 15.0, 11.25])
        self.assertEqual(plan["volume_fields"], ["Ex","Ey","Ez"])
        self.assertFalse(plan["native_tile_pass"])
        self.assertFalse(plan["solver_ready"])
        bad = copy.deepcopy(proof)
        bad["probes"]["P3_H09"]["area_reduction_factor"] = 6
        with self.assertRaises(ValueError):
            production.case_plan("P30_X_FINE", bad)

    def test_cpu_report_cannot_be_replaced_by_gpu_fields_or_missing_memory(self):
        # GPU-only or null collection evidence must not be interpreted as CPU zero bytes.
        self.assertTrue(hasattr(production, "cpu_memory_admission"), "CPU memory admission missing")
        accepted = production.cpu_memory_admission(cpu_report(), 100.0, 100.0)
        self.assertTrue(accepted["memory_estimate_gate_pass"])
        self.assertFalse(accepted["solver_ready"])
        for bad in [
            {"Approximate_GPU_Memory_Requirements": {"Maximum_Bytes": 1024}},
            dict(cpu_report(), Memory_Recommended_Bytes=None),
        ]:
            with self.assertRaises(ValueError):
                production.cpu_memory_admission(bad, 100.0, 100.0)

    def test_alert_fraction_cap_collection_and_disk_fail_closed(self):
        # A valid recommendation must not conceal a bad later phase or insufficient free memory.
        self.assertTrue(hasattr(production, "cpu_memory_admission"), "CPU memory admission missing")
        bad = cpu_report()
        bad["Approximate_Memory_Requirements"]["Alert"] = "unverified conformal estimate"
        self.assertFalse(production.cpu_memory_admission(bad, 100.0, 100.0)["memory_estimate_gate_pass"])
        bad = cpu_report()
        bad["Approximate_Memory_Requirements"]["Data_Collection_Bytes"] = 70 * 1024 ** 3
        self.assertFalse(production.cpu_memory_admission(bad, 100.0, 100.0)["memory_estimate_gate_pass"])
        self.assertFalse(production.cpu_memory_admission(cpu_report(), 10.0, 100.0)["memory_estimate_gate_pass"])
        self.assertFalse(production.cpu_memory_admission(cpu_report(), 100.0, 1.0)["memory_estimate_gate_pass"])


if __name__ == "__main__":
    unittest.main()
