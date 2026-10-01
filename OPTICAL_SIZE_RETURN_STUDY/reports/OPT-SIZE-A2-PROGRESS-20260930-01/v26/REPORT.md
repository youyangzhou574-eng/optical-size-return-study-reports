# P15/P30 X 偏振四算例：本地非求解放行前资源审查

Report ID: OPT-SIZE-A2-PROGRESS-20260930-01 / v26

**结论：HOLD_RESOURCE_AND_UNVERIFIED_NATIVE_PREFLIGHT。本地核算完成，四算例包尚不具备 CAD/求解放行条件。**

用户已授权嘟嘟代批 P15/P30 × BASE/FINE 四个 X 偏振生产算例包，并要求先核实具体网格、含监视器的内存、资源和时间上限、顺序及 STOP。本次授权不是 CAD 或求解启动许可。本轮 0 服务器会话、0 CAD、0 solve、0 新预算事件；未向 Pro 新提交或询问。

科学范围依 Pro `OPT-SIZE-PRO-PILLAR-X-PILOT-PLAN-20261001-07`：只做 X 偏振，不扩成 Y/无偏振结论。Flat 已结案，其 NOT_QUALIFIED、NARROWED_BUT_NOT_UNIQUE、NOT_YET_TESTED 保持；不重算 Flat。第5个 MAIN/flat-fine 只是预留，本四算例包不包含它。

## 1. 已核来源与未核证据

- 两个已有几何审计 JSON 逐字 SHA 校验通过，仍只是 geometry-only 草稿，不是 CAD/input 验收。P15/P30 周期分别 9×5.196152422706632 μm、18×10.392304845413264 μm；柱高9 μm、PDMS base10 μm、ITO100 nm、Fe2O3 25 nm、M0/A2 不变。
- 历史 D3 日志 SHA 校验通过：native grid452×262×560、1MPI×1thread、solver speed70.6856 Mnodes/s、8265迭代；FDTD壁钟7754.25 s、总壁钟7850.41 s。资源快照8.74756 GiB不是实测峰值。折合约141.63 bytes/native grid point，仅作为工程代理校准。
- 不使用配置旧“D3正在运行”字段。MPI0/原runner-1/task1按原证据保留，不改成统一成功。
- 当前 P15/P30 的 native grid、dt、实际 Yee 材料归属、systemcheck、license checkout、当前可用RAM/磁盘均未实测。本轮不为补这些证据开远端或CAD。

## 2. 具体候选网格与固定空间关系

| 参数 | BASE | FINE |
|---|---:|---:|
| 全周期名义 dx、dy | 20、20 nm | 15、15 nm |
| coating/柱体细化区 dz（z=-0.2至9.325 μm） | 15 nm | 11.25 nm |
| PDMS bulk dz（z=-10至-0.2 μm） | 25 nm | 18.75 nm |
| 外围 water dz | 25 nm | 18.75 nm |
| nominal CFL dt，非native | 3.398022760620957e-17 s | 2.548517070465718e-17 s |

P15/P30共享同一套绝对步长规则，FINE各方向为BASE的0.75倍。conformal variant0、mesh accuracy2、grading factor sqrt(2)、PML profile1及8层保持已保存设置的候选继承值，不自行换conformal/PML。仿真z域候选为[-11.5,10.325] μm。外部water不采用100 nm粗步长，以免8层PML把固定的R/source平面吞入。

沿用已记录pillar空间映射：source z=-10.85 μm，R=-11.15 μm，T=9.825 μm；控制体 Pbottom=-10.35 μm、Ptop=9.475 μm。它们与实际native位置/PML距离仍须CAD核定。输出freq为350:5:800 nm全部91点，各case复用同一实际f/权重；本候选不把名义位置冒充保存后的真实采样面。

背景和连续base层延伸到周期Yee区域之外；完整真实柱体先生成固定法向壳层，再周期复制、取中央cell及一格halo。不能给人工cut face镀膜，不能拉伸边界柱，不能按P30×2放大100/25 nm膜厚。积分只覆盖一个原周期的半开控制体；halo与周期等价边界不能重复计面积或损耗。

20 nm横向网格并不保证每个斜侧面的25 nm Fe层都有多个纯材料采样点；不能据此宣称材料归属合格。必须检查实际分量Yee坐标、index、混合/未归属体元及真实材料fit；有歧义就STOP，不按位置强行分配或从旧field借数据。

## 3. 逐case内存与数组估算

**以下都是离线模型，不是 CAD systemcheck 或真实峰值。** 全部GiB为2^30 bytes。轴向端点余量2点；z另加16点和10%transition/PML工程余量，不是native mesher精确预测。solver代理取160 bytes/规划grid point；并行时按全case总内存计，不能除以MPI rank骗过上限。

