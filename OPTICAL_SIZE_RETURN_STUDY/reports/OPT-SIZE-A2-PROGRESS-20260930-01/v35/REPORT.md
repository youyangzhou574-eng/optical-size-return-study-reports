# v35: Human Requests Original Cell, Thicker Fe and Coarser Geometry-Aware Mesh

Project OPTICAL_SIZE_RETURN_STUDY; Report ID OPT-SIZE-A2-PROGRESS-20260930-01.
This is a PLAN FOR REVIEW ONLY. No new geometry/FSP/CAD or FDTD execution.

## Latest Human Constraints Supersede v34's Proposed Next Route

After v34 was sent, the user rejected a smaller computational cell and asked
whether Fe2O3 could be thickened to approximately 50 nm, whether coarser mesh
could be assigned according to geometry, and asked for one proposal discussed
with Pro. The user accepts some accuracy sacrifice for practical progress.

No smaller solver cell, Bloch cell reduction, or periodicity representation
change is permitted. Original cell extents remain P15 9 x 5.196152423 um,
P30 18 x 10.392304845 um. A restricted observation monitor is not a smaller
solver cell, but any tile-based integration still needs its native proof.

v34 already has an actual delivered user message
fc3deda1-7dec-4bdc-80e3-565abc591f7f, and remains an authentic resource STOP.
The latest human change will be sent after its in-flight response finishes;
no second concurrent request or replacement/resend of that report is made.

## One Proposed Exploratory Package, Not Approved Parameters

**Candidate physical model:** Fe2O3 nominal normal thickness exactly **50 nm**
for BOTH P15 and P30. PDMS core side/height and the 100 nm ITO layer remain
unchanged. True parent core -> normal offset 100 nm for ITO -> normal offset
150 nm for outer Fe -> periodic copies -> protected halo clipping. Do not
coat an already clipped polygon, independently stretch the triangle, or
double-count the blanket/pillar overlap. Fe blanket z=100..150 nm and outer
pillar top h+150 nm = 9.15 um. Source/control plane clearances must be verified
against these new extents; no silent plane or PML change.

This doubles the previous 25 nm Fe thickness and changes the physical problem.
It is not a numerical-only memory optimization. Absorption/resonances need not
change monotonically; old 25 nm curves cannot validate or replace new 50 nm
results. Compare sizes only at the same 50 nm thickness. No claim about a
25-to-50 nm thickness effect is allowed without a separate matched comparison,
which is NOT requested or authorized here.

**Proposed mesh for original cells:**

| Region / axis constraint | BASE | FINE |
| --- | --- | --- |
| Coated-pillar bbox XY | 40 / 40 nm | 30 / 30 nm |
| Coated-pillar bbox Z | 30 nm | 22.5 nm |
| Flat ITO/Fe/PDMS interface, Z override only | 20 nm | 15 nm |
| Bulk PDMS/water | inherited automatic accuracy 2, no explicit whole-cell fine override | same |

The pillar bbox retains XY outer-coating extent plus 80 nm, z=-50 nm..h+200 nm.
The planar override retains full-cell XY and z=-50..200 nm, Z only. This is a
rectangular Cartesian override strategy, NOT a fictitious triangle-conformal
shell-only fine mesh with a separately coarse core inside the same bbox.
Overlapping overrides use the finer constraint and may couple whole axis
projections. Actual native axis vectors and per-phase system memory, not ideal
shell volumes, determine whether the proposed spacing is realized.

**Mesh-growth candidate:** change inherited allowed size increase factor from
1.0 to **1.2**, solely if Pro verifies the property's supported semantics and
accepts the numerical change. The present 1.0 was retained in v34, whose X/Y
axes are uniform ~15 nm. There is no causal proof or native trial of 1.2.
Never silently preserve 1.0 while claiming adaptive bulk coarsening, or silently
change it while claiming all previous grid settings are frozen.

Conformal Variant 0, source 350-800 nm, X polarization, original BC/PML,
2900 fs/1e-8 and all eight monitors at 500 nm remain candidates unchanged.
No static probes, 10-point spectrum, AM1.5G integral, J10 or photocurrent claim.

## Memory Illustration Is Not Admission

Actual v34 P30_FINE original-cell running estimate is 185.717566844 GiB,
including 153.653892066 GiB internal fields/index and two 15.855507240 GiB
volume monitors. It was NOT run as an FDTD simulation.

