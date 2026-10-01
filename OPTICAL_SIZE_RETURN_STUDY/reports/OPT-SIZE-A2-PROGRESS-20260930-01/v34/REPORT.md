# v34: P30 Fine 500 nm Local-Bbox Native Preflight

Report ID: OPT-SIZE-A2-PROGRESS-20260930-01. Project: OPTICAL_SIZE_RETURN_STUDY.
This is a new non-solving evaluation after explicit human resume, not a
resubmission of v33 or a restart of the closed Flat diagnostics.

## Decision

**STOP: the original P30 supercell is still over the unchanged resource cap.**
No FDTD solve, reopen, full 3D index extraction, or automatic retry was started.
The candidate remains NOT_READY and is not a scientifically accepted result.

## What Actually Ran

One native v241 CAD process (PID 51212), true exit 0, wall time 13.0499828 s.
The small completion JSON confirms layout mode and one recorded frequency.
Stdout and stderr are both empty. XML is absent and XML errors remain null,
not an invented XML error count of zero. CAD exit, completion, native outputs,
and transfer receipts are separate evidence.

Server snapshot UTC 2026-10-01T19:37:46.0827217Z; CAD start UTC
2026-10-01T19:37:47.8441173Z; server end UTC 19:38:00.9735468Z.
Local controller completion UTC 19:34:19.3124267Z. These clocks are kept
separate and have not been adjusted. The local controller and worker both
returned actual exit 0 within the 25 s bounded local wait.

Before this request, the exact previous remote host PID 50304 was confirmed
absent. The new remote host PID 46404/birth UTC 19:37:45.1514870Z has only a
local-session-closed receipt; its remote disappearance was not independently
checked. No additional session was opened just to chase that proof.

## Frozen Candidate

- P30 original solver cell: 18 x 10.392304845413264 um; same protected geometry.
- Fine overrides: dx/dy/dz = 15/15/11.25 nm.
- The previous whole-cell `flat_coating_mesh` was deleted.
- Each of the **14 outer Fe-coated periodic geometry pieces** received a
  native-vertices-derived XY bbox plus 80 nm outward buffer. The preserved
  manifest has piece counts [14,18,14] for PDMS/ITO/Fe; 18 is not the Fe count.
- Bbox Z bounds: -50 nm to 9.2 um. Flat interface: full-cell XY, override Z only,
  -50 nm to 200 nm, dz 11.25 nm; no inactive X/Y maximum-step properties.
- Auto non-uniform accuracy 2, Conformal Variant 0, and inherited mesh allowed
  size increase factor **1.0** were read back and not changed.
- Broadband source still 350-800 nm; all eight monitor objects use one global
  custom frequency, 599584916000000 Hz (500 nm). No 10-point or J10 reversion.
- Maximum time 2900 fs and auto shutoff 1e-8 unchanged. Geometry, material fit,
  BC/PML, source normalization, field components and tile extent unchanged.
- No solve, `runanalysis`, layout/result cycling, or full 3D data getter.
- Native index/Yee/material translation equivalence remains PENDING; the
  nominal one-third-X tile is not permission to multiply a native result.

## Actual Native CPU Estimate

Startup free RAM was 105.23796081542969 GiB; startup D disk free was
2609.1280059814453 GiB. The cap is min(64, 0.70*free) = **64 GiB**.
These are admission snapshots, not continuously monitored current RAM.

| Item | Native estimate GiB |
| --- | ---: |
| Initialization and mesh | 0.15625 |
| Internal electromagnetic fields and refractive index | 153.65389206632972 |
| REP_TILE_E | 15.855507239699364 |
| REP_TILE_INDEX | 15.855507239699364 |
| Four flux monitors, combined | 0.19957953691482544 |
| Running simulation | 185.71756684407592 |
| Recommended | 185.7175668440857 |
| Data collection, literal native phase field | 63.821414947509766 |
| FSP saved monitor data | 31.71112859249115 |

The literal collection field is retained as reported. It is NOT summed with
or substituted for the running field, and is not an empirical measured peak.
Export/analysis allocation and total raw-output disk admission remain pending.
The native conformal reliability warning is also preserved as a STOP reason;
it has not been ignored, weakened or turned into a PASS margin.

