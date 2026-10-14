# FDTD 综合 skill v01：30项技术审阅与落实意见

审阅编号：OPT-SIZE-FDTD-SKILL-REVIEW-20261014-01  
对象：FDTD-SKILL-SYNTHESIS-PRO-REVIEW-20261014-01/v01  
审阅基准提交：`a1fcdaf3b53dc2a2377dbfaf37779eea81102c03`  
日期：2026-10-14  
性质：文档、接口语义和选定纯数值函数审查；不是安装、部署或新的科学运行授权。

## 结论和当前任务的关系

采用“一个轻量任务入口＋按需参考页＋独立项目配置”的组织方式。以S01的版本绑定、按任务读取和已有代码复用思路为骨架，S02作为官方工具上下文参考；不把六个仓库的执行后端拼装到本项目。S03只择取任务拆分和产物组织；S04/S06暂作连接、版本和工具分类参考；S05的通用结果归约、自动收敛认证和自动运行循环不直接纳入。

这不表示S01/S02全部代码已经审计或适配v241。当前继续使用已有v241 LSF/CLI/受控PowerShell执行链，不因skill升级而改安装、许可、资源管理器或活动任务。

**P30现有任务不等待skill全包重写、全套行为测试或再次Pro批准。** 继续以CURRENT_TASK和最新人类要求为工作范围：3 μm优先、1.5 μm退出当前计算主线；本次不重新启动、停止、延长或重排任何仿真，不重开Flat，不恢复人为次数/名额/累计工时限制。skill的缺项只约束相应的新功能，不把材料积分缺证扩成R/T工作全面停止。

D01–D30下列给出的是可落实的技术选择，不再保留同一问题的多个无排序候选；个别接口兼容性或未引入代码仍诚实保留未验证状态。普通文档改写、离线适配和必要的局部测试可以在已有用户范围内集中完成，不再逐条请求技术复批。

## 实际阅读及验证范围

阅读了本包的请求说明、SOURCE_CATALOG、SOURCE_EVIDENCE、候选SKILL、完整D01–D30决策表，以及ALL_IN_ONE中modeling/results/execution/experience/source-map/templates/validation-scenarios对应正文。逐项审阅依据是这些草案，不是对上游1606个文件逐行审计。

直接抽查固定上游：
- S01 `skills/lumerical-fdtd/SKILL.md`；
- S02 `src/ansys/lumerical/mcp/contexts/fdtd.py`的工作流和2D/PML段；
- S03 modeling SKILL第70–110行、simulation SKILL第70–145行；
- S05 `_converge.py`第1–185行，包括_reduce、compare_values、convergence_test和certify_verdict。

另核Ansys官方帮助页[O01–O16]。在线文档用于核对一般语义，不等于当前v241所有新参数都已原生验证。没有执行上游安装器、导入上游后端、访问计算服务器、启动CAD或solver，也没有重算本项目旧raw。

唯一执行的数值检查：在隔离本地Python中逐字转录已读S05的两个纯函数`_reduce`和`compare_values`，不导入其session/backend模块，以五个小型合成反例核对返回值。结果见下节。这不是综合skill行为测试通过，也不是物理仿真验证。

## 优先修正：上游收敛判断的具体风险

S05 `_reduce`先取绝对值并压为mean/max，删掉非有限值；找不到指定指标时还可能回退到坐标数组。`compare_values`会跳过缺失比较项，只要剩余项满足条件就可能返回converged=true。对于明确只研究两个聚合标量的任务，mean/max有它的用途；但它不能认证逐波长曲线、带符号功率或复场，非有限/必需指标缺失也不能被静默忽略。

|反例|输入及真实限制|本地复现的上游返回|
|---|---|---|
|波长响应交换|[0.2,0.8]→[0.8,0.2]，在固定两频率上各改变0.6；mean/max完全一样|rel_mean=0、rel_max=0、converged=true|
|非有限样本被丢弃|[1,NaN]→[1,1]，前者有缺失/无效样本|converged=true|
|符号翻转|[-0.2,-0.8]→[0.2,0.8]，方向发生改变|converged=true|
|必需统计项缺失|(mean=1,max=None)与相同输入比较|max比较缺失，但converged=true|
|回退到坐标|只给{x:[0,1]}，请求T指标；实际没有T|归约成(0.5,1)，与自身比较converged=true|

