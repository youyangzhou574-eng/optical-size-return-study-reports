# v36: Legacy solver baseline, local recording, coarser mesh, Fe25

Report ID: OPT-SIZE-A2-PROGRESS-20260930-01
Status: one consolidated scientific/implementation review request; no new CAD or solve.
Target: paired Pro conversation 6aba1cbd-1318-83e8-8628-6dc39e2a903b.

## Latest human direction supersedes the v35 implementation route

The human now explicitly asks for the old solver setup as the baseline, coarser mesh, and the old local-monitor concept. Keep the original large P15/P30 computational cells; the human explicitly rejects a smaller computational cell. First retain the present 25 nm Fe2O3 shell. Do NOT simultaneously implement the proposed 50 nm shell, full-height/full-cell E monitor, or v35 safety/budget revisions. The earlier discussion of a thicker shell was exploratory, not a final production choice. This request authorizes review and local planning, not a server/CAD/solver start.

Please issue one executable, bounded replacement plan, identifying any incompatibility explicitly. Do not simply repeat the v35 Fe50/FULLCELL_E_500 route.

## Verified legacy comparison

Read-only legacy builder: build_indexaudit_1p5_9.lsf, historical 1.5 um side / 9 um high pillars.

| Item | Legacy builder | Present project / constraint |
| --- | --- | --- |
| Computational XY | 9 x 5.196 um | P15 original 9 x 5.196 um; P30 original 18 x 10.392 um |
| Pillar height / PDMS base | 9 / 10 um | unchanged |
| ITO / Fe2O3 | 100 / 25 nm | retain 100 / 25 nm initially |
| Explicit fine override | 20 / 20 / 15 nm; full XY across pillar height | failed present FINE branch uses 15 / 15 / 11.25 nm |
| Solver | FDTD, mesh accuracy 2, XY periodic, z PML | use as baseline; do not copy unsafe old control scripts |
| Maximum time / shutoff | 2900 fs / 1e-4 | maximum remains 2900 fs; current 1e-8 requires an explicit decision before changing |
| Source band | 380-780 nm | current 350-800 nm; do not silently change |
| Component recording | one 500 nm frequency, per-pillar outer-coat bounding boxes plus 80 nm on each XY side, z=0..9.125 um; matching index | restore LOCAL recording concept, not full-height PDMS/water volume by default |
| Flat-film recording | full XY but z=0..0.125 um only | local thin-film recording, not the 10 um PDMS base |

The old local boxes also include pillar PDMS and some nearby water; they are not geometrically Fe-only. Their overlaps and periodic copies need mutually exclusive ownership in absorption integration. Legacy conformal/growth were not explicitly set in that script; their actual old defaults were not independently read back. Current M0/A2 material fits stay frozen; old material card names are not a license to replace them.

The successful old 91-point R/T run removed heavy 3D component monitors. Its historical 12.7 GiB estimate is NOT a verified peak for the old single-wavelength component model. Reducing wavelength count does not remove the solver's field/material grid cost.

## Actual failed native audit already completed; do not repeat it

v34 fixed evidence: commit 97c1edd46f6c1fc334613eb9897419c39a10ce1c in this repository, same report directory /v34.

Present Fe25 P30_X_FINE: original 18 x 10.392 um solver, one 500 nm recorded frequency, 14 true outer-Fe periodic piece boxes padded 80 nm in XY, z=-0.05..9.2 um; fine override 15/15/11.25 nm. A full-XY flat override remained only near the coating. REP_TILE_E and REP_TILE_INDEX recorded a one-third-X observation volume 6 x 10.392 x 19.825 um, NOT a smaller computational cell.

Native audit CAD exited 0 without solving. Actual x/y fine spacing spanned the whole computational axes: 1200 x-cells, 696 y-cells, 1346 z-cells; x all 15 nm, y approximately 14.931 nm. Merely replacing the fine override by local boxes did NOT localize those tensor-grid axes.

Native report, GiB: internal fields/material grid 153.653892066; E 15.855507240; index 15.855507240; running total 185.717566844; literal collection estimate 63.821414948; saved data 31.711128593. Hard resource cap is 64 GiB. A conformal reliability warning also remained. Resource gate FAILED, no solve, native material/boundary proof not completed. Collection estimate is not a measured peak and must not substitute for the failed running estimate.

