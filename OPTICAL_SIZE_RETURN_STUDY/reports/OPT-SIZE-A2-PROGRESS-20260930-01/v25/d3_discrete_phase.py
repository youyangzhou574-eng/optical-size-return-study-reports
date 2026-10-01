"""One local D3 phase diagnostic; never changes the acceptance reference."""
import csv
import hashlib
import json
from pathlib import Path
import numpy as np
from tmm import interface_r, interface_t, T_from_t
from compare_f0_d1 import ROOT, OLD, load_data, weighted_metric
from process_f0_raw import numeric_mat

C = 299792458.
CASE = ROOT/'evidence/a2_preflight_20260930/F0_D3_autoshutoff_20261001/closeout_review06_01'
OP = CASE/'discrete_phase_offline01'


def discrete_k(frequency, dt, dz, epsilon):
    if frequency <= 0 or dt <= 0 or np.any(np.asarray(dz) <= 0):
        raise ValueError('Positive actual frequency/dt/dz required')
    omega = 2*np.sin(np.pi*frequency*dt)/dt
    return 2*np.arcsin(omega*np.sqrt(complex(epsilon))*np.asarray(dz)/(2*C))/np.asarray(dz)


def extract_k(z, field):
    z, field = np.asarray(z), np.asarray(field)
    h = np.diff(z)
    if len(z) < 8 or field.shape != z.shape or not np.isfinite(field).all():
        raise ValueError('Finite complete uniform-window field required')
    if np.any(h <= 0) or not np.allclose(h, h[0], rtol=1e-8, atol=1e-18):
        raise ValueError('Nonuniform field window cannot use uniform recurrence')
    x, y = 2*field[1:-1], field[:-2]+field[2:]
    denominator = np.vdot(x, x).real
    if denominator <= 0:
        raise ValueError('Degenerate zero field')
    coefficient = np.vdot(x, y)/denominator
    k = np.arccos(complex(coefficient))/float(np.mean(h))
    residual = np.linalg.norm(y-coefficient*x)/np.linalg.norm(y)
    return {'k': k, 'cos_kh': coefficient, 'recurrence_relative_l2': float(residual)}


def wave_fit_error(z, field, k):
    offset = np.asarray(z)-np.mean(z)
    basis = np.column_stack((np.exp(1j*k*offset), np.exp(-1j*k*offset)))
    amplitudes = np.linalg.lstsq(basis, field, rcond=None)[0]
    return float(np.linalg.norm(basis@amplitudes-field)/np.linalg.norm(field))


def uniform_window(z, effective, fitted):
    z, effective = np.asarray(z), np.asarray(effective)
    h = np.diff(z)
    if effective.shape != (len(z), len(fitted)) or np.any(h <= 0):
        raise ValueError('Actual coordinate/index mapping mismatch')
    material = np.all(abs(effective-fitted[None,:]) <= 1e-7*np.maximum(1, abs(fitted))[None,:], axis=1)
    mask = np.zeros(len(z), bool)
    guard = 3*np.maximum(h[:-1], h[1:])
    mask[1:-1] = (material[:-2]&material[1:-1]&material[2:] &
        (abs(h[:-1]-h[1:]) <= 1e-8*np.maximum(h[:-1],h[1:])) &
        (z[1:-1] > -10e-6+guard) & (z[1:-1] < -guard))
    groups = np.split(np.flatnonzero(mask), np.flatnonzero(np.diff(np.flatnonzero(mask)) != 1)+1)
    selected = max(groups, key=len)
    if len(selected) < 8:
        raise ValueError('No complete uniform PDMS stencil window')
    return selected


def pdms_links(z):
    z = np.asarray(z)
    h = np.diff(z)
    width = np.maximum(0, np.minimum(z[1:], 0)-np.maximum(z[:-1], -10e-6))
    if np.any(h <= 0) or not np.isclose(width.sum(), 10e-6, rtol=0, atol=1e-15):
        raise ValueError('PDMS ten-micron phase domain incomplete')
    selected = width > 0
    return {'dz': h[selected], 'width': width[selected], 'index': np.flatnonzero(selected)}


