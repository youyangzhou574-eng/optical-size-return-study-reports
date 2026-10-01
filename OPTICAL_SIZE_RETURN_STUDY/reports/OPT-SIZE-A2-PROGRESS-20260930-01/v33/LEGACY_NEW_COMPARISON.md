# Legacy vs Current Candidate: Human-Requested Mesh Ruling

The latest direct request is to compare the old models and ask Pro: when pillar side doubles, can the mesh be coarser than the old mesh? The user is asking for a scientifically supported recommendation, not asserting that40nm is adequate and not authorizing execution of a new mesh.

## Verified local comparison

| Setting | Legacy single-500nm component builder | Legacy91-point R/T builder | Current P30_X_FINE ten-point native candidate |
|---|---|---|---|
| PDMS triangular core side |1.5um|1.5um|3um|
| Pillar height |9um|9um|9um|
| Computational XY period |9x5.196152um|9x5.196152um|18x10.392305um|
| PDMS base thickness |10um|10um|10um|
| ITO coating thickness |100nm|100nm|100nm|
| Fe2O3 coating thickness |25nm|25nm|25nm|
| Coating/pillar override dx/dy/dz |20/20/15nm|20/20/15nm|15/15/11.25nm|
| Uniform fine mesh through all PDMS/water? |Not established; local override only|Not established; local override only|No: inherits automatic mesh outside z=-0.2 to9.325um override|
| Source band |380-780nm|See protected legacy builder; not assumed identical to component builder|350-800nm|
| Recorded wavelengths |500nm only|350:5:800nm,91 R/T samples|350:50:800nm,10 samples|
| Heavy3D recording |Per-pillar E/index volumes plus flat-stack pair|Deleted; flux monitors retained|One full-height rectangular repetition-tile E/index pair|
| Qualification |Historical component outputs are not proof of current native-Yee/interface validity|Historical R/T completion/replay, not3D component qualification|Resource STOP; no solve; native material/tile proof pending|

The prepared but unexecuted one-point revision retains the last column's physics and grid and changes only all observation frequencies to500nm. It is NOT an actual one-point native report and does not narrow the broadband source.

The legacy single-point source is build_indexaudit_1p5_9.lsf in the preserved side_1p50_height_9p00_indexaudit_20260522 folder, freshly checked SHA2565794E1E48A99BFE42E2281FA89E3B568B37CF31F7CD841E79E537AFDEA86ECD1. Relevant original line numbers: geometry/thickness14-20, source22-23, mesh27-29, periods32-33, metrics_lambda44, flat E volume349 onward, pillar E/index405/420 onward. It was read only, never executed or modified. Old define_sampled_materials/CAD/save operations were not reused.

The legacy91-point resource estimate12.697GiB is from historical R0 preflight, not a measured current peak and not a verified memory estimate for the old500nm component-monitor configuration. No matching historical P30 grid audit is established. The per-rank old grid products have unresolved halo conventions; they are not an exact global-cell count.

## What made the new case large

XY area doubled in each direction:4x. At the same override volume, changing20/20/15nm to15/15/11.25nm increases node density by(20*20*15)/(15*15*11.25)=2.37037037x. Their product9.48148148x is a local-volume cell-count scaling illustration, not a complete native-grid or RAM prediction. Automatic mesh, halo/PML, material coefficients and acquisition buffers still matter.

Actual native ten-point CPU estimate: fixed electromagnetic fields/index151.385952GiB; E/index monitors each159.365511GiB; runtime472.257970GiB; collection641.438746GiB. Single-point unchanged-grid proxy: E/index each15.936551GiB, runtime183.610535GiB, collectionUNKNOWN. Even fixed fields exceed64GiB. Neither estimate has been allocated by a solver.

## The requested consolidated ruling

1. Explain whether larger lateral features permit larger dx/dy in core/bulk/water, while unchanged25nm Fe and100nm ITO shells, sharp corners, material wavelength and9um height may still require local resolution. Which parts can be coarser than20/20/15nm? Do not infer that all features became2x larger.
2. Provide one preferred, concrete region-aware mesh pair: dx/dy/dz and bounds for shell/interface, pillar core, PDMS bulk and water; say whether it is a fair shared-resolution comparison between P15/P30 or needs size-dependent grids validated to the same error. Explain the conformity/mixed-cell loss partition and material-ownership validation; no nearest-material binary replacement.
3. Compare a coarser/local-refinement original-cell route with a smaller, demonstrably equivalent computational-cell route. A nominal factor3 X tile exists, but native grid/index/source equivalence is pending. Never replace P30's18um period with9um just to save memory if that changes the actual density/pattern. Smaller-cell representation needs explicit human approval.
4. Prefer the cheapest valid500nm-first observable A_Fe2O3_X(500nm), retaining independently feasible material absorption and current scientific gates. Define BASE/FINE and size-difference uncertainty; no J10, full-spectrum/current or spectral-convergence claim. Any four-material closure waiver remains an explicit human decision.
5. Decide a bounded stage order that can actually proceed without another identical unsafe P30_FINE attempt: whether P15_BASE preparation/start may precede the other three native preflights, or which original case is the prerequisite. No additional case/diagnostic solve or auto retry.
6. Incorporate native RAM for all phases, export/analysis buffers and disk. Cap remains min64GiB/70% startup-free memory. No raise of RAM cap, blind third P30 CAD or source-band/PML/conformal/time change. Local80-input/8h and total10-CAD/2h operational allowance is explicitly USER-REQUESTED and remains unapproved; include the consumed40 inputs and2 CAD, not reset counts.

Please produce one implementable preferred plan plus, only if required, a clearly stated minimal human decision. Ordinary script implementation errors are handled locally, not separately submitted for scientific approval.
