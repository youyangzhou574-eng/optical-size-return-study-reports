我已经按你这次指定的 **v24 固定提交 `772960d978929234638ca5d4be02ac47944675c9`** 重新审了，不再沿用旧的“D3运行中”状态。

我实际读了这些文件：`REPORT.md`、`INDEX.md`、`manifest.json`、`comparison_summary.json`、`D2_full_diagnostic_91.csv`、`D3_full_diagnostic_91.csv`、`D3_independent_materials_and_closure_91.csv`、`D3_minus_baselines_raw_flux_91.csv`、`key_Ex_complex.csv`、`D3_raw_metadata.txt`，以及冻结/无写入者/CAD导出/传输/测试相关收据，包括 `freeze01_receipt.json`、`freeze01_current_no_writer_receipt.json`、`freeze01_runner_status.original.json`、`freeze01_p0.redacted.txt`、`export_raw01_receipt.json`、`export_raw01_worker_exit.json`、`export_raw01_loaded_result_audit.txt`、`focused_test_evidence.json`。

### 这次D3真正说明了什么

D3 的求解本身可以作为这次“时间长度敏感性测试”的有效结果使用：

- MPI = **0**
- 8265 iterations
- 实际物理时间 **280.7915 fs**
- AutoShutoff = **8.71817×10⁻⁹**
- 确实达到新设的 \(10^{-8}\)，而不是撞上2900 fs上限
- 日志有正常结束、collect data 和保存证据
- 独立无写入者复核后完成保护冻结
- 后续快照CAD导出实际 **exit 0 / stderr 0**
- 原runner `-1`、task `1` 和476成员范围bug均被原样保留，没有“洗成0”

所以执行层面这次已经够了，**不需要再追runner那个bug，也不需要再做一次导出或服务器核查。**

---

## 科学上最重要的结果：早停确实解释了“闭合类”问题，但解释不了R/T和Fe₂O₃

这个对照非常有价值，因为D2→D3只改变了停止阈值。

从D2到D3：

| 指标 | D2 | D3 | 变化 |
|---|---:|---:|---:|
| direct/net weighted | 0.002290 | **0.000660** | **下降约71%** |
| 四材料 closure weighted | 0.002682 | **0.000498** | **下降约81%** |
| R vs TMM weighted | 0.017802 | 0.016632 | 只下降约6.6% |
| T vs TMM weighted | 0.011205 | 0.011085 | 只下降约1.1% |
| Fe₂O₃ vs TMM weighted | 0.006070 | 0.006206 | **反而变差约2.2%** |

而且不只是weighted：

- direct/net 最大误差降到 **0.002485**，通过原 `.005` 门；
- closure 最大误差降到 **0.002529**，远低于原 `.02` 门；
- R 最大仍 **0.06894**，门是 `.01`；
- T 最大仍 **0.02532**，门是 `.01`；
- Fe₂O₃ 最大仍 **0.04775**，门是 `.01`。

这已经把问题拆得很清楚了。

### 可以支持的结论

> **D2中相当一部分能量闭合和direct/net不一致，确实具有明显的有限仿真时间/早停敏感性。收紧AutoShutoff并继续衰减后，这两类误差基本消失。**

也就是说，之前我们怀疑“是不是170 fs停太早”——**答案现在是：对闭合问题，是。**

但：

> **R/T及Fe₂O₃相对于连续TMM的主要偏差不是早停造成的。**

因为时间从171 fs延长到281 fs之后，它们基本没动到足以改变判断的程度。

因此现在不应该再把所有剩余问题归到“时域没跑够”。

---

## 这其实是一个很好的止损点

我建议**到这里停止继续折腾AutoShutoff、closure和服务器运行器。**

现在我们已经解决/分离了两件真问题：

1. **周期边界覆盖错误**  
   → 一格外延后，16.5%横向见证差变成0。

2. **早停造成的能量闭合误差**  
   → \(10^{-4}\rightarrow10^{-8}\) 后，direct/net和component closure都通过。

剩下的是第三类：

3. **连续TMM vs FDTD的传播/离散误差**  
   → R/T和Fe₂O₃仍然失败。

这个分支已经和前两个问题基本分开。

### 当前合理的状态

我建议把状态改成：

```text
Periodic-boundary coverage issue:
RESOLVED for flat D3 diagnostic

Finite-duration / early-stop contribution:
CONFIRMED AND CONTROLLED at auto shutoff = 1e-8

Flux internal consistency:
PASS

Independent four-material closure:
PASS

R/T vs continuous TMM:
FAIL

Fe2O3 vs continuous TMM:
FAIL

Overall flat calibration:
NOT_QUALIFIED

Remaining root:
DISCRETE_PROPAGATION / GRID EFFECT STRONGLY SUSPECTED,
NOT YET UNIQUELY VERIFIED

Paired numerical convergence:
NOT_YET_TESTED
```

这里“early-stop contribution confirmed”是可以比以前说得更强的；而“剩余是空间离散导致”仍然不能直接写成已证明。

---

# 下一步我只建议做一个离线检查，然后结束这个排查阶段

**不要再开solver。**

唯一还值得做的，是：

### `D3_DISCRETE_PHASE_CONFIRM_OFFLINE_01`

用现在D3已经有的Ex全谱数据，重复一次我们之前对D2做过的传播波数检查：

1. 在均匀PDMS内部，从D3复场提取实际 \(k_{\mathrm{FDTD}}\)；
2. 比较：
   - 连续介质 \(k=2\pi n/\lambda\)
   - 有限 \(dz,dt\) 的离散色散 \(k_{\mathrm{disc}}\)
   - D3场实际提取的 \(k_{\mathrm{field}}\)
3. 再做一次**仅作诊断**的PDMS离散相位TMM，看看R/T剩余误差是否像D2一样明显下降。

这个检查很有价值，因为D3已经排掉了“早停”的主要干扰。

如果D3仍然出现：

\[
k_{\mathrm{field}}\approx k_{\mathrm{disc}}
\neq k_{\mathrm{continuous}}
\]

并且离散相位参考明显缩小R/T误差，那么我们就可以相当有把握地说：

> **剩余平面校准差异主要来自厚PDMS中的有限网格数值传播，而不是边界覆盖或仿真时间不足。**

这个离线检查完成以后，**不要再继续发明新的残差分解。**

---

## 然后就该回到真正的研究任务了

我不建议为了让这个平面FDTD“完美匹配连续TMM”再耗很多天。

后面真正有价值的是回到：

**1.5 μm vs 3 μm 三角柱。**

但正式进入尺寸比较之前，我们需要把D3得到的两个修正直接固化进生产协议：

- 周期边界材料/周期副本必须正确覆盖边界Yee区域；
- AutoShutoff采用这次已经验证过的更严格停止条件，而不是原来的 \(10^{-4}\)。

真正必须做的数值收敛，不是继续调平面校准，而是**后面在最终尺寸比较体系里做最小必要的网格收敛证据**。

所以我的路线是：

**现在：1个纯离线D3相位确认 → 结束flat故障排查 → 回到1.5 vs 3 μm。**

不再启动新的flat D4，不再继续调时间，不再查runner，不再做PML，不再做同一raw的closure分账。

这次D3已经给我们足够的信息把项目往前推了。
