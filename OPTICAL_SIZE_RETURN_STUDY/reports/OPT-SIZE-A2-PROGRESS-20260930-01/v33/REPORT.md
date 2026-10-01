# OPT-SIZE-A2-PROGRESS-20260930-01 v33

## Latest direct human request: legacy comparison and coarser-grid ruling

The user now explicitly asked us to consolidate the old/new comparison and ask this paired Pro conversation whether doubling pillar side length permits a grid coarser than the legacy grid. This authorizes this report/publication and one consolidated question, NOT new CAD or solver execution. The previous communication pause is lifted for this request only; resource STOP and model-execution pause remain. See LEGACY_NEW_COMPARISON.md for the exact comparison and the requested mesh ruling.

Please address that question directly: the pillar side doubled from1.5 to3um, but height9um, ITO100nm, Fe2O3 25nm and target500nm did not double. Can interior/bulk/water use coarser grids than20/20/15nm while the unchanged thin shells use local/anisotropic refinement? Give actual dx/dy/dz and refinement extents for each region, a paired validation criterion, material-interface risks and native resource checks. Do not automatically double all three steps to40/40/30nm or insist on15/15/11.25nm without showing what scientific observable needs it. No coarser-grid change has been applied.

## User direction: first one recorded wavelength

The user supplied the old-model audit and directly requested: first calculate one wavelength. This supersedes waiting for the user to retrieve old context. We selected500nm as the candidate because the verified legacy component builder explicitly used metrics_lambda=0.5e-6. The user did not specify500nm. There are no new remote, CAD or solver actions in this revision.

Four locally prepared candidate plans now record only f=c/500nm=599584916000000Hz in R/T, Pbottom/Ptop, E and index. The source remains350-800nm, material fits and X polarization are unchanged. This is a one-point observation of the existing broadband solve, not a new monochromatic source. Original period, mesh, control planes, time2900fs, auto1e-8, PML/conformal, native Yee/no downsampling and four-material scope remain unchanged. Tile multiplication remains disabled pending native equivalence.

The four conditional MAIN cases remain P15_X_BASE, P30_X_BASE, P15_X_FINE, P30_X_FINE. No extra diagnostic, Flat, Y or fifth case is authorized. The local P30_FINE one-point LSF is NOT EXECUTED. Historical ten-point files are preserved.

## Actual native resource STOP and why one point alone cannot fix P30_FINE

The ten-point P30_FINE native CPU report is exact4917bytes, SHA9411F62470C764996B05FE0884410642E35FF4843303DAA6750970DA71541CE1. It corresponds to full cell18x10.392304845413264um, local mesh15/15/11.25nm, inherited automatic mesh elsewhere and one-third-X monitor tile6x10.392304845413264um.

| Component | Ten-point native estimate GiB | One-point scalar proxy GiB |
|---|---:|---:|
| Electromagnetic fields and index |151.3859523879364|151.3859523879364 unchanged|
| REP_TILE_E |159.36551123857498|15.936551123857498|
| REP_TILE_INDEX |159.36551123857498|15.936551123857498|
| Four flux monitors combined |1.9872051477432252|0.19872051477432252|
| All monitors combined |320.71937292814255|32.071937292814255|
| Running phase |472.2579704867676|183.6105348514393|
| Collection phase |641.4387458562851|UNKNOWN; no proportional assumption|
| Saved monitor data |318.7321689724922|31.873216897249222 proxy|

The proxy subtracts native monitor bytes from native running bytes, keeps the remainder151.53859755862504GiB, and scales monitor bytes by1/10. It is a read-only arithmetic diagnostic, NOT a new native resource report or measured RAM. Even the unchanged field/index estimate alone exceeds64GiB. No large array was allocated or loaded. Merely reducing the computational cell by3 would not automatically reduce an already one-tile monitor; do not divide all costs by3 or announce PASS.

The original report contains a conformal-memory reliability warning, numeric-string Total_FDTD_Yee_Nodes=1147.83 (million-node display), Memory_Recommended without _Bytes suffix, and Geometry=null. Missing/unknown fields are not zero or PASS. The explicit phase bytes independently justify STOP. Settings readback confirms layout1, ten configured frequencies and dt2.5478700814633336e-17s, not actual saved index/Yee translation equivalence.

## Legacy evidence: same kind of monitor, different acquisition volume

Verified locally in build_indexaudit_1p5_9.lsf: old1.5um-side/9um-height component model used metrics_lambda=500nm, local20/20/15nm override, per-pillar3D E/index and a separate flat-stack pair. Its source380-780nm differs from the current source and is not silently copied. The later91-point broadband builder deleted the heavy volume monitors and kept flux acquisition. Thus91-point R/T memory is not evidence that full3D component spectra are cheap.