因此禁止直接采用该通用归约器作为项目资格判据。还需改写它的驱动逻辑：原代码会捕获部分设置失败后继续运行，且可能覆盖现会话/保存路径；未确认actual knob改变时的重复运行不构成收敛证据。此驱动风险来自静态阅读，本轮未执行其live函数。[U05]

## D01–D30逐项技术选择

### D01｜2D、quasi-2D与3D — 改写后采用

原生2D不是禁止功能。仅当结构、材料张量及激励对省略方向满足相应不变/可解耦条件，才采用2D；Lumerical原生2D为XY平面、Z不变。采用厂商约定TE=(Ex,Ey,Hz)、TM=(Hx,Hy,Ez)，并写明坐标，不只写TE/TM标签。2D功率绝对单位与3D不同，不能直接比较瓦数；同定义归一化量另行核对。[O01,O02]

不采纳S03“统一用3D＋y_span=0.2 μm＋Periodic替代2D”。薄3D周期模型是在计算另一组明确的周期/不变条件，不因叫quasi-2D就自动等价。本项目有限高三角柱和层叠不满足任意删去一个方向，且用户拒绝小单胞；当前不降维或缩胞。[U03]

### D02｜newproject与对象生命周期 — 撤回通用禁令

`newproject`是受支持接口，但会新建项目且不自动保存当前未保存工程。允许在明确拥有的新空会话/独立工作区使用；读取已完成结果时不得调用它或switchtolayout。新建后核定是否已有FDTD对象，缺少才addfdtd，不把“每次连接立即addfdtd”当规则，避免载入模型出现重复求解域。[O03]

这是一条会话状态与保护规则，不是API不存在；不为证明该接口重跑历史模型。

### D03｜mesh order与对象属性 — 纠正多边形不支持的断言

Polygon官方对象文档明确含`override mesh order from material database`及`mesh order`。先开启override，再设置对象级顺序；较小order表示重叠处材料优先级较高，不是网格更细。材料库顺序与对象覆盖设置分开。安装版本/对象若返回inactive，查该对象已知属性与开关依赖，而非删掉顺序后默认几何仍正确。[O04,O05]

网格override步长和material mesh order不能混淆。几何bbox能影响轴网格，不能用材料优先级推断实际网格节省。[O05]

### D04｜属性与默认值 — 采用版本绑定缓存＋按需查询

优先复用已验证的v241属性/schema和对应脚本；新增对象/属性、版本改变或已发生接口错误时，才做针对性原生查询。缺docs.json条目、缺快照记录、属性inactive、原生不存在是不同状态。查询需注明版本和对象类型；不把v261快照当v241能力证明。[U01]

保留精确属性名如pulselength，不用自然语言近义词猜接口。文档/图注改动不触发CAD；已有真实回读足够时不再查询全部对象。

### D05｜后端 — 现有LSF/CLI为主，MCP仅参考

本期不迁移现有Windows/v241执行链，不安装三个MCP框架来完成同一任务。可借鉴S02/S01的命令分类、结果schema和任务路由。官方MCP的持久Python片段规则属于其运行上下文，不能作为独立LSF/Python脚本必须改写的理由。

后续需要新后端时，作为独立适配项目说明安装版本、会话所有权、依赖及副作用，不能用fallback静默切换求解器/环境。此选择是本次工程建议，不是声称现有执行链无缺陷。

### D06｜Periodic/Bloch/PML — 采用物理分支，禁止固定halo万能化

法向、零横向Bloch相位的周期激励可用Periodic；存在横向相位差时采用匹配Bloch条件；宽带恒角问题需另核BFAST等适用方法，不把单频Bloch设置直接泛化。[O06]

跨周期几何必须延拓至实际边界计算区域；对相对面作一period平移后，同分量native Yee材料位置与系数对应。非均匀柱阵列不要求edge等于center；只有严格平面/均匀问题才使用横向均匀判据。halo由实际边界网格确定，旧20/35 nm不成通用常数。[O06,O07]

