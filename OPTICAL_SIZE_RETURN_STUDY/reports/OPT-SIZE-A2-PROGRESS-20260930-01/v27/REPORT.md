# P15/P30 X Production Package: Legacy Monitor Evidence and Resource Decision

Report ID: OPT-SIZE-A2-PROGRESS-20260930-01 / v27
Decision requested: resource-feasible, scientifically equivalent acquisition path.

## 1. 最新授权与实际状态

用户直接批准 P15_X_BASE、P30_X_BASE、P15_X_FINE、P30_X_FINE 四个 X 偏振生产算例，包括按 Pro07 方案有界远端 CAD 审计及全部条件满足后的求解。无需再等嘟嘟批准同一个包。用户随后要求核查旧网格和重型三维监视器，明确不能把服务器内存打爆；本次直接指令是“你去问问pro该怎么办吧”。

这不是再次申请同一个四算例的人类授权。问题是如何在保留科学要求的同时实现真实可行的资源方案。当前新生产包尚未进行远端会话、CAD 或 solve，预算未增加；本报告交付也不触碰服务器。旧 Flat 已结案，NOT_QUALIFIED / NARROWED_BUT_NOT_UNIQUE / convergence NOT_YET_TESTED 不改，不恢复 Flat 求解。

v26 是先前离线资源候选报告，当时的人类授权描述已经过时；其计算是拒绝一个不安全候选，不能作为最终配置或当前授权状态。v26 未向你提交过。本次以 v27 为当前事实，不重开已结案科学包。

## 2. 旧模型实际怎么做

本地重新读取四组旧工程目录的 30 个 build 脚本，排除 GitHub/GPT/paper 打包副本。附件 LEGACY_INVENTORY.csv 保留每个来源的相对身份、SHA256 和显式设置；这只是脚本审计，不冒充重新打开原 native FSP 的验收。

- 28 个柱/孔 builder 明确使用局部 coating mesh dx=dy20 nm、dz15 nm。另 2 个 Flat builder 明确薄膜区 dz5 nm，不能由缺失变量猜横向网格。
- 30 个 builder 都定义 metrics_lambda=500 nm；显式诊断 frequency points 均为 1。不能由此说所有 R/T 或 index 对象也都只有一个频点。
- 重型柱体诊断通常是 14 个柱体局部包围盒的 3D E/index，加 z=0..125 nm 的薄膜 flat-stack volume；柱体盒含 PDMS 核心、壳层及部分 water，不是只取 Fe/ITO 的稀疏壳采样。
- 旧 1.5/9 indexaudit 明确每盒 XY 增加 80 nm；其重型 E 是 500 nm 单点。旧 export 先构造 E2，另读 Hx/Hy 算 Pz；旧 indexmask 分析 TARGET_WAVELENGTH_NM=500。这不是 91 点各分量原生 Yee 吸收证据。
- 另查 directRT91 包：删除重型 flat-stack 和 14 柱 E/index，仅保留 91 点面通量输出。因此历史能跑的 broadband R/T 包，不等于能跑 91 点完整四材料体损耗包。
- 30 个脚本未显式设置 downsample / spatial interpolation，也未明确全部关闭 H/P。不能将脚本未写当成已确认 native 默认值，更不能复制旧盒子即称周期去重、材料归属、Yee halo 合格。

同采样点数、分量和精度下，单频点到 91 频点使对应场 payload 约乘 91；不是总引擎峰值严格倍数。详细限定及来源见 LEGACY_MONITORS.md。

## 3. 资源冲突是什么，不是什么

附件 RESOURCE_CANDIDATES.csv 是 v26 已拒绝候选的离线规划，不是 native grid 或实测 RAM。候选 BASE dx/dy20 nm、coating dz15 nm；FINE15/15/11.25 nm；bulk z25/18.75 nm。全部具体值尚未冻结。

