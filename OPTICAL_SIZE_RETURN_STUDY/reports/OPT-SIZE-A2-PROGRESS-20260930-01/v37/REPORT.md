# v37: Native memory estimate and real ownership blocker

Report ID OPT-SIZE-A2-PROGRESS-20260930-01. This is a normal consolidated report and major plan-correction request, not a solver-start request or a repeated v36 submission.

## Human request and current authority

The human explicitly requested the memory estimate for the current v36 candidate. One separate memory-only native CAD audit was performed, not the full v36 production preflight. The subsequent human request was to check current server free RAM and remote-host memory risk, with an ambiguous conditional-start phrase containing 100G. Clarification was requested locally. Do NOT infer a100GiB resource cap or a scientific STOP waiver from that phrase. Existing prior instructions authorize consolidated Pro review of major blockers; ordinary implementation details remain local.

This report preserves the original large cells, Fe25/ITO100, 9um pillars,10um base, M0/A2 fits, X polarization, source350-800nm,500nm recording,2900fs/1e-8. No small cell, thickness change, new solve, retry or safety-policy relaxation occurred.

## One actual memory-only audit completed

Case P30_X_FINE, original18 x10.392304845413264um. Native geometry retained protected true-parent coating/periodic halo. Mesh25/25/15nm, flat-z12.5nm, growth1.2, accuracy2,Conformal0. Candidate recording includes16 local3D E-only monitors,85 additional2D power faces plus the existing4 full-cell flux monitors.2D faces conservatively retain E/H/P/power outputs; no3D H/P. Runtime index monitors0, large index/field getters0. This candidate is NOT scientifically qualified or production-ready.

Actual CAD exit0, wall15.8221219s, local worker exit0/PID absent, stderr0, completion marker valid,8 transferred files bytes/SHA matched. XML absent/errors null, not fabricated XML0. Protected source remains560994bytes/SHA61B24C378622FDD91E0F4D02F0E80F47BF3103E4E02AD8E45FBB0F31491D16E0. Saved candidate806215bytes, not uploaded as the only evidence.

| Native CPU estimate | GiB |
| --- | ---: |
| Internal fields and material grid |54.44219215679914|
| All monitors |6.888887390494347|
| Runtime total |61.99234244693071|
| Data collection |14.880361706018448|
| Saved monitor data |7.355270177125931|
| Initialization/mesh report phase |0.15625|

Native report SHA2563F417D6DB2A6B0C173C1904C85EEA616F88ACA6C4CC9351433FF2D1567B6DFEE. These are estimates, not an actual solver peak. CAD peak working set was not collected. The Conformal memory reliability warning remains. Current executor did not waive it. Runtime is below64GiB but above your suggested0.9*cap=57.6GiB admission margin. Available RAM does not remove that problem.

Native axes: x720cells/all25nm; y493cells/min14.6894534824nm/max24.9942039613nm; z1142cells/min12.5nm/max25.8620689655nm. Growth did not make the bulk obviously sparse enough. Do not claim shell-local refinement from the bbox names.

## The local owner-prism scheme has a genuine geometric blocker

We recovered logical parents from protected full_parent_core_vertices_um, deduplicating the two periodic x-edge copies.12 logical owners wrap into14 central-cell rectangle segments. OuterFe bbox +80nm produces12 positive-area prism-overlap pairs, summed pairwise overlap area17.022198127334054um2. Full coordinates, proposed E regions,2D faces and overlap table accompany this report.

Recording overlap is retained in this memory-only estimate, NOT silently removed. Scientific ownership is NOT PASS. Independent water-complement flux from simply subtracting every overlapping prism boundary is invalid. The candidate is not allowed to integrate or solve as a valid partition; no divide-by2, residual water backfill or gate waiver was applied.

Please repair the mathematical/control-volume scheme explicitly before authorizing any further execution. Distinguish harmless overlapping recording buffers from forbidden overlapping scientific ownership; if an exact exclusive union/partition and correctly oriented union-boundary surfaces can be constructed from the current data, prescribe it. Do not imply it is implemented or already native-validated. Do not require another identical resource-only CAD to demonstrate this same overlap.

## Current one-time server snapshot, not a monitoring loop

Server UTC2026-10-01T21:26:50.4059436Z: total127.24334716796875GiB, free106.36219024658203GiB, used20.881156921386719GiB. Remoting maximum private0.0657615662GiB / working set0.0897521973GiB; three shell/remoting processes were returned, none truncated. No hundred-GiB remoting host observed in this snapshot. This does not establish a growth rate or guarantee future behavior.

Previous audit host55460 was independently CONFIRMED_ABSENT. New short read local worker exit0 and PID absent, local session closed; new remote host exit NOT independently proven, and no extra session is opened to chase it. Client UTC closure21:23:04.4341719Z and server UTC are separately retained; clocks/history unchanged. Old RAM/engine monitors remain retired. Return was a primitive JSON string, bounded8192chars, one request, no rich CIM/GetContent object graph, no CAD/solve.

## Budget and a single bounded remedy requested

Science ledger unchanged MAIN1/6,DIAGNOSTIC4/4,RECOVERY0/2,TOTAL5/12; config SHA8A07DA334F61C9DD979521BFE33FD36057473F819F41FE0D28A0F59EB7EC1BB5. Actual CAD now4/10, cumulative48.8902708s/2h. Conservative local-input/check accounting now80/80, no reset. Earlier hardcoded71 in the initial memory-summary output is preserved but superseded by the scope-counting receipt77 and three new bounded-read static checks80. No extra science event was booked.

More bounded execution time/check/CAD autonomy was explicitly requested by the human; include the needed allowance in this normal report's decision, not a separate budget-only exchange. With4 CAD already used, four genuinely revised inputs each build/reopen would require a total12, not v36's11. First prefer verified reuse and no duplicate CAD; otherwise give an exact cumulative ceiling and local-check allowance, keeping local8h,CAD2h,hard RAM64GiB and the existing four conditional MAIN starts unchanged. No account/platform quota expansion.

Please give ONE coherent route, or an honest STOP: resolve exact ownership/water-complement surfaces and state whether the existing61.99GiB estimate is admissible under an explicitly justified policy, or give one bounded monitor/mesh remedy that preserves Fe25/native acquisition/strict2% and old direct-net<=.002/closure<=.005 gates. No secret source-band/thickness/PML/shutoff/small-cell changes, no lowering qualifications, no blind repeated candidate tuning, no restore1e-4. Any changed physical scope or safety policy requiring human confirmation must be stated as a single consolidated approval item, not silently implemented.

Executor will own the new response readback/check. No solver will start while these blockers or the ambiguous human memory condition remain unresolved.