3D监视器候选覆盖控制体全部体积，记录原生 Ex/Ey/Ez、91频点、complex128；index_x/y/z同f/coords做保守同尺寸存储模型。关闭额外H/P/profile图像输出，四通量面只输出功率；其运行期内部仍按六复分量作保守估算。原生采样 downsample=1、interpolation=none，不削减频点或跳过薄壳。

| Case | 规划solver grid | solver代理 GiB | 单份3D E GiB | E+index+通量 raw GiB | 收集/副本峰值模型 GiB |
|---|---|---:|---:|---:|---:|
| P15_X_BASE | 452×262×1260 | 22.23 | 555.94 | 1115.73 | 2819.13 |
| P30_X_BASE | 902×522×1260 | 88.40 | 2210.37 | 4436.07 | 11202.68 |
| P15_X_FINE | 602×349×1675 | 52.44 | 1315.36 | 2637.55 | 6661.42 |
| P30_X_FINE | 1202×695×1675 | 208.51 | 5230.11 | 10487.40 | 26481.14 |

E的数据形状为[planning_nx,planning_ny,planning_monitor_nz,91,3]；monitor_nz依次1154、1154、1539、1539。单份E字节=点数×91×3×16。index同尺寸是保守场景，不宣称软件一定以该形式分配；即使去掉index，E这一项本身仍远超64 GiB。