The preceding whole-override/10-point estimate was 472.2579704867676 GiB
running, 641.4387458562851 GiB collection, and 151.3859523879364 GiB internal
fields/index. Each 10-point volume monitor was 159.36551123857498 GiB.
Thus one point did reduce monitor memory about tenfold. It did NOT reduce the
underlying Cartesian solver grid enough to admit the current supercell.

## Native Axis Evidence

The complete, small native coordinate vectors are in `native_mesh_axes.json`.
They were obtained with layout-mode `getresult("FDTD","x/y/z")`, not inferred
from override settings, interpolated, or reconstructed from ideal shell volume.

| Axis | Points | Cells | Min step nm | Max step nm |
| --- | ---: | ---: | ---: | ---: |
| X | 1201 | 1200 | 14.999999999975293 | 15.000000000000703 |
| Y | 697 | 696 | 14.9314724790419 | 14.931472479047406 |
| Z | 1347 | 1346 | 11.239368165190559 | 25.862068965517693 |

The system report independently displays 1142.71 million Yee nodes. Its
rounded reported count is kept separate from the layout-axis cell product.
X/Y are nearly uniform across the full cell despite localized bbox objects.
Cartesian axis coupling and inherited growth factor 1.0 are relevant diagnostic
constraints. This is not an independent causal proof that changing that one
factor would resolve the memory issue; it has not been changed or tested.

## Integrity, Tests and Budget

Protected mother: 560994 bytes,
SHA256 61B24C378622FDD91E0F4D02F0E80F47BF3103E4E02AD8E45FBB0F31491D16E0,
unchanged locally and remotely. New layout candidate: 619120 bytes,
SHA256 183869E49E790690815D8215D43A06CB4C9F6C8D3EF9C0158F2575EC23AE67E3.
All eight transferred files matched native bytes/SHA; no binary is the sole
delivery artifact.

Thirteen focused local tests now pass. Two production PS scripts parse with
zero errors; bounded response/no-kill/identity guards were checked. The initial
local Fe count mismatch was fixed against the preserved structured manifest
BEFORE any CAD. The post-CAD local parser initially assumed plain lists, but
v241 emits real vectors as {_type:matrix,_complex:false,_size,_data} and a
one-frequency table as a scalar. Three RED/GREEN regression cases cover that
format. Only the local parser was repaired; no native CAD or science rerun.
An initial command path error occurred before the controller or any session
started; the existing Windows PowerShell executable was then used.

Conservative local input/check upper count: 62/80, including 40 prior inputs,
13 pre-CAD checks, 3 post-CAD encoding cases, four native evidence-schema inputs,
one public whitelist input and one final integrity audit. CAD cumulative actual count is
**3/10**, wall time **33.0681489 s / 7200 s**; the inclusive budget was not reset.
Science ledger is unchanged MAIN1/6, DIAGNOSTIC4/4, RECOVERY0/2, TOTAL5/12.
No failure erased an event. The second original-cell P30 CAD is unused and
must not be automatically reallocated following this resource STOP.

## Consolidated Review Request

Please consume this native resource failure and give one bounded next plan,
without reopening original-cell mesh trials. The existing nominal rectangular
translation candidates are P30 6 x 10.392304845 um and P15 3 x 5.196152423 um.
Native source/material/grid equivalence is NOT proven. Specify the single
preferred representation, required native checks and area/flux normalization,
and explicitly retain the 500 nm-only four-case paired 2%/near-zero rules and
unchanged direct/net and four-material closure gates.

Identify whether inherited growth factor 1.0 needs a separately declared
numerical-mesh change; do not silently alter it or claim ideal shell-only mesh.
Retain cap min(64 GiB, .70*free), all-phase admission, conformal warning STOP,
no retry and the consumed CAD accounting. Give the necessary human approval
request for a smaller computational cell and any CAD reallocation. This report
does not authorize that representation or another native process.

**The user explicitly requested more bounded working budget to reduce repeated
questions.** Carry forward the approved inclusive 8 h/80 local inputs/10 CAD/
2 h CAD scope; if the next complete verification package cannot fit the seven
unspent CAD processes or 18 remaining conservative local inputs/checks, state exact
additional time/check/CAD needs and purpose in this normal report response.
No platform-quota change, extra solve/case/rank, or relaxed resource/science gate
is requested or assumed. Local ordinary implementation errors remain local.

Historical Flat D3 NOT_QUALIFIED/root-not-unique conclusions, original runner
failures and all protected results remain unchanged. No new absorption result
was produced by this preflight.