The preserved legacy mesh comparison gives a historical resource estimate12.697GiB, not current measured peak, and old engine counts by rank partition. Approximate reconstructed global counts include unresolved halos; do not claim exact old global-grid identity or assign P15 evidence to P30. The old component integration and unresolved periodic/Yee boundary issues do not justify skipping current ownership/closure/equivalence gates.

## Execution, tests and limits preserved

The prior two actual CAD processes count2/8 total and consumed both of P30_FINE's build1+reopen1 slots. CAD1 exit0 had XMLerror1 at the LinearZ inactive downsample-x property. That minor error was fixed locally as the user requested, not escalated. CAD2 native exit0/stderr0 generated fresh report/settings/input files, transferred with exact hashes. Its stdout marker is absent, XML absent/errorsnull, original worker exit1/query_okfalse remain. A post-exit PeakWorkingSet result0 is NOT proof of zero peak. We do not rerun just to improve these receipts.

Cumulative CAD wall20.0181661s; science starts in this package0. A subsequent direct user request for current server memory was fulfilled once with a bounded primitive response,0CAD/0solve/no periodic monitor. It independently confirmed prior host29728 ABSENT. Snapshot serverUTC2026-10-01T18:37:03.1327510Z: total127.243347GiB/free103.234917GiB/used24.008430GiB. This is a dated snapshot, not current live RAM. Latest read host50304/birth2026-10-01T18:37:02.6535111Z is only locally closed, not independently remote-gone. Any next necessary authorized remote action must check its exact four-state identity; no session is opened just to chase its exit.

Single-point support was tested RED (the old generator incorrectly allocated10 frequency slots for1 sample), then GREEN. Full bounded local suite10/10 passed; one new distinct input means known distinct synthetic inputs40/40, not reset. Closed mother and original geometry hashes remain unchanged. The old corrected ten-point LSF and611216-byte FSP remain unchanged. One-point candidates have no actual native property/resource/Yee PASS.

Science ledger is MAIN1/6, DIAGNOSTIC4/4, RECOVERY0/2, TOTAL5/12. Original four authorized MAINs only increment on actual starts. Failed attempts are not erased. Existing all-four native-preflights-before-start and BASE science gates before FINE remain until an explicit revised Pro ruling; no unilateral isolated P15 solve.

## One consolidated decision requested

Please replace the ten-point production observation with a500nm-first, explicitly bounded and implementable package. One wavelength cannot define J_Fe,10 or an AM1.5G spectral integral. Define the correct single-point A_Fe2O3_X(500nm) comparison, absolute/relative mesh uncertainty and size-difference qualification without presenting it as full-spectrum performance or spectral convergence. Preserve finite/actual-f/Yee/material ownership, direct-net and independent four-material closure tolerances unless a separate explicit human-approved scope change is necessary.

Use the real native costs to choose a viable route. Decide whether a P15_BASE-first preparation/start can be released before all four inputs pass preflight, without adding a scientific case or consuming an unauthorized retry. If not, say exactly which of the original four remains the prerequisite. Supply the concrete computational-cell/mesh/monitor architecture and RAM/collection/export/analysis bounds; do not repeat the already failed same-grid full-volume proposal. Any smaller cell, coarser mesh, changed source band or material/closure waiver must be identified as a single explicit human decision, not treated as granted by the sampling request.

The following request is explicitly USER-REQUESTED to reduce repeated approvals: an inclusive operational scope of local8h/80 distinct synthetic inputs and at most10 total CAD processes/cumulative2h for the chosen architecture's non-solving verification and input preparation. Include consumed counts40 inputs,2 CAD and20.0181661s rather than resetting. Permit ordinary implementation fixes locally inside that scope. Retain the current per-case168h operational ceiling unless the chosen safe plan needs a different bounded value. No extra scientific starts or RAM cap enlargement is requested. State remaining usable counts and any changed P30-specific CAD sublimit. Until approved, current limits and STOP remain in force.

## Delivery status

This v33 replaces unpublished local v32 resource-report draft, not a previously delivered report. Its earlier unsent local draft was updated with this latest direct human request before its first publication. v31 minor-error draft was neither published nor submitted and remains cancelled for escalation. Only this normal major-decision report receives a short summary with its fixed GitHub commit. Message delivery, response generation and actual Pro reading are separately evidenced. No claim of Pro reading is made before a real reply. Public CAD receipts omit the account SID; original receipts remain unchanged locally and a sanitization receipt records their full hashes without publishing the omitted value.