def validate_coefficients(q, f, dt, fitted):
    numerical = np.asarray(q['eps_numerical'])
    if numerical.shape != fitted.shape or not np.isfinite(numerical).all():
        raise ValueError('Invalid existing numerical permittivity')
    if (np.asarray(q['f']).reshape(-1).shape != f.shape or
        np.max(abs(np.asarray(q['f']).reshape(-1)-f)) > 1 or
        abs(float(np.asarray(q['actual_dt']).squeeze())-dt) > 1e-29 or
        np.asarray(q['eps_fit']).shape != fitted.shape or
        np.max(abs(q['eps_fit']-fitted)) > 1e-12):
        raise ValueError('Existing dt/f/material coefficient identity mismatch')


def validate_field_grid(z, grid):
    z, grid = np.asarray(z), np.asarray(grid)
    if (not np.isfinite(z).all() or not np.isfinite(grid).all() or
        np.any(np.diff(z) <= 0) or np.any(np.diff(grid) <= 0)):
        raise ValueError('Finite ascending native coordinates required')
    indices = np.argmin(abs(z[:,None]-grid[None,:]), axis=1)
    if len(np.unique(indices)) != len(z) or np.max(abs(grid[indices]-z)) > 1e-15:
        raise ValueError('Monitor native points are not an exact full-grid subset')
    return indices


def phase_tmm(n, delta):
    """Use tmm Fresnel/power APIs; only propagation phases are supplied."""
    n, delta = np.asarray(n), np.asarray(delta)
    if n.shape != (5,) or delta.shape != (3,) or not np.isfinite(delta).all():
        raise ValueError('Complete normal-incidence stack phases required')
    r = interface_r('p', n[3], n[4], 0., 0.)
    t = interface_t('p', n[3], n[4], 0., 0.)
    for i in (2,1,0):
        ri = interface_r('p', n[i], n[i+1], 0., 0.)
        ti = interface_t('p', n[i], n[i+1], 0., 0.)
        propagation = np.exp(1j*delta[i])
        denominator = 1+ri*r*propagation**2
        r, t = (ri+r*propagation**2)/denominator, ti*t*propagation/denominator
    return float(abs(r)**2), float(T_from_t('p', t, n[0], n[4], 0., 0.))


def write_csv(path, rows):
    with path.open('x', newline='', encoding='ascii') as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader(); writer.writerows(rows)