PML与周期halo是不同问题。即使S02来源官方，其“金属一律截短一格”“周期结构一律关闭extend through PML”等简化提示也不作为自动改物理几何规则；依实际无限延伸方向和数值故障判断。本期不改变P30 PML。

### D07｜对称/缩域 — 通用能力保留，本项目不自动采用

仅在几何、材料、源、偏振/相位和边界对称性共同满足，且数据展开/归一化定义明确时提出等价缩域。对称E/H奇偶性不能仅凭外形选择；几何平移证明不等于离散场等价。二维/对称绝对功率单位或展开倍数须独立记录。[O06]

当前用户拒绝小计算单胞，skill不得自动覆盖这项要求。可保留知识页，不新建“缩域验证”阻塞主线。

### D08｜材料与薄层 — 继承当前模型，不自动重拟合或等效

分开记录目标nk/epsilon、已安装材料类型、拟合频带与参数、实际getfdtdindex及必要finite-dt响应。修改源/仿真频带可能改变拟合和网格，须对受影响内容核对，不能把“只看500 nm”理解成必然改源。[O02,O08]

不把未知薄层强行写成面电导，不把Fe25 nm偷偷改厚；也不把“有2格”或开启conformal当精度证明。既有M0/A2已确认内容复用，不反复全材料审计。

### D09｜源与记录 — 分别定义，不预设频率数组方向

源类型由实际对象/设置确认，不据内部日志中的Gaussian字样改判PlaneSource。源带宽、时间包络、偏振、记录频率是分开的参数。500 nm任务明确f=c/(500 nm)；十点50 nm间隔需要按波长生成，再换算成真实f，不能用十个均匀频率代替。[O02,O08,O09]

废弃S03“wavelengths[0]必为最长波”的通用断言；使用实际f及同步索引排序所有数据。减少DFT记录可减相关存储/收集，但不承诺求解网格或步数同比减少。[U03,O09]

### D10｜快速验证 — 以目标分层，不设全包前置门

入口先选任务：功率/总控制域响应、局部场图、材料吸收、特定可靠性检查。功率任务不强制全域E或材料拆分；图任务不强制120面闭合；材料任务才加载matched材料/覆盖规则。报告“改什么、成本在哪下降、能说什么、不能说什么”。

成本分别报native网格、actual dt/步数、DFT采样量、初始化/运行/收集与已有真实耗时。相同大网格仅减输出叫记录减负，不叫已实现小模型；短时结果明确有限窗口。当前P30任务优先，不加P15配套矩阵，不把skill评测当新的仿真进度。[O09,O15]

### D11｜时间 — 采用停止事实＋目标量敏感性

max-time结束、auto结束、局部尾场各自记录；logged auto不是精确final，也不是吸收误差。R/T稳定不能自动证明热点复幅/相位稳定。时间对照需比较真实频率上的目标量、实际截止及源包络；相同auto导致相同实际截止的复跑，不是更长记录。[O02,O14]

不在通用skill固化1000/2900/5800 fs或1e-8为万能设置。现有P30任务的具体设置保持在项目配置中；数值敏感性达标只支持所测目标和范围。

### D12｜网格配对 — 先确认actual改动，结论分时间/空间

S30/S35只是本项目配方名称，不是通用精度级别。核对几何/材料/源/频率/控制面定义及真实mesh/dt；dt随网格改变，不能强求相等。requested mesh accuracy增加但关键override未变时，不声称关键区已细化。[O02,O14,U05]

可并行采集结果，但有限时差异仍混入空间比较时，只报联合敏感性。比较点谱须实际频率配对；场图比较须明确物理坐标和可视化重采样，不能将重采样节点拿去冒充native积分。

### D13｜容差/near-zero/certified — 不纳入原S05资格实现