该候选用全控制体 3D Ex/Ey/Ez、91 频点、complex128，并保守计同尺寸 index、通量、收集副本，得到 P15 BASE、P30 BASE、P15 FINE、P30 FINE 峰值模型约 2819、11203、6661、26481 GiB。即使删除 index，全域 E 一项仍约 556、2210、1315、5230 GiB。不能执行这条路径。

上述并非软件认证峰值上界；index 内部分配与精度模型未核，solver160 bytes/规划格点仅历史工程代理，真实 mesher/PML/transition/DFT 实现未核。即使 monitor 优化，P30 FINE solver 代理约208.51 GiB 也需特别核查，不能将总内存除以 rank 数伪装通过。当前真实可用 RAM、磁盘和 P30 native grid 未查询，不能沿历史恢复值报 current。

历史旧 P15 directRT91 局部步长也是20/20/15 nm，native 分区日志折合全域格点约1.38亿，分区 halo 口径有差异；旧 systemcheck 报告约12.697 GiB 推荐RAM且有conformal警告，是历史估计而非峰值，更不是新三维采样资源证明。之前全域 z细化候选不能冒充旧 mesher。

仅把相同体积切 tile、运行后逐 tile 导出，不自动减少求解期同时存在的 DFT 点数；相反 halo/重叠可能增加。任何 material-loss analysis 也不能仅凭输出最终是91行就假称内部不保存巨量场。需要确认原生实现或证明等价，不能靠命名解决RAM。

当前历史 fit 的 PDMS / water epsilon.imag 在91点均有限但非严格零：PDMS约4.3354e-10..1.1937e-9，water约1.4117e-10..5.2005e-10。其fit来源SHA见 PREPARATION_EVIDENCE.json。这不是本次新CAD fit；仅“小”并不能在未知内部场下证明吸收上界。没有擅自令其零损耗、略去两材料，或用总残差分配其损耗。

## 4. 已做的本地准备

新目录生成四个真实壳层先构造、周期邻居再裁中央控制体与 halo 的几何片段。半格端点/材料互斥/人工 cut-face 不能镀膜的数学规则纳入测试。中央几何足迹与既有草稿一致，边界采样 mismatch0；但片段不是 FDTD 输入，native Yee/index/材料归属尚未验收。

14个新准备测试通过，实际本地生成 exit0；Python regression 报告111项通过，含继承重复项，不冒称111个独立科学验证。0远端、0CAD、0solve。完整生产输入、已证明低内存四材料监视器、actual f/dt/coords 审计仍未完成。

预算保持 MAIN1/6、DIAGNOSTIC4/4、RECOVERY0/2、TOTAL5/12。四个实际获准 starts 才分别记 MAIN，完成将到 MAIN5 / TOTAL9；没有额外benchmark、频点拆分求解、Y、Flat、重跑或借RECOVERY买科学收敛。

## 5. 请集中裁定的核心问题

请给出一个首选实现路径或明确不可行结论，而不是再次原则性重复“用局部monitor”后让执行端凭猜测开算。

1. 在 Lumerical 可实现的保存/DFT能力下，怎样获取同次91点真实 Fe/ITO 吸收而不使用巨量全域3D数组？请区分壳层局部/原生 material-loss/数学等价表面法各自需证明的条件、实际内部存储以及必须 STOP 的未知项。不能从旧500nm盒结果推定合格。
2. Pro07 要求四材料独立积分及独立通量closure。是否有资源可行的完整等价途径？如果没有，是否维持 HOLD，或提出明确有误差界的有界采样/科学范围调整供用户批准？任何 background 省略、lossless 改材、粗积分/降低频点都尚未执行，不能默认放宽门。不能用closure残差冒充water/PDMS独立吸收。
3. 网格请基于旧局部20/20/15与真实P30审计决定，而不是直接认可全域uniform候选。你已允许共同mesh规则且FINE<=0.75BASE；若P30 native solver或DFT本身不可控，请明示保持STOP。不要为了开算削弱fine、改变conformal/PML/geometry/物理时长，或建议未经授权的新机器/许可。
4. 用户已准四包的有界CAD审计。请明确资源优化阶段允许一次整包自主落实的范围与必须报告的科学冲突；没有必要逐小步骤再问你，但只有真实 native / 身份 / no-writer / 资源 / 科学门通过才启动。