def main():
    out = OP/'results01'
    if out.exists():
        raise ValueError('Existing phase result directory: no repeat or overwrite')
    raw = CASE/'export_raw01'
    sources = [raw/('F0_D3_'+s) for s in ('raw_Yee_and_flux.mat','raw_coordinates.mat','saved_run_information.mat')]
    coefficient = OLD/'localization_decision15_01/F0_actual_grid_dt_numerical_permittivity.mat'
    audit = CASE/'analysis01/comparison_summary.json'
    original = CASE/'analysis01/D3_full_diagnostic_91.csv'
    audited = json.loads(audit.read_text(encoding='ascii'))
    for path in sources+[coefficient]:
        expected = audited['source_hashes'][str(path)]
        if hashlib.sha256(path.read_bytes()).hexdigest().upper() != expected:
            raise ValueError('Existing audited source SHA mismatch: '+path.name)
    hashes = {str(p):hashlib.sha256(p.read_bytes()).hexdigest().upper() for p in sources+[coefficient,audit,original]}
    data = load_data(*sources)
    f, z = data['f'].reshape(-1), data['z'].reshape(-1)
    dt = float(data['actual_dt'].item())
    fitted = np.column_stack([data['nk_'+n]**2 for n in ('PDMS','ITO','Fe','water')])
    q = numeric_mat(coefficient)
    validate_coefficients(q, f, dt, fitted)
    if len(f) != 91 or data['Ex'].shape != (len(z),91) or np.any(data['Ey']) or np.any(data['Ez']):
        raise ValueError('Complete existing scalar Ex spectrum required')
    grid_indices = validate_field_grid(z, data['z_grid'].reshape(-1))
    selected = uniform_window(z, data['index_x']**2, fitted[:,0])
    links = pdms_links(z)
    old = np.genfromtxt(original, delimiter=',', names=True)
    solar = np.loadtxt(ROOT/'evidence/a2_preflight_20260930/solar_reference/ASTMG173.csv',delimiter=',',skiprows=2)
    rows = []
    for j, frequency in enumerate(f):
        wl = C/frequency*1e9
        match = np.flatnonzero(abs(old['wavelength_nm']-wl) < 1e-8)
        if len(match) != 1:
            raise ValueError('Original full-spectrum mapping absent; no interpolation')
        o = old[match[0]]
        n = np.array([data['nk_'+v].reshape(-1)[j] for v in ('water','PDMS','ITO','Fe','water')])
        continuous = 2*np.pi*n[1]/(wl*1e-9)
        dz = float(np.mean(np.diff(z[selected])))
        discrete = discrete_k(frequency, dt, dz, q['eps_numerical'][j,0])
        field = data['Ex'][selected,j]
        extracted = extract_k(z[selected], field)
        delta = 2*np.pi*n[1:4]*np.array([10000.,100.,25.])/wl
        full_phase = np.sum(discrete_k(frequency, dt, links['dz'], q['eps_numerical'][j,0])*links['width'])
        baseline_rt = phase_tmm(n, delta)
        diagnostic_delta = delta.copy(); diagnostic_delta[0] = full_phase
        diagnostic_rt = phase_tmm(n, diagnostic_delta)
        water_loss_k = 2*np.pi*n[0].imag/(wl*1e-9)
        bottom, top = float(data['zbottom'].item()), float(data['ztop'].item())
        factors = np.array([np.exp(4*water_loss_k*(bottom+10e-6)), np.exp(2*water_loss_k*(bottom+10e-6-top+125e-9))])
        original_reference = np.array([o['TMM_R'],o['TMM_T']])
        if np.max(abs(factors*np.asarray(baseline_rt)-original_reference)) > 1e-10:
            raise ValueError('Unchanged diagnostic TMM must reproduce original reference normalization')
        r_diag, t_diag = factors*np.asarray(diagnostic_rt)
        row = dict(wavelength_nm=float(wl),frequency_Hz=float(frequency),actual_dt_s=dt,window_dz_m=dz,
            index_PDMS_real=float(n[1].real),index_PDMS_imag=float(n[1].imag),
            epsilon_dt_real=float(q['eps_numerical'][j,0].real),epsilon_dt_imag=float(q['eps_numerical'][j,0].imag),
            relative_k_field_minus_continuous=float(abs(extracted['k']-continuous)/abs(continuous)),
            relative_k_field_minus_discrete=float(abs(extracted['k']-discrete)/abs(discrete)),
            recurrence_relative_l2=extracted['recurrence_relative_l2'],
            continuous_wave_fit_relative_l2=wave_fit_error(z[selected],field,continuous),
            discrete_wave_fit_relative_l2=wave_fit_error(z[selected],field,discrete),
            extracted_wave_fit_relative_l2=wave_fit_error(z[selected],field,extracted['k']),
            R_D3_original=float(o['R_control']),T_D3_original=float(o['T_control']),
            R_TMM_original=float(o['TMM_R']),T_TMM_original=float(o['TMM_T']),
            R_PDMS_discrete_phase_diagnostic=float(r_diag),T_PDMS_discrete_phase_diagnostic=float(t_diag),
            R_original_signed_error=float(o['R_control']-o['TMM_R']),T_original_signed_error=float(o['T_control']-o['TMM_T']),
            R_diagnostic_signed_error=float(o['R_control']-r_diag),T_diagnostic_signed_error=float(o['T_control']-t_diag))
        for label, value in (('k_continuous',continuous),('k_discrete',discrete),('k_field',extracted['k']),
                             ('phase_continuous_PDMS',delta[0]),('phase_discrete_PDMS',full_phase)):
            row[label+'_real'] = float(value.real); row[label+'_imag'] = float(value.imag)
        if not np.isfinite(list(row.values())).all():
            raise ValueError('Nonfinite spectrum; preserve failure, do not drop points')
        rows.append(row)
    rows.sort(key=lambda r:r['wavelength_nm'])
    wl = np.array([r['wavelength_nm'] for r in rows])
    metric = lambda key: weighted_metric(np.array([r[key] for r in rows]), wl, solar)
    summary = dict(operation='D3_DISCRETE_PHASE_CONFIRM_OFFLINE_01',new_solver_starts=0,remote_sessions=0,cad_starts=0,
        frequency_points=len(rows),window_nodes=len(selected),window_lower_m=float(z[selected[0]]),window_upper_m=float(z[selected[-1]]),
        monitor_field_z_nodes=len(z),full_saved_grid_z_nodes=int(data['z_grid'].size),monitor_grid_mapping='EXACT_NATIVE_SUBSET_NO_INTERPOLATION',
        window_dz_m=float(np.mean(np.diff(z[selected]))),actual_dt_s=dt,
        extraction='Least-squares E[i-1]+E[i+1]=2*cos(k*dz)*E[i]; handles forward/backward superposition without phase unwrap or epsilon field fitting.',
        phase_diagnostic='PDMS propagation phase only; integrate documented local discrete k over original ten-micron material thickness. Original fitted interface impedances and other layer phases unchanged.',
        original_R_metric=metric('R_original_signed_error'),original_T_metric=metric('T_original_signed_error'),
        diagnostic_R_metric=metric('R_diagnostic_signed_error'),diagnostic_T_metric=metric('T_diagnostic_signed_error'),
        median_relative_k_field_minus_continuous=float(np.median([r['relative_k_field_minus_continuous'] for r in rows])),
        median_relative_k_field_minus_discrete=float(np.median([r['relative_k_field_minus_discrete'] for r in rows])),
        max_recurrence_relative_l2=float(max(r['recurrence_relative_l2'] for r in rows)),
        source_sha256=hashes,qualification='NOT_QUALIFIED',root='NARROWED_BUT_NOT_UNIQUE',paired_convergence='NOT_YET_TESTED',
        references=['https://optics.ansys.com/hc/en-us/articles/360034930093-getnumericalpermittivity-Script-command'],
        limitations=['Phase-only TMM is diagnostic, not an exact nonuniform-grid/interface engine transfer operator.',
            'No independent time/grid/PML convergence; a tighter stop sensitivity result does not prove zero finite-time error.',
            'Existing numerical epsilon reused only after matching actual dt, frequencies and all fitted-material values.',
            'Original acceptance references, absorption integrals, curves and thresholds are not changed.'])
    for path, digest in hashes.items():
        if hashlib.sha256(Path(path).read_bytes()).hexdigest().upper() != digest:
            raise ValueError('Original source changed during local diagnostic')
    out.mkdir()
    write_csv(out/'phase_and_RT_91.csv', rows)
    write_csv(out/'uniform_PDMS_window_coordinates.csv',[dict(node_index=int(i),z_m=float(z[i])) for i in selected])
    write_csv(out/'monitor_grid_mapping.csv',[dict(monitor_node_index=int(i),full_grid_node_index=int(g),z_m=float(z[i])) for i,g in enumerate(grid_indices)])
    write_csv(out/'PDMS_phase_links.csv',[dict(link_index=int(i),dz_m=float(h),PDMS_width_m=float(w)) for i,h,w in zip(links['index'],links['dz'],links['width'])])
    with (out/'summary.json').open('x',encoding='ascii') as handle:
        json.dump(summary,handle,indent=2)
    print(json.dumps({k:v for k,v in summary.items() if k!='source_sha256'},indent=2))


if __name__ == '__main__':
    main()