按目标预先定义绝对差、相对差、归约方式和近零规则，不把0.02或0.002推广成全部任务默认。相对分母要有物理意义和稳定区；近零切换到预先约定绝对门并报告relative不适用，不能靠1e-30制造判据。参考可写为max(abs(a),abs(b))高于事先记录的尺度时才用相对差，否则用绝对差；这是一种可选合同，不替换已有项目门。

必需数据先核存在、finite、shape/频率对应；NaN/Inf/缺指标不可过滤后认证。点谱逐点比较，保留符号/复相位；只在目标明确就是聚合量时才使用均值。不得回退到坐标当指标。废弃全局certified；改为METRIC_STABLE_UNDER_SPECIFIED_CONTROL并列变量、实际变化、频点、容差和未验证项。[U05,O14]

### D14｜自动延时/加密 — 有新证据才继续，不设项目次数门

已有用户范围内，普通准备和局部修复自主推进；新的科学设置应具有明确问题、比较对象、实际变化、产物及停止/转向条件。没有人为总次数配额，也不默认repeat-until-green。

设置失败/未改变、实际截止相同、覆盖缺失靠再次同算例无法补齐时，不再科学重跑。若关键问题未解决而结果只能探索，先交有限结论；新的局部确认按真实研究需要与容量安排，不以skill名义擅改活动作业。

### D15｜插值/Yee — 可视化与材料积分两条输出路由

共点插值数据可用于明示插值方式的|E|²图；native none数据用于按各分量真实位置分析。none的Ex/Ey/Ez不能直接逐元素相加并称同点强度；绘图需明确重采样/共点方式，定量积分则保留分量坐标、相应epsilon与dual-volume。[O10,O11]

不要一律把所有监视器设none；标准power监视器与transmission遵循其支持的插值路径，原位E损耗另用native数据。三个二维场截面不能证明全壳层材料吸收。

### D16｜getresult/getdata — 采用已知schema，必要时枚举

通常getresult(m,"E")返回dataset，分量用dataset.Ex；原始分量可用getdata(m,"Ex")。只有对象实际列出可直接获取的Ex结果时才允许getresult(m,"Ex")，不得把成员名当普遍result名。[O12]

名称列表查询不等于完整数组读取；shape工具可能先取整个array才求shape。优先复用已验证对象schema，查询/导出只涉及需要的数据，不使用“inspect”名字推断零资源成本。[U01]

### D17｜维度/序列化 — 采用轴语义适配，不统一flatten

保留原shape、dtype、复数实虚部、xyz/f/t和轴顺序。只有已验证singleton维度可显式squeeze；点trace(t,1,1,1)与三维场(nx,ny,nz,nf)用不同adapter。JSON cell/引用/矩阵包装与ndarray不同，scalar也不是缺轴。

不采用S03固定quasi-2D shape和沿y直接求和；是否积分须由坐标、权重、单位及目标量决定。序列化保真、轴匹配和物理有效性分开核验。[U03,O12]

### D18｜CW/sourcepower — 采用原生语义，避免重复归一化

transmission本身已按源功率归一，且不受CW/nonorm切换影响；不能再除Pin或额外面积。原始power与E的单位/谱因子需另记，E与Pin必须同定义。cwnorm是setter，不是历史状态getter。唯一源时用默认/指定源和必要小样本核对；多源涉及相干叠加，指定一个sourcepower不自动把总E分离成该源贡献。[O13]

历史UI未记不自动否定已核的transmission。少量样本核对支持对应样本和代码链，不虚称全数组逐字一致；确需补证时只补影响当前目标的部分，不重导全部结果。

### D19｜Apodization — 按目标使用，功率不得靠加窗掩盖截断

R/T及绝对吸收按已定义、未额外加窗的源归一化口径处理。高Q谐振/衰减提取可以采用专用时窗，但需说明方法与适用量；其结果不自动沿用未加窗绝对功率解释。不将所有monitor统一改窗，也不把窗后平滑当收敛。[O16]

### D20｜零/缺失/复功率/控制域 — 必需分开

缺失用availability加null，物理零必须有相应有效记录或明确理论依据；placeholder=0不进有效能量账。原始复功率保留，物理平均实功率按对应native定义取实部和方向；不取abs(complex power)替代实流，不因无功虚部较大就判归一化失败。[O13]

