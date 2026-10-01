# Legacy Mesh Reconciliation

This is a local-file audit in response to the user's request to check the old mesh and protect server memory. No remoting, CAD or solve was performed.

## Verified Legacy P15 Coating Mesh

The existing directRT91 builder at `mac_review_handoff/01_server_simulation/model_packages/pillar_1p5um_9um_fluxonly_dense50_directRT91_v001/build_spectral_pillar_1p5um_9um_fluxonly_dense50_directRT91_v001.lsf` has SHA256 `06EEF3DC1D584CBAE221B14AD9D1D87F57CF8624E223D76B04D7056F8DA54A3B`.

- Lines 27-29 explicitly set dx=20 nm, dy=20 nm, dz=15 nm. The name dense50 does NOT establish a 50 nm mesh.
- Mesh accuracy is 2.
- `coated_pillar_mesh` covers the whole lateral period and z=-0.2 to9.325 um. This is a local override region, NOT proof of a uniform 15 nm z mesh throughout the 10 um PDMS base and exterior water.
- The original indexaudit builder also has the same 20/20/15 nm assignments. Neither old file was changed.
- DirectRT91 explicitly deletes heavy 3D field/index monitors for flat-stack and all 14 pillar volumes before save, retaining flux spectra. It does not demonstrate native four-material 3D absorption at91 frequencies.

## Existing Runtime Evidence

Historical p0 printed 227x132x166 with28 ranks /2x2x7 partition. R0 replay p0 printed452x262x291 with4 ranks /1x1x4 partition. These are per-partition counts; NOT two directly comparable global grids.

Approximate partition products are454x264x1162 and452x262x1164, respectively, about138 million cells, with halo/count conventions unresolved. No exact global-grid identity is claimed from these products. See the protected `reports/R0_EARLY_PROCESS_COMPARISON_20260929.md`.

The existing R0 preflight report records13,632,961,269.6 bytes recommended memory (12.697 GiB),8,226,598,016 collection bytes,4,113,299,328 saved-monitor bytes. This is HISTORICAL SYSTEMCHECK WITH CONFORMAL WARNING, NOT measured peak or current free RAM. The original systemcheck binary/text was not independently retrieved this turn; its quoted SHA is22E44C0234D5DABC27ED97A82B57F947EF8A12D8DD3334CCAB35A3A12E5D0A41.

## Implication for Authorized New Package

The v26 BASE coating mesh equals the legacy nominal20/20/15 nm; it is not automatically a new refinement everywhere. The v26 explicitly fine PDMS bulk and reserved global z count are new forecast assumptions, not legacy native-grid observations. Main new storage conflict comes from proposed full-control-volume3D Ex/Ey/Ez +index, all91 frequencies, and P30/FINE volume scaling. Reusing the old12.697 GiB estimate for that new monitor configuration would be unsafe.

v26 remains retained as rejected candidate forecast. No mesh is frozen for production. Full-3D monitor strategy, native grid, material ownership and safe resource estimates must be validated before either new CAD operation or actual solver start. Human approval is received; no additional Dudu approval wait remains. No change to64 GiB/.7 RAM, science gates, budget or old monitoring retirement.

No matching historical P30 saved-grid audit was established from the inspected local project folders; P15 results must not be silently assigned to P30.
