import copy
import json
from pathlib import Path
import re
import unittest

import bbox_preflight as subject


class BboxPreflightTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.plan, cls.geometry = subject.load_candidate()
        cls.script = subject.build_script(cls.plan, cls.geometry)
        cls.report = json.loads((subject.OLD / 'native_corrected02/cpu_memory_report.json').read_text())

    def test_whole_override_removed(self):
        self.assertIn('select("flat_coating_mesh");delete;', self.script)
        self.assertNotIn('setnamed("flat_coating_mesh"', self.script)

    def test_native_outer_bbox_and_buffer(self):
        self.assertEqual(self.script.count('addmesh;'), 15)
        self.assertEqual(self.script.count('"vertices");'), 14)
        self.assertIn('min(vv(:,1))+ox-80e-9', self.script)
        self.assertIn('max(vv(:,2))+oy+80e-9', self.script)
        self.assertIn('set("z min",-50e-9);set("z max",9.2e-6);', self.script)

    def test_flat_override_z_only(self):
        block = self.script.split('set("name","FLAT_INTERFACE_Z_ONLY");', 1)[1].split('f10=matrix', 1)[0]
        self.assertIn('set("override x mesh",0);set("override y mesh",0);', block)
        self.assertIn('set("override z mesh",1);', block)
        self.assertNotRegex(block, r'set\("d[xy]"')

    def test_single_frequency_and_unchanged_source(self):
        self.assertEqual(self.plan['custom_frequencies_hz_ascending'], [599584916000000.0])
        self.assertIn('f10=matrix(1,1);', self.script)
        self.assertIn('f10(1)=599584916000000;', self.script)
        self.assertNotRegex(self.script, r'setnamed\("FDTD","(?:mesh accuracy|mesh refinement|mesh allowed size increase factor|simulation time|auto shutoff min)"')
        self.assertNotRegex(self.script, r'setnamed\("source_from_bottom_water_side","wavelength')

    def test_no_solve_or_full_index(self):
        uncommented = '\n'.join(line for line in self.script.splitlines() if not line.startswith('#'))
        self.assertNotRegex(uncommented, r'\b(?:run|runjobs|runanalysis|switchtolayout)\s*[;(]')
        self.assertEqual(re.findall(r'getresult\("FDTD","([^"]+)"\)', self.script), ['x', 'y', 'z'])
        self.assertIn('jsonsave("layout_complete.json",completion);', self.script)

    def test_native_schema_and_phase_fail(self):
        result = subject.memory_admission(self.report, 103, 1000)
        self.assertFalse(result['memory_estimate_gate_pass'])
        self.assertAlmostEqual(result['cpu_phase_gib']['Data_Collection_Bytes'], 641.4387458562851)
        self.assertAlmostEqual(result['yee_nodes_millions'], 1147.83)
        self.assertIn('NATIVE_MEMORY_WARNING', result['reasons'])

    def test_unknown_phase_blocks(self):
        report = copy.deepcopy(self.report)
        report['report']['Approximate_Memory_Requirements'].pop('Data_Collection_Bytes')
        with self.assertRaises(ValueError):
            subject.memory_admission(report, 103, 1000)

    def test_cap_small_ram_and_disk(self):
        report = copy.deepcopy(self.report)
        report['report']['Approximate_Memory_Requirements'].update({key: 8 * subject.GIB for key in subject.PHASES})
        report['report']['Approximate_Memory_Requirements']['Alert'] = ''
        report['report']['Memory_Recommended'] = 8 * subject.GIB
        result = subject.memory_admission(report, 10, 50)
        self.assertEqual(result['cap_gib'], 7)
        self.assertIn('CPU_PHASE_EXCEEDS_CAP', result['reasons'])
        self.assertIn('DISK_BELOW_FSP_ONLY_MINIMUM', result['reasons'])

    def test_template_mutation_is_guarded(self):
        with self.assertRaises(ValueError):
            subject.replace_once('nothing', 'missing', 'replacement')

    def test_native_axes_require_monotonic(self):
        with self.assertRaises(ValueError):
            subject.axis_summary({'axes': {'x': [0, 1, 1], 'y': [0, 1], 'z': [0, 1]}})

    def test_actual_native_matrix_encoding(self):
        vector = {'_complex': False, '_type': 'matrix', '_size': [3, 1], '_data': [0, 1, 2]}
        self.assertEqual(subject.numeric_vector(vector), [0, 1, 2])

    def test_one_frequency_native_scalar(self):
        self.assertEqual(subject.numeric_vector(599584916000000.0), [599584916000000.0])

    def test_native_matrix_dimension_mismatch_blocks(self):
        vector = {'_complex': False, '_type': 'matrix', '_size': [3, 1], '_data': [0, 1]}
        with self.assertRaises(ValueError):
            subject.numeric_vector(vector)


if __name__ == '__main__':
    unittest.main()