Merely doubling actual XY spacing from 15 to 30 nm would give an idealized
factor of 4 in dominant cell counts; doubling all three dimensions would give
factor 8. Dividing the old total suggests illustrative 46.43 or 23.21 GiB,
respectively. These are NOT installed-v241 estimates: bulk/PML/flat-interface
grids, constrained automatic meshing, monitor coordinates, thickness change,
source buffers, collection and export allocation can defeat this scaling.

Goal: a native estimate comfortably below 64 GiB, preferably below 48 GiB for
working headroom. No candidate is admitted by the arithmetic above. Exact cap
remains min(64 GiB,.70*startup free), with all-phase and disk gates; conformal
warning remains STOP until specifically adjudicated, not ignored because a
nominal estimate looks lower. No heavy 3D getter before allocation admission.

## Accuracy and Claims

The user accepts lower numerical accuracy, but this is not permission to call
an unverified value converged. Suggested reporting tiers for Pro to adjudicate:

- Existing strict qualification keeps the 2% paired Fe500 rule, the near-zero
  absolute 2e-5 rule and abs(size difference)>u15+u30. No 5% PASS substitution.
- If the user/Pro approves an exploratory tier, a paired deviation between
  2% and 5% may be shown only as **coarse-mesh exploratory data**, never as a
  strict PASS, converged result, photocurrent or established size effect.
- More than 5%, negative/nonfinite/unassigned material values, or failed
  direct/net or four-material closure blocks physical interpretation and
  production qualification. Pro must specify any alternative scientific scope
  explicitly; implementation must not quietly delete a failed gate.

The 50 nm shell with 30 nm XY nominal spacing does not guarantee two native
samples across every normal direction. Conformal/native material ownership,
top/sidewall resolution and actual monitor sampling need explicit scrutiny.
Increasing the macroscopic pillar side does NOT scale the illumination
wavelength or unchanged ITO thickness, so doubling grid spacing solely from
the larger pillar is not an accuracy proof.

## Required Consolidated Pro Decision

1. Accept/reject this one 50 nm physical candidate and give the exact final
   normal thickness; no smaller computational cell or extra thickness case.
2. Give one native-executable Cartesian mesh, explicitly accepting or correcting
   the 40/40/30 BASE and 30/30/22.5 FINE bbox plus planar-Z 20/15 scheme and
   growth factor 1.2. Identify thin-layer/material-fit/mesh-frequency conflicts.
3. Re-adjudicate the prior rule forbidding any original-cell trial after v34
   resource failure, in light of the user's explicit original-cell-only request.
   Do not treat the new request as permission to bypass resource STOP.
4. Preserve a clear strict-versus-exploratory claim boundary and all unwaived
   energy/material/resource gates. Give a single bounded validation package,
   native allocation strategy, execution order and STOP rules.
5. Request human confirmation of the exact new thickness/numerical model and
   any scope/budget changes before CAD/solve. Existing four MAIN conditional
   authorizations do not silently expand to arbitrary new physics variants.

## Explicit User-Requested Working Budget

This is explicitly the user's request to reduce repeated small-step questions,
not a platform-quota workaround. Current inclusive approval is 8 h local,
80 local inputs/checks, 10 CAD processes/2 h cumulative CAD; already used
CAD3/10 and 33.0681489 s. Conservative local input bound after this plan and
its illustrative arithmetic is 65/80 (62 previous plus 3 plan/number inputs).
Four science cases remain P15/P30 x BASE/FINE, X polarization; science ledger
MAIN1 DIAGNOSTIC4 RECOVERY0 TOTAL5 stays unchanged, diagnostic quota exhausted.

For a self-contained four-case build-and-reopen validation, eight future CAD
processes plus three used would require inclusive **CAD11**, i.e. one above
the present cap of 10, with no retry buffer. Ask Pro to either fit a concrete
seven-process package into the remaining current allowance or propose this
exact bounded increase for human approval. Cumulative CAD wall cap 2 h and
scientific solve counts are not increased by default. Local remaining 15
checks should be budgeted across the complete plan; state any exact additional
time/check needs once, not piecemeal. No permission is inferred from a request.

All current original inputs/results/runner failures and resource STOP evidence
remain unchanged. New actions in preparing v35: local planning only, CAD0,
remote server sessions0, FDTD0. This document is not a ready-to-run input.
