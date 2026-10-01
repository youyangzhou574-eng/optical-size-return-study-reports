# Native Capability Review After Pro Reply 07804891

The complete Pro reply is retained without edits. One v27 submission is delivered and answered; no pending reply remains. This note is not a second Pro submission.

## Current Gate

RUNTIME_STREAMING_AND_MEMORY_EQUIVALENCE_NOT_PROVEN. No remote session, CAD, solve, model/material modification or new scientific budget event occurred in this review.

Pro proposes runtime layer-wise accumulation and retaining only 91x4 integrated spectra plus small audit regions at450/525/650nm. It accepts a bounded local4h/40tests and CAD8processes/2h package, and operational168h/case admission, not extra scientific starts. This is a proposed measurement architecture, not a demonstrated native API.

## Primary Documentation Checked

- https://optics.ansys.com/hc/en-us/articles/360034382454-Analysis-Groups-Simulation-object : conventional analysis groups analyze monitor data via getdata/runanalysis; the documented example runs simulation before analysis.
- https://optics.ansys.com/hc/en-us/articles/53979664687507-Clearing-unwanted-simulation-results : clearing child results takes effect when analysis executes; saves can occur after analysis. This reduces retained output, not proof of reduced engine-time DFT allocation.
- https://optics.ansys.com/hc/en-us/articles/360034902393-Frequency-domain-monitor-Simulation-object : standard frequency-domain monitors have spatial field arrays; memory depends on spatial extent/frequency/components.
- https://optics.ansys.com/hc/en-us/articles/360034915693-Calculating-absorbed-optical-power-Higher-accuracy : component-wise native positions and periodic/interface handling must be respected.

Inference: an ordinary analysis-group loop over z, or exporting one layer at a time, does not by itself demonstrate runtime memory savings. The checked documentation does not establish a supported per-timestep spectral loss accumulator that bypasses all spatial DFT storage. This limited search does NOT prove no possible implementation exists. Require an identified supported interface/implementation plus full engine/DFT/collection/resource evidence before calling it feasible.

For coherent spectral loss, abs(sum_t E(r,t)*exp(i*w*t)*dt)^2 is not interchangeable with sum_t abs(E(r,t))^2 or abs(sum_r E(r,w))^2. A91x4 final output alone does not establish small internal state. An analytic identity/synthetic test alone cannot certify the commercial engine's runtime allocation.

## Other Interpretive Protections

- All fourcases must use the same validated integration architecture, material fits, component/native Yee rules and91 frequencies. A small local cross-check is algorithm evidence, not proof of whole-domain ownership/closure or grid convergence.
- Periodic pillar auditing compares opposite faces at translated matching native coordinates/materials. It must NOT require an arbitrary edge point to equal the cell center: a patterned cell legitimately varies within a period. The reply's flat-inspired edge!=center shorthand is not an executable general gate.
- E components and corresponding epsilon/dual-volume are required for volume loss. H is needed for independent flux/local flow evidence only where actually used, not an automatic full-volume allocation.
- Existing closure thresholds remain weighted<=.005/max<=.02; informal strict inequalities do not silently rewrite frozen gate metadata.
- The reply's assertion that old28 builders were runnable is not what the survey proved: only script settings/SHA were checked, not all28 runtime completions.
- Streaming does not resolve possible P30 FINE solver-grid memory on its own. Native solver and DFT allocations are separate gates; do not divide wholecase RAM by MPI count.
- No additional Flat/Y/benchmark/frequency-split solve, material plugin, new solver/physics/PML/mesh relaxation or RAM cap enlargement is authorized by this note.

Next allowed step: bounded local capability/implementation verification. If no supported equivalent route is established, maintain HOLD and report the consolidated precise blocker at the next necessary decision point. Do not launch CAD merely to appear active, construct giant arrays, or treat the Pro assertion as an actual software test.
