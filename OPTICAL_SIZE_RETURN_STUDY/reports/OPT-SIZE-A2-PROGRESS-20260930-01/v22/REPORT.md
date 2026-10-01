# D3 Single-Variable Proposal and Communication Resumption

Report ID: OPT-SIZE-A2-PROGRESS-20260930-01 / v22

Project: OPTICAL_SIZE_RETURN_STUDY

Source: latest paired decision message 3865acd0-799a-4523-8e2d-67e4d1f27952,
read on 2026-10-01T04:39:28.659Z. This is a new D3 recommendation, not another
review of the already accepted v21 offline residual budget.

## Current Authorization

The user has explicitly resumed communication and progress with the paired
decision conversation. Public report delivery is authorized for this independent
optical repository. Neither instruction supplies the specific additional solver
start authorization required by the D3 recommendation.

This package records a proposal only. No D3 CAD input, solver task, engine
request, restart, or budget event has been created. No server session is needed
to prepare or publish these documents. D3 is NOT SOLVER READY.

## Unique Proposed Diagnostic

Use a fresh independent input derived from the immutable D2 pre-solve input.
Only the FDTD automatic shutoff threshold changes from 1e-4 to 1e-8.

Keep the maximum simulation time at 2900 fs and parallelism at 1 MPI x 1 thread.
Keep geometry, four-object one-grid transverse coverage, source, actual fitted
materials, thicknesses, normalization area, mesh, conformal settings, boundaries,
PML, time step, original eight monitors and 91 samples from 350:5:800 nm unchanged.
Do not add static probes. Do not combine this test with a z-grid change.

Baseline D2 frozen input SHA-256:
0C21BE1CA258FE6018EA5619E5F53E6CA1A441EECF2F495BA75B9A5404BBDD3C

The purpose is to discriminate sensitivity to early automatic stopping. D2 had
a 2900 fs configured limit but ended at 170.989 fs with AutoShutoff 7.27365e-5.
The proposed threshold is a diagnostic choice, not proof that D2 stopped too
early or a guarantee that D3 will fix calibration.

If the fixed 2900 fs limit is reached without reaching the new threshold,
record that actual outcome. No automatic time extension, retry, or extra case
is authorized.

## Budget and Human Gate

Current: MAIN1 / DIAGNOSTIC3 / RECOVERY0 / TOTAL4 out of 12.

If this one new diagnostic is explicitly authorized and a real solver request
occurs: MAIN1 / DIAGNOSTIC4 / RECOVERY0 / TOTAL5. This uses the final existing
DIAGNOSTIC slot. Do not increment for preparing documents or inputs, and do not
erase a consumed event after failure. No rerun or additional solver case is
covered by the proposal.

Explicit human authorization of this unique D3 start remains outstanding.
Before any actual start, verify the independent input difference, unchanged
settings, input/code hashes, current resources/license and existing technical
safety conditions; check for an existing request/task/markers to prevent a
duplicate. Preparation and routine closeout should not be fragmented into
repeated approvals. Only real safety blockers or configuration changes need
escalation.

## Existing Evidence and Acceptance

The v20 raw reconstruction and v21 discrete z-budget have already been reviewed.
Do not repeat their downloads, conversions, CAD exports, TMM reconstruction,
witness audit, or further residual/closure decompositions of the same raw.

The transverse witness difference was eliminated in D2. Remaining optical
calibration and closure are not qualified. Current status remains
NOT_QUALIFIED / ROOT_CAUSE NARROWED_BUT_NOT_UNIQUE / PAIRED_CONVERGENCE
NOT_YET_TESTED. The original D2 MPI exit 0, runner exit -1, task result 1 and
export CAD exit UNKNOWN/null remain preserved as separate execution records.

After a future authorized D3, reuse established output analysis once: actual
termination time and stopping reason, all 91 R/T points against the unchanged
actual-fit TMM, Fe2O3 absorption, corrected direct/net consistency, six witness
checks and independent four-material closure. Preserve full complex fields,
actual frequency/coordinates/Yee offsets and signed closure.

Original acceptance gates remain: witness 1e-6; R/T and component TMM weighted
absolute error <=0.002 and max <=0.01; corrected direct/net <=0.002/0.005;
four-material closure <=0.005/0.02. No residual is added back to absorption;
no clipping, normalization repair, changed reference, threshold relaxation,
or promotion of three lines to 3D qualification is permitted.

Outcome interpretation from the new recommendation:

- Both spectra and closure pass: close this fault-isolation stage, then obtain
  authorization for minimal necessary convergence evidence before size comparison.
- Closure improves but R/T fails: finite duration mattered partly; a later
  separate z-grid test is a proposal only, not an automatic next solve.
- Actual evolution is longer but results remain effectively unchanged and fail:
  stop further shutoff tuning and consider the discrete model/grid separately.

## Resource Safety

The old remote FDTD resource/log monitoring scripts are retired. They must not
be restored or used for D3. Do not send rich CIM/Get-Content object graphs or
large persistent buffers across WinRM. Current work is entirely local document
publication. Any future necessary remote preparation uses a short, serial,
bounded primitive response and explicit session-lifecycle evidence. Local
completion is not proof of remote-host termination. No kill, permission/account
change or continuous server RAM polling is authorized here.

## New Delivery Method

Complete reports and readable evidence go into this project-only public GitHub
repository, under fixed version directories. The paired decision conversation
receives one short summary, file list and immutable commit links, not split
long text. These three documents are newly authored and allowlisted; no old
raw, private screenshots, credentials or server routes are republished.

Reader access verification is useful but is not a prerequisite to continue
the authorized workflow. No claim that the decision agent read a GitHub file
will be made unless that was actually verified.

## Requested Response

The D3 scientific recommendation is understood; no repeated justification or
re-audit of v21 is requested. Please identify only any substantive conflict
between this single-variable proposal and the accepted preparation/closeout
conditions. Otherwise the next execution gate is the human's explicit D3
one-start authorization, not another cycle of residual reports.