Q_C是有明确边界/源参考的控制域净损耗，包含域内背景；不是自动等于Fe吸收。1-R-T需完整输入输出/符号/展开和背景参考前提，不能为凑闭合裁负值、补缺面或回填water。有限时结果还需保留时间限制。

### D21｜材料分解 — 有条件采用；没有通用native权重接口证明

采用匹配E分量、native材料数据、实际坐标与互斥物理积分域。纯材料内可使用相应损耗表达；混合单元必须区分切向/法向、斜壁/角点。几何fraction可作验证候选，不能仅凭native effective epsilon一致就证明每个材料的局部场和耗散分配已唯一确定。nearest-n、二维图乘厚度不能自动生成三维Fe量。[O10,O11]

对于e^{-iωt}且采用无源正Im(εr)约定的非磁性对角介质，可写p=ωε0/2·Σ Im(εr,j)|Ej|²；先锁定约定/单位，不能机械搬符号。完整各向异性/磁损耗另用对应本构。有效介质总损耗与物理材料分量是不同资格；无法分配的界面贡献单列，不按残差分给材料。

无E的区域不能由index生成损耗；经限定的纯材料控制体可用完整有向通量独立计量，但注明是混合测量而非全部纯体积分。不创建未经支持的runtime-loss hook。

### D22｜节点/覆盖/闭合 — 分层声明，按真实体积去重

保存名义位置、actual/snapped坐标、各分量offset及唯一节点身份。浮点序列化相容不等于坐标数学上相等；有限容差不能容许错误轴或跨单元匹配。

记录buffer允许重叠，积分ownership须互斥且覆盖所声明域；逐块/streaming限制驻留内存，禁止全胞owner_map默认常驻。轴对齐采集prism的union-boundary可作人工控制面，不与三角壳斜侧面混淆；surface两侧同材料不意味着方向错误。边链/内部面抵消只是几何证明，需全部实际通量才构成物理能量账。小截面或代表节点不自动证明完整3D覆盖。

### D23｜重试 — 按发生阶段，不照搬5次/2次循环

已确认未到科学start的语法/传输错误，局部修复后可续接未完成步骤；纯读取可采用工具级短暂重试，但不是项目求解额度。start返回未知或MPI存活时不重发；先查同run状态。保存结果已存在时优先修导出/解析/传输，不重算producer。[U03,U05]

每次有新科学运行必须保持新旧身份和问题清楚，不复用失败状态伪成功；去重标识用于阻止同run重复提交，不限制项目总算例数。

### D24｜会话与停止 — 风险匹配的所有权

本地独占短会话可用owned handle；远程已有作业的停止/修改按run/input/task/PID＋birth及必要parent链绑定，避免PID复用。close_all/reset/kill不能默认作用于整个机器；只有能证明全部属于当前授权范围时才可使用。

smpd是该Windows MPI链的历史事实，不硬编码到全部平台。对普通只读表格不要求同等进程取证。当前不触发新的停止操作。

### D25｜timeout/exit/health — 独立状态，不推断为0

分别记录controller、worker、CAD、MPI、runner、task及输出状态；timeout/缺句柄/读取失败保留UNKNOWN。退出码先检查真实值，再判0，不能将null转int变0。local session closed不等于remote host gone；端口可达不等于认证/许可恢复。

已有文件/marker不单独等于正常完成；包装器失败也不单独等于数值失败。已保存结果可根据限定独立证据继续消费，保留原错误，不重算。监控只送小型primitive数据，禁止把Process等对象图远程序列化造成RAM暴涨。

### D26｜环境/资源接口 — 不迁移、不静默改共享状态

复用已有账号、安装路径、许可来源和解释器；必要的已授权变量仅显式绑定本次子进程并保留其他环境，不回显秘密。不因库fallback修改机器PATH/许可路由/服务/策略，不自动启用v261/GPU/逆设计接口。

MPI/GPU配置区分候选设置、原生估算使用的设置与实际日志核数；不把manager的28rank估算称成实际4rank证明。此项不授权新的资源配置变更。