本轮不是要求扩大RAM上限，也不是以预算申请覆盖技术不可行。当前默认RAM门 min(64 GiB, 0.70*启动时真实可用RAM) 保持，所有阶段含CAD/DFT/收集/导出/分析分别检查。只有用户明确改变硬件或安全门才可调整。

## 6. 按用户要求申请更多有界工作预算

**这是用户提出的要求**：在本次正常报告中一并申请适合本项目的执行时间、计算/试验次数及自主推进范围，减少反复请示；不是额外单发预算报告。

建议先给执行端一个最多4小时本地资源优化整包，最多40个新增synthetic/标量内存/几何验证用例，不创建巨型3D数组，0额外solve、0额外benchmark、0旧raw重算。你若批准首选实现且本地资源门可过，再落实用户已经授权的四冻结case CAD build/reopen/index审计；建议每case最多build1+reopen1，整个审计最多8个CAD进程，累计2小时admission预算，失败不自动重跑。实际操作仍需短有界请求、明确宿主生命周期，不能恢复旧rich CIM/GetContent监控。

四个MAIN生产starts上限仍4，不申请额外科学case，不改变 MAIN6 / DIAGNOSTIC4 / RECOVERY2 / TOTAL12。运营时间建议以每case最多168小时、四case累计672小时作为启动前admission/停止后续队列并报告的上限，仿真物理上限仍2900fs。v26历史速度外推P30FINE理想4倍场景约156小时，未经native/DFT验证，不能拿它当ETA或保证；若真实估算不能进预算，则不启动。此时间提案尚未获批，不是按超时kill引擎的许可，不能自动延期。

自主范围请求：首选方案明确后，在同一审批整包内自行实现、测试、审计、正常路径顺序执行、冻结/导出/分析/汇总，不逐case回问；任何未知身份、资源失败、MPI非0/未知、流/保存失败、周期/材料归属冲突、direct/net或closure失败立即STOP后续队列并集中报告。不改账户、安全策略、许可或原历史；不新开网页/换模型绕额度。

获批前遵守当前硬预算及全部STOP。若你认为需要不同执行时间或更小有界试验范围，请给具体替代，不以新增solve购买资源证明。

## 7. 冻结科学门与交付

顺序P15_BASE -> P30_BASE -> P15_FINE -> P30_FINE；两BASE全门通过才FINE。频点350:5:800 nm共91、X、M0/A2、h9um、base10um、ITO100nm、Fe25nm、各自period均不变。corrected direct/net weighted<=.002/max<=.005；四材料独立积分前有限值/coords/f/Yee/material门；积分后closure weighted<=.005/max<=.02；每尺寸 J 的配对相对变化<=2%，零/非有限分母不能PASS；uDelta=u15+u30且abs(DeltaJ)>uDelta才称差异分辨。不恢复Flat、不将J等效电流称器件电流、不三线乘面积、不删点/裁剪/缩放/残差回填。

请按此报告一次集中回答首选实现、无法回避的资源/科学冲突和上述有界预算。完整附件公开于本项目专属仓库的v27固定commit，网页只收到简短摘要与索引，不多段长正文。实际读文件与发送完成分开记；不会冒称你已读。每次发送均绑定后续检查计划，报错/超时保留回执，不盲重发。

官方参考（说明分析要求，不作为本地native验收）：

- https://optics.ansys.com/hc/en-us/articles/360034915673-Calculating-absorbed-optical-power-Simple-method
- https://optics.ansys.com/hc/en-us/articles/360034395254-Calculating-absorbed-optical-power-Higher-accuracy-method-with-multiple-materials
- https://optics.ansys.com/hc/en-us/articles/360034902393-Frequency-domain-monitor-Simulation-object
- https://optics.ansys.com/hc/en-us/articles/360034915693-Calculating-absorbed-optical-power-Higher-accuracy
