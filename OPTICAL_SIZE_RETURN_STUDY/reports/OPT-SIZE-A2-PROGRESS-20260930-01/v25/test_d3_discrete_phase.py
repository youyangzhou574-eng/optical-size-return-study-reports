"""Focused tests for the single existing-data phase diagnostic."""
import importlib.util
import unittest
import numpy as np
from tmm import coh_tmm

SPEC = importlib.util.find_spec('d3_discrete_phase')
if SPEC is not None:
    import d3_discrete_phase as phase


class PhaseTests(unittest.TestCase):
    def test_implementation_present(self):
        self.assertIsNotNone(SPEC, 'D3 phase diagnostic implementation missing')

    @unittest.skipIf(SPEC is None, 'Implementation absent in RED phase')
    def test_discrete_continuum_limit(self):
        f, n = 299792458 / 525e-9, 1.43 + .001j
        k = phase.discrete_k(f, 1e-20, 1e-12, n*n)
        np.testing.assert_allclose(k, 2*np.pi*f*n/299792458, rtol=1e-8)

    @unittest.skipIf(SPEC is None, 'Implementation absent in RED phase')
    def test_standing_wave_recovers_complex_k(self):
        z = np.arange(301)*20e-9
        k = 17e6 + 170j
        e = np.exp(1j*k*z) + .8j*np.exp(-1j*k*z)
        result = phase.extract_k(z, e)
        np.testing.assert_allclose(result['k'], k, rtol=1e-8, atol=1e-4)
        self.assertLess(result['recurrence_relative_l2'], 1e-12)

    @unittest.skipIf(SPEC is None, 'Implementation absent in RED phase')
    def test_zero_field_and_nonuniform_rejected(self):
        z = np.arange(10)*20e-9
        with self.assertRaises(ValueError):
            phase.extract_k(z, np.zeros(10, complex))
        z[4] += 1e-9
        with self.assertRaises(ValueError):
            phase.extract_k(z, np.ones(10, complex))

    @unittest.skipIf(SPEC is None, 'Implementation absent in RED phase')
    def test_uniform_window_fixed_material_and_interface_exclusion(self):
        z = np.r_[np.arange(-10e-6, -1e-6, 20e-9), np.arange(-1e-6, .1e-6, 10e-9)]
        eps = np.full((len(z), 2), 1.43**2, complex)
        selected = phase.uniform_window(z, eps, np.array([1.43**2]*2))
        self.assertGreater(z[selected[0]], -10e-6)
        self.assertLess(z[selected[-1]], 0)
        self.assertGreater(len(selected), 100)
        self.assertLess(np.ptp(np.diff(z[selected])), 1e-18)

    @unittest.skipIf(SPEC is None, 'Implementation absent in RED phase')
    def test_phase_only_tmm_matches_library_when_unchanged(self):
        n = np.array([1.33+.003j, 1.43+.0001j, 1.8+.03j, 2.7+.08j, 1.33+.003j])
        d = np.array([10000., 100., 25.])
        delta = 2*np.pi*n[1:4]*d/525.
        r, t = phase.phase_tmm(n, delta)
        ref = coh_tmm('p', n, [np.inf, *d, np.inf], 0., 525.)
        np.testing.assert_allclose([r,t], [ref['R'],ref['T']], rtol=1e-12, atol=1e-12)

    @unittest.skipIf(SPEC is None, 'Implementation absent in RED phase')
    def test_numerical_material_identity_guard(self):
        f = np.array([4e14, 5e14]); fit = np.ones((2,4), complex)
        q = {'f':f[:,None], 'actual_dt':np.array([1e-17]), 'eps_fit':fit, 'eps_numerical':fit}
        phase.validate_coefficients(q, f, 1e-17, fit)
        with self.assertRaises(ValueError):
            phase.validate_coefficients(q, f, 2e-17, fit)
        q['eps_fit'] = fit + .01
        with self.assertRaises(ValueError):
            phase.validate_coefficients(q, f, 1e-17, fit)

    @unittest.skipIf(SPEC is None, 'Implementation absent in RED phase')
    def test_phase_integral_preserves_ten_um_on_nonuniform_mesh(self):
        z = np.array([-11e-6, -10e-6, -8e-6, -3e-6, 0., 1e-6])
        links = phase.pdms_links(z)
        self.assertAlmostEqual(float(links['width'].sum()), 10e-6, places=18)
        self.assertTrue(np.all(links['width'] <= links['dz']))

    @unittest.skipIf(SPEC is None, 'Implementation absent in RED phase')
    def test_monitor_subgrid_exact_mapping(self):
        grid = np.arange(545)*20e-9
        selected = phase.validate_field_grid(grid[35:510], grid)
        np.testing.assert_array_equal(selected, np.arange(35,510))
        bad = grid[35:510].copy(); bad[20] += 1e-9
        with self.assertRaises(ValueError):
            phase.validate_field_grid(bad, grid)


if __name__ == '__main__':
    unittest.main()