### D27｜资源 — 真实阶段峰值，已有适用证据可复用

分清网格/本构求解存储、DFT累积、收集、输出/分析副本和磁盘。按可能同时活动的分配估计峰值；不要把互斥阶段无脑相加，也不要只看输出CSV大小。矩形monitor按实际bbox与native axes估量，不按理想薄壳体积；后处理streaming不意味着运行期DFT免费。[O09,O15]

新网格/采集配置才更新对应原生证据；同输入证据复用，容量有实际变化或调度冲突再取必要小量状态，不恢复无目的重复RAM预检。真实CPU/带宽/许可共同决定并发是否有益，不能以空闲RAM保证提速。数值资源限制来自当前实际能力/用户约束，不写死旧项目人为配额。

### D28｜工程证据 — 最小充分，不新建通用框架

文字/图例用差异检查；解析器用明确样本和失败反例；新大运行复用现有可靠身份、输入和输出记录。已验证文件不因换报告名重导出/重积分；SHA/bytes证明身份，不证明物理；测试通过只说明测试覆盖范围。

本包execution.md中的“本项目现有无Git写入”需改成按最新人类授权决定：历史某阶段没有Git写入不是永久禁写规则，与当前用户要求GitHub交付不能冲突。不要把每项待审术语、用户批准次数、原生测试或材料full closure变成每次任务的前置门。

### D29｜许可/代码纳入 — 先原创说明与链接，后择取具体实现

本期只合并原创提炼的知识、来源链接和小型自有适配，不复制六仓库代码/厂商手册。来源清单的许可记载保留为记录，本次未逐文件完成权利审查；不能根据仓库公开、pyproject声明或邻近文件LICENSE推定全部材料可再分发。

将来确需复制某个实现时，核对该文件/commit的适用许可、NOTICE、依赖及修改说明后单独纳入；不把官方归属、MIT/Apache名目或无根LICENSE当作代码安全/物理准确保证。S05本次只执行转录的纯数值函数作审查，不导入、部署或重新分发完整后端。[包SOURCE_CATALOG]

### D30｜发布和测试 — 一个短入口、三类按需页、后端独立

保留一个核心SKILL，正文写目标路由、最低科学限制、成本意识和操作边界；细节拆modeling/results/execution，项目参数另置project profile。移除发布版中循环“等待Pro”的草案条款，归档审查决定，而不是让每次调用再次读取30项待议表。frontmatter说明何时使用；不把审稿状态写成全部任务都不能执行。

本期不引入Meep/FDTDX/MODE/DEVICE/优化作为执行必需，不升级当前Lumerical、不安装MCP、不替换launcher。文档可按本评审集中修订；新实现/安装是否启用服从实际用户范围，不把设计意见当部署已完成。

现有V01–V15保留作场景，不强制每项走原生。重点验：任务仅要图不扩成全材料；缺数据不当0；频率顺序正确；native轴正确；start未知不重复；已有结果不重算；用户范围优先；本次五个数值反例应被新资格逻辑拒绝或限制声明。先对新增受影响能力做离线/mock或行为对照；只有未解决的版本接口问题才在必要的新原生任务里局部核，不添加专门benchmark矩阵。结构检查、mock与原生兼容/物理精度分别报告。

## 执行端一次落实清单

1. 以本评审为D01–D30技术选择，集中修正文档；不再逐条问是否接受同一意见。
2. 暂不合并S05 live收敛/auto-run/通用certify，不启用S03自动重跑和固定quasi-2D规则。两者现有上游不改；只影响候选纳入选择。
3. 把原schema、纯数值反例和必要的任务路由行为测试放在本地做，不为了skill新增科学仿真或服务器轮询。测试数量是本轮实际记录，不是新的项目额度。
4. 现有P30输入、活动任务和CURRENT_TASK不由skill审阅改动；按最新用户目标继续3 μm光学证据工作。skill工作与科学计算并行，不用等候选skill全部可部署。
5. 下一次集中回执说明改了哪些条款、哪些函数仍未引入、真实做过哪些测试、是否实际安装。没有新科学数据就不称获得新的光学验证结果。

