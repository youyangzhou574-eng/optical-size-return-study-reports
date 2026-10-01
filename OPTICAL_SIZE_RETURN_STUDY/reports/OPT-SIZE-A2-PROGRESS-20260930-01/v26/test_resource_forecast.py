import math
import unittest

import resource_forecast as forecast


class ForecastTests(unittest.TestCase):
    def test_gib_conversion(self):
        self.assertEqual(forecast.gib(1024 ** 3), 1)

    def test_double_complex_payload(self):
        self.assertEqual(forecast.field_bytes(100, 91, 3), 436800)
        self.assertEqual(forecast.field_bytes(100, 91, 6), 873600)

    def test_reject_invalid_dimensions(self):
        for args in ((0, 91, 3), (100, 0, 3), (100, 91, -1)):
            with self.assertRaises(ValueError):
                forecast.field_bytes(*args)

    def test_exact_ratio_does_not_add_roundoff_cell(self):
        self.assertEqual(forecast.nodes(9, 0.015), 602)
        self.assertEqual(forecast.nodes(18, 0.015), 1202)

    def test_piecewise_z_includes_all_zones(self):
        zones = [(-11.5, -10, .1), (-10, -.2, .025),
                 (-.2, 9.325, .015), (9.325, 10.325, .1)]
        self.assertEqual(forecast.zone_nodes(zones, -11.5, 10.325), 1054)

    def test_control_volume_does_not_include_pml(self):
        zones = [(-11.5, -10, .1), (-10, -.2, .025),
                 (-.2, 9.325, .015), (9.325, 10.325, .1)]
        self.assertEqual(forecast.zone_nodes(zones, -10.155, 9.325), 1031)

    def test_production_control_planes_match_existing_pillar_mapping(self):
        zones = [(-11.5, -10, .025), (-10, -.2, .025),
                 (-.2, 9.325, .015), (9.325, 10.325, .025)]
        self.assertEqual(forecast.zone_nodes(zones, -10.35, 9.475), 1049)

    def test_fixed_source_and_flux_planes_are_outside_nominal_pml(self):
        pml_min_end = -11.5 + 8 * .025
        pml_max_start = 10.325 - 8 * .025
        for plane in (-11.15, -10.85, -10.35, 9.475, 9.825):
            self.assertGreater(plane, pml_min_end)
            self.assertLess(plane, pml_max_start)

    def test_fine_improves_all_directions(self):
        base = [.02, .02, .015, .025, .1]
        fine = forecast.refine(base, .75)
        for a, b in zip(base, fine):
            self.assertAlmostEqual(b / a, .75)

    def test_solver_memory_is_aggregate_not_divided_by_ranks(self):
        self.assertEqual(forecast.engine_bytes(1000, 160), 160000)

    def test_tiling_without_halo_does_not_reduce_aggregate_payload(self):
        self.assertEqual(forecast.field_bytes(100, 91, 3),
                         sum(forecast.field_bytes(n, 91, 3) for n in (20, 30, 50)))

    def test_nominal_cfl_is_not_native_dt(self):
        nominal = forecast.cfl_dt(.02, .02, .015)
        actual = 3.3973566775471255e-17
        self.assertAlmostEqual(nominal, 3.398022760620957e-17, delta=1e-30)
        self.assertNotEqual(nominal, actual)
        self.assertLess(abs(nominal / actual - 1), .001)

    def test_runtime_uses_full_physical_limit(self):
        seconds = forecast.runtime_seconds(100, 1000, 1000)
        self.assertEqual(seconds, 100)
        self.assertGreater(math.ceil(2900e-15 / forecast.cfl_dt(.02, .02, .015)), 85000)

    def test_no_cad_or_start_evidence_means_hold(self):
        self.assertFalse(forecast.release_gate(1, 64, cad_verified=False,
                                             human_start_approved=False))
        self.assertFalse(forecast.release_gate(65, 64, cad_verified=True,
                                             human_start_approved=True))

    def test_forecast_alone_never_certifies_start(self):
        self.assertFalse(forecast.release_gate(1, 64, cad_verified=False,
                                             human_start_approved=True))


if __name__ == '__main__':
    unittest.main()