Nominal periodic geometry checks passed (central geometry mismatch and periodic-edge mismatch zero), but native Yee/material-edge and dynamic boundary validation remain unproven. Preserve the corrected true outer-coat periodic geometry and halo; do not restore the old clipping-at-cell-edge geometry.

## Specific consolidated decisions requested

1. Provide ONE exact original-cell Fe25 mesh prescription for BASE and FINE. Candidate discussion values are BASE 40/40/30 nm and FINE 30/30/22.5 nm, with thin flat-film z-resolution 20/15 nm. They are proposals, not validated settings. Specify each region's bounds and mesh priority. A 25 nm shell may not be resolved by these values: explain whether conformal/native ownership can support this qualitative comparison, or which bounded refinement is indispensable. Do not imply fine-shell boxes leave a coarse XY core when the native tensor grid proves otherwise.
2. Specify accuracy, conformal variant, growth, source band, maximum time and shutoff. Distinguish legacy explicitly set values from unknown defaults. Current growth is 1.0 and shutoff 1e-8; proposed 1.2 or legacy 1e-4 are numerical changes needing stated purpose and gates. Flat D2/D3 time sensitivity is a warning, not proof for these pillars. Keep 2900 fs maximum; no automatic extension/retry.
3. Give exact runtime LOCAL E monitor list/bounds/components/frequency/offset handling, and CAD-only index/material audit if useful. Decide whether matching index can be exported before solve and removed only after native grid/dt/epsilon/Yee equivalence is proven. Account for every allocation before any data getter. No full-height/full-cell E monitor as the default solution. Handle periodic pieces, halo and overlap without double-counting.
4. Reconcile local recording with existing component/direct-net/closure gates. We have NOT approved dropping water/PDMS completeness or manufacturing water absorption as a residual. If local recording cannot prove required four-material closure, identify a native-executable bounded method (for example only if independently valid flux/control-volume accounting), or state the exact scientific scope adjustment needing human approval. Do not relabel a missing gate as PASS. Keep strict 2% paired comparison and old science thresholds unless an explicit separately labeled exploratory tier is adjudicated; exploratory is not convergence or qualified absorption.
5. Specify a single bounded phase order, admission checks and STOP conditions. Does this NEW coarse Fe25/local branch justify reconsidering v34 original-cell resource STOP? The old FINE15 branch remains stopped. Preserve the 64 GiB hard cap, all native runtime/collection/export memory gates, scientific STOP and no active-engine changes. A conformal warning/headroom-policy waiver from v35 has not been applied; adjudicate it explicitly, not silently.
6. Give a bounded whole-package work budget, as REQUESTED BY THE HUMAN to reduce repeated small-step questions. Current approved limits: 8 local hours, 80 local inputs/synthetic checks, 10 CAD processes / 2 hours cumulative; actual CAD used 3 processes / 33.0681489 seconds; conservative local-input upper bound 65. Plan within the remainder if possible; otherwise give exact added CAD/check/time limits and purpose. v35's 11 CAD / 90 checks were recommendations only, not applied. No platform quota increase, RAM-cap increase, automatic extra solve, or budget reset. Science ledger remains MAIN1/6, DIAGNOSTIC4/4, RECOVERY0/2, TOTAL5/12. Existing four conditional MAIN cases do not authorize a changed-physics fifth case.

Please return concrete native-executable parameters and a complete bounded preparation/production sequence, including claims allowed if memory and native shell ownership cannot both pass. Ordinary implementation details will be handled locally; consolidate major scientific/resource decisions in this reply. The executor will first consume and record your full response; no duplicate CAD, no blind retries, no new solve under this request.

## Evidence limits retained

Flat diagnostic is closed NOT_QUALIFIED; do not reopen it. Historical MPI/runner/task conflicts and original receipts are unchanged. The last audit remote host was locally closed but not independently confirmed gone; no new session is opened just to chase it. No current server RAM measurement is asserted. No credentials, private server routes or other project files are included here.
