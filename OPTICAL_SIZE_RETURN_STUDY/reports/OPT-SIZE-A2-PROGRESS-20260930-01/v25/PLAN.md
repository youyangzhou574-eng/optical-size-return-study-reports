# D3 Existing-Data Phase Diagnostic

Goal: implement only D3_DISCRETE_PHASE_CONFIRM_OFFLINE_01 requested in complete Pro agent f001159c-aeab-4b52-ab42-00e7c8896b0e.

Scope: local saved D3 fields/coordinates/fit, and existing numerical-permittivity data only after actual frequency/dt/fit identity validation. No remote session, CAD, solve, modified FSP, new material query, new residual decomposition, or changed acceptance curve.

Method: choose one fixed longest uniform PDMS field window for all 91 wavelengths, away from interfaces and mesh transitions. Extract complex k by a least-squares standing-wave recurrence, preserving every wavelength. Compare continuous k and the documented finite-dz/dt dispersion relation. Keep original interface impedances and all other phases in a normal-incidence TMM diagnostic; change only the PDMS propagation phase integrated across existing z intervals.

Validation: first RED then focused tests for continuum limit, standing waves, degenerate/nonuniform rejection, material identity, window selection, unchanged TMM agreement with the existing tmm library, and clipped phase integration. Existing scientific output hashes must remain unchanged.

Outputs: full 91-point complex k/phase and R/T diagnostic CSV, window/node coordinates, summary with limitations/source SHA, tests and original review. No acceptance upgrade; numerical epsilon is not inferred from field. A phase-only diagnostic is not an exact engine transfer operator or convergence test.

Status: review/scope inspected; no previous phase operation receipt exists. Tests written, implementation pending.