峰值模型=1.25×[solver代理+2×(E+index+四通量面)] +2 GiB。它考虑一次收集副本和工作区，却不是认证上界；直接运行官方整数组分析脚本可能还有更多临时数组，因此真实峰值可能更高。软件输出/内部DFT精度、采样降频和分配策略只能在获准的native检查后确定。[三维监视器资源说明](https://optics.ansys.com/hc/en-us/articles/360034902393-Frequency-domain-monitor-Simulation-object)、[systemcheck分项说明](https://optics.ansys.com/hc/en-us/articles/4403937981715-runsystemcheck-Script-command)。

四case完整raw模型合计约18676.76 GiB，按既有2×新输出+50 GiB门，需要约37403.51 GiB（36.53 TiB）可用磁盘。旧配置“每case8 GiB”不适用于本3D方案，也不是当前磁盘证明。

## 4. 监视器实现路线审查

推荐的最终目标仍是同次新场、新index的真实3D四材料独立积分，再与控制体净通量closure；不能用三条line乘面积、能量残差回填材料，或用边界流量之间的代数恒等式冒充独立积分。

当前能明确拒绝的方案：

- 标准全控制体3D E/index：如表，资源不通过。
- 仅把同一体积切成多个矩形monitor：各tile同时DFT，总点数不减少；halo重复还可能增加。运行后逐tile导出，只改善后处理，不减少求解时DFT内存。
- 只监测Fe/ITO理想稀疏材料体元：这个目前未实现、未证明数学/软件等价；按已有材料体积和候选单元体积估出的单份E场景依次51.10、104.18、121.12、246.94 GiB，且未计water、index、halo、重叠和solver，不能拿它报资源PASS。
- 降到少量频点、下采样掉薄壳、仅留一个E分量、使用光谱平均代替91点，不满足本包输出/材料归属门。
- 未证明等价的surface-only材料分解、改变周期/利用未审对称性、引入材料插件或新solver，不在当前包许可内。

原生未插值场在接口上须分量分别用同位置的实际epsilon/dual-volume后积分；不能先插值E再乘材料loss。周期端点与halo一次计权，native混合材料/未匹配点必须显式报出，不强行最近n分类。[高精度吸收方法](https://optics.ansys.com/hc/en-us/articles/360034915693-Calculating-absorbed-optical-power-Higher-accuracy)、[多材料归属说明](https://optics.ansys.com/hc/en-us/articles/360034395254-Calculating-absorbed-optical-power-Higher-accuracy-method-with-multiple-materials)。

**因此本报告不能给出已证明可行的低内存3D采集实现。它排除了不安全的标准路线，而不是宣称所有等价实现都不可能。** 若继续，应先做本地有界采样/监测可行性优化；实际CAD仍保持未放行。

## 5. 运行资源与时间上限，均为待批候选

- 全项目同时最多1个heavy FDTD；候选4MPI×1thread，全部case一致，无rank扫描。不新增账号、权限、许可路由或购买许可；实际entitlement/checkout/runner身份仍待核。4rank不保证4倍速度，也不把全case内存除以4。
- 全case RAM门仍为min(64 GiB, 0.70×启动时实际可用RAM)。CAD mesh、solver、DFT、收集/保存、导出及后处理分别检查，任何阶段超过门就不启动。当前可用RAM未查询，历史恢复值不当current。
- simulation time最多2900 fs，auto shutoff1e-8；不达到阈值而撞上限就记录真实终止，不自动延期/重算。
- 提请嘟嘟核定的运营预算：每case48h、四case192h。它是启动前admission与队列停止/人工处置触发上限，不是完工保证。无单独授权时不能据超时自行kill运行引擎；触发后停止后续队列并请求明确处置，不默默延长预算。
- 历史D3速度外推到2900fs：1rank场景依次50.04/198.97/157.37/625.72h；理想4倍加速场景12.51/49.74/39.34/156.43h。巨大DFT可能更慢，native dt也可能更小；这些不是ETA/严格上界。P30 BASE和FINE在理想外推中都已超过48h候选，因此时间admission也不通过。
- 不另做benchmark solve来买时间估计。已有case的真实速度只能在其获准启动后用于后续检查，不作为额外算例。

## 6. 顺序、科学门与停止条件

必须先使全部四case准备可行并冻结共同规则，再按 P15_X_BASE → P30_X_BASE → P15_X_FINE → P30_X_FINE 串行执行。两BASE均正常完成且3D归属/独立closure合格后才进入FINE；不能先开易跑P15来回避不可行的P30 FINE。

启动前任何一项为false/unknown均阻断：嘟嘟明确CAD/求解放行、明确非空inputFsp与可信PID+birth+name范围、无写入者/冲突、真实native grid/dt与91freq、周期连续层/真实壳层、实际fit和Yee材料归属、各阶段RAM/磁盘/时间门、唯一预算事件与输入SHA。旧476成员缓存、外部MPI排除表和退役监控不能复用。

运行/结果门：MPI非0或unknown、stderr/收集失败、normalend/collect/newsave不完整、失去身份/出现写入者、周期审计冲突、非有限/坐标或f不符、3D材料归属失败、R/T与净通量一致性失败（corrected direct/net weighted>0.002或max>0.005）、独立closure weighted>0.005或max>0.02均STOP全包后续队列；不自动恢复、retry或改失败记录。runner/task/MPI分别记录，不能以MPI0伪写runner0。柱体没有平面TMM解析参考，不套用Flat的continuous-TMM门；Flat原FAIL标签不变。

配对门按Pro冻结：每尺寸|Jfine-Jbase|/|Jfine|≤2%；Jfine=0或非有限不能直接做除法通过。u_delta=u15+u30，只有|DeltaJfine|>u_delta才称差异被分辨，否则报告未分辨，不自动追加细网格。

J_Fe^X是AM1.5G吸收等效光电流，不是实际器件电流。使用同一350–800 nm Global Tilt线性读取/梯形积分与统一单位。ASTM原始SHA要求为B48A6635CE398F7E0FA392150D68B5793ED7F2A65D9E2406BEC7E6BE9FB20954，尚未在本次准备生成/核91点权重。eta_gain^X只用D3时标PROVISIONAL_INTERNAL_REFERENCE；不预设95%等论文阈值，不把Flat旧门升级为PASS。可选flat-fine不包含在本四case授权候选中。

## 7. 按用户要求随正常报告申请有界工作预算

**这是用户提出的要求：申请更适合本项目的执行时间、计算/试验次数和自主推进范围，减少普通细节反复请示。** 本报告先供嘟嘟核实，不为此另向Pro发送预算申请。

建议先审批一个最多120min的本地非求解资源优化包：只比较可证明等价的3D采集策略、独立geometry/source/频点身份、离线数组/内存核算与最多40项synthetic tests，产出一个可读整包。额外solver starts=0、CAD=0、远端=0；不能通过换源/降频点/压低网格/改材料/PML来“优化”。超过该范围或无法满足64 GiB门就报告具体冲突。

未来四case最多新增4个MAIN，使消耗从MAIN1/DIAGNOSTIC4/RECOVERY0/TOTAL5到MAIN5/DIAGNOSTIC4/RECOVERY0/TOTAL9；这只是获准后实际start才记账的候选，不提前记账。当前限额仍MAIN6/DIAGNOSTIC4/RECOVERY2/TOTAL12，不挪类别、失败不减账。完整X/Y预算扩容是另一个科学范围，若后续需要，按用户要求在正常报告中明确申请，不因本X包许可自动扩。

自主范围建议：本地实现/测试/报告整包累计；CAD、真实启动与硬件/预算变化须明确放行；同包正常成功路径可按已批准状态机推进，无需逐小步骤Pro审批，但任何科学STOP/安全/资源失败都阻断。当前没有给出更大RAM/机器/平台额度的自动许可；增加时间和次数本身不能修复数TiB数据冲突。

## 8. 可复算产物与现状

15个本地聚焦测试通过；forecast02实际exit0。forecast01及最初错误CFL等同假设留在本地历史中，未覆盖。名义dt与历史native dt差约0.0196%，已明确区分，不反求参数强行拟合。计算器只做标量运算，不生成巨型3D数组，不访问服务器或CAD。

完整计算表、输入来源SHA、假设、计算器和tests见INDEX.md。**建议嘟嘟此时不要放行CAD/求解；先确认资源冲突，并审查一个不新增solve的低内存等价采集准备范围。**
