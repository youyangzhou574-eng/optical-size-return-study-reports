# OPT-SIZE-A2-PROGRESS-20260930-01 v25

## Sole requested D3 discrete-phase confirmation completed offline

This completes D3_DISCRETE_PHASE_CONFIRM_OFFLINE_01 requested by Pro agent f001159c-aeab-4b52-ab42-00e7c8896b0e after its actual v24 review. No server session, CAD, solve, new material query, rerun, modified FSP, residual decomposition, or changed acceptance reference occurred. Budget remains MAIN1/6 DIAGNOSTIC4/4 RECOVERY0/2 TOTAL5/12. No further solver authorization is requested or inferred.

## Actual result

All 91 frequencies retained. One fixed, material-validated uniform PDMS window has 402 nodes, z=-9.9041564792176046e-06 to -2.9584352078238749e-07 m, dz=2.3960880195599045e-08 m. Actual dt=3.3973566775471255e-17 s. Monitor z has 475 nodes, an exact subset of the 545 saved full-grid z nodes, with no interpolation. Sample-grid convention 451/261/545 remains distinct from p0 engine counts 452/262/560.

Median relative complex-k discrepancy:

| Comparison | Median |
| --- | ---: |
| Extracted field k versus continuous k | 0.0048943759801793017 |
| Extracted field k versus discrete k | 1.2081375231277069e-07 |

Maximum fitted recurrence relative L2 residual: 2.5319080348476995e-06. Exact complex values, forward/backward wave-fit residuals, epsilon_dt, frequency/dt and PDMS propagation phases are in phase_and_RT_91.csv. Do not read the median as a uniform bound over all wavelengths.

## Phase-only reference comparison, diagnostic only

| Quantity | Original continuous TMM weighted/max | PDMS discrete-phase diagnostic weighted/max |
| --- | --- | --- |
| R | 0.016631656495264709 / 0.068939730354361878 | 0.0034339601768928435 / 0.017494400701086127 |
| T | 0.011084749900039619 / 0.025323458413064714 | 0.001811458894339454 / 0.020334415206653689 |

Weighted discrepancies decline by 79.35286736% for R and 83.65809864% for T. Diagnostic worst R occurs near 439.99999999999994 nm; diagnostic worst T at 355 nm. R still exceeds both original .002/.01 criteria; T meets .002 weighted but fails .01 maximum. Even this diagnostic reference is not an overall pass. The unchanged original R/T and Fe2O3 acceptance failures remain failures.

The field k closely follows the finite-dz/dt relation, and changing only PDMS phase removes much of the R/T weighted discrepancy. This supports accumulated discrete propagation in the thick PDMS as an important remaining contributor. It does not prove a unique root, a complete engine transfer model, or paired convergence.

## Method and independent checks

Complex field k comes from least-squares E[i-1]+E[i+1]=2*cos(k*dz)*E[i], which accommodates a superposition of forward/backward waves. No single-wave phase unwrap, field-fitting epsilon, spectral deletion, or per-wavelength window selection. Continuous k=2*pi*n/lambda. Discrete k solves the documented Yee relation with saved actual dt, dz and existing numerical epsilon.

Existing numerical epsilon is reused only after source SHA and exact actual frequency/dt/all-material-fit identity checks against D3. It is not a new index evaluated for an old field. The theoretical relation is documented by [Ansys getnumericalpermittivity](https://optics.ansys.com/hc/en-us/articles/360034930093-getnumericalpermittivity-Script-command). At normal incidence, k=2/dz*asin(dz*sqrt(epsilon_dt)*sin(pi*f*dt)/(c*dt)).

For phase-only TMM, original fitted interface impedances and ITO/Fe2O3 phases stay unchanged. Only PDMS propagation phase is replaced by the local discrete-k phase integral over original ten-micron PDMS intervals. The existing tmm library supplies Fresnel and power APIs. With phases unchanged, the implementation reproduces original continuous TMM control-normalized R/T to <=1e-10 at every frequency; a separate synthetic complex-index test reproduces coh_tmm to 1e-12. This diagnostic does not replace the original source/control normalization or reference curves.

Nine focused tests passed after RED. One initial precondition failure incorrectly required monitor and full-grid arrays to have equal lengths (475 versus 545); preserved error and a new exact-subset guard/test resolve it without interpolation. That first attempt produced no result directory and no phase spectra. One full successful phase calculation then exited 0. Source/old-analysis hashes were unchanged before and after. Local Python initially needed the repository's existing _deps/tmm on sys.path; no installation or account change. A read-only dependency locator wait was cancelled without opening a server session.

## Boundaries retained

Original D3 MPI/runner/task remain 0/-1/1, original scope bug preserved; protected freeze and non-solving CAD export are not repeated. D3 direct/net and independent material closure pass the original frozen gates, while R/T and Fe2O3 against the original continuous TMM remain FAIL. NOT_QUALIFIED, root NARROWED_BUT_NOT_UNIQUE and paired convergence NOT_YET_TESTED stay unchanged. A stopping-threshold sensitivity comparison is not proof of zero time error at every wavelength.

Phase-only TMM omits an exact nonuniform-grid/interface update operator and is only a localization diagnostic. No residual is added to absorption, no data are clipped/rescaled/deleted, no center line is represented as a new independently measured 3D volume. Returning to 1.5 versus 3 um triangular pillars is a future proposal, not authorization to create/run new science cases or spend the exhausted diagnostic budget.

## Original immutable evidence

All D3 raw, original gates, source/coordinate/material data and original closeout evidence remain at [v24 fixed commit](https://github.com/youyangzhou574-eng/optical-size-return-study-reports/tree/772960d978929234638ca5d4be02ac47944675c9/OPTICAL_SIZE_RETURN_STUDY/reports/OPT-SIZE-A2-PROGRESS-20260930-01/v24). No old raw is re-uploaded or reconverted. Summary source SHA values retain the correspondence; v25 contains only new phase outputs, coordinates, implementation/tests, scope and complete Pro review.

Request: accept or narrowly correct this final offline phase confirmation, then issue the bounded flat-diagnostic closeout and describe any future size-comparison proposal separately. No automatic new solve, grid/PML/time/budget change or qualification upgrade.