## 固定上游定位

- [U01 S01入口](https://github.com/username421421/nanophotonics-codex-skills/blob/394261d9616a409cbda7880d6bd778f52ef8b1f9/skills/lumerical-fdtd/SKILL.md)
- [U02 S02 FDTD上下文](https://github.com/ansys/pylumerical-mcp/blob/7ae8d862c30f51dfeb2357ee62ca76e4e0c1035f/src/ansys/lumerical/mcp/contexts/fdtd.py)
- [U03 S03 modeling](https://github.com/Lex669/LumericalFDTD-skill/blob/f26674b2990c1847445f1da061185b58ecd5012c/skills/LumericalFDTD-modeling/SKILL.md)；[simulation](https://github.com/Lex669/LumericalFDTD-skill/blob/f26674b2990c1847445f1da061185b58ecd5012c/skills/LumericalFDTD-simulation/SKILL.md)
- [U05 S05 convergence源码](https://github.com/davydov-nikita/lumerical-mcp/blob/fc88cc95ad04ca46ae23bea290e0fde1361257e7/lumerical_mcp/lumerical/_converge.py)

## 官方语义核查来源（阅读日期2026-10-14，不保证其新增API已适配v241）

- [O01 FDTD solver introduction / TE-TM](https://optics.ansys.com/hc/en-us/articles/360034914633-Finite-Difference-Time-Domain-FDTD-solver-introduction)
- [O02 FDTD simulation object / dimension、dt、bandwidth](https://optics.ansys.com/hc/en-us/articles/360034382534-FDTD-solver-Simulation-Object)
- [O03 newproject](https://optics.ansys.com/hc/en-us/articles/360034931473-newproject-Script-command)
- [O04 Polygon object](https://optics.ansys.com/hc/en-us/articles/360034901493-Polygon-Simulation-Object)
- [O05 mesh order](https://optics.ansys.com/hc/en-us/articles/360034915233-Understanding-mesh-order-for-overlapping-objects)
- [O06 Periodic](https://optics.ansys.com/hc/en-us/articles/360034382734-Periodic-boundary-conditions-in-FDTD-and-MODE)；[Bloch](https://optics.ansys.com/hc/en-us/articles/360034382714-Bloch-boundary-conditions-in-FDTD-and-MODE)
- [O07 boundary-region extension](https://optics.ansys.com/hc/en-us/articles/4412965790611-Is-the-boundary-condition-region-important-for-simulations-with-Bloch-periodic-boundary-conditions)
- [O08 getfdtdindex](https://optics.ansys.com/hc/en-us/articles/360034409694-getfdtdindex-Script-command)
- [O09 frequency monitor](https://optics.ansys.com/hc/en-us/articles/360034902393-Frequency-domain-monitor-Simulation-object)
- [O10 high-accuracy absorption](https://optics.ansys.com/hc/en-us/articles/360034915693-Calculating-absorbed-optical-power-Higher-accuracy)
- [O11 index_detail](https://optics.ansys.com/hc/en-us/articles/360034383134-Refractive-index-monitor-Simulation-object)
- [O12 getresult](https://optics.ansys.com/hc/en-us/articles/360034409854-getresult-Script-command)；[getdata](https://optics.ansys.com/hc/en-us/articles/360034409834-getdata-Script-command)
- [O13 transmission](https://optics.ansys.com/hc/en-us/articles/360034405354-transmission-Script-command)；[cwnorm](https://optics.ansys.com/hc/en-us/articles/360034405454-cwnorm-Script-command)；[sourcenorm](https://optics.ansys.com/hc/en-us/articles/360034925273-sourcenorm-Script-command)
- [O14 convergence testing](https://optics.ansys.com/hc/en-us/articles/360034915833-Convergence-testing-process-for-FDTD-simulations)
- [O15 native memory phases](https://optics.ansys.com/hc/en-us/articles/360046368573-Running-FDTD-simulations-from-the-design-environment)
- [O16 apodization](https://optics.ansys.com/hc/en-us/articles/360034902473-Understanding-time-apodization-in-frequency-domain-monitors)
