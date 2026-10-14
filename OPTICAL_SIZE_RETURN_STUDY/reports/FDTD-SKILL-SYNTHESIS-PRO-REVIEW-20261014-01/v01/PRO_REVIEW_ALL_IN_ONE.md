# FDTD综合Skill：单文件Pro审阅稿

固定版本：2026-10-14 / v01。仅设计审阅；所有技术选择待裁决，未安装启用。
下文整合本包自撰文档；来源为固定GitHub版本链接，不嵌入上游程序或大体积手册。

---

原文件：`PRO_REVIEW_REQUEST.md`

# FDTD 综合 Skill 草案：请 Pro 逐项裁决

版本：2026-10-14 / v01。状态：DRAFT_FOR_REVIEW，不是已批准、已安装或已验证的新skill。

## 用户原始要求

把先前找到的skill都解包，综合并结合已有经验，形成更强大的skill；具体取舍先不判断对错，列出来交给Pro判断。

本包落实到六个固定版本仓库。上一轮对部分仓库的优先推荐不是本次裁决，本包不预填推荐结果。官方、社区、既有经验均标来源，来源身份不代替具体条款的审查。

## 怎么读

1. [来源与版本清单](SOURCE_CATALOG.md)：六仓库角色、版本、完整下载情况、许可记录。
2. [候选综合skill](candidate/lumerical-fdtd-integrated/SKILL.md)：拟议模块和使用方式，未激活。
3. [30项待裁决表](candidate/lumerical-fdtd-integrated/references/decision-register.md)：每项含上游说法、不同选择、需回答的问题。全部PENDING_PRO_REVIEW。
4. [经验摘要](candidate/lumerical-fdtd-integrated/references/experience.md)：八份历史报告与本对话经验，区分观察和拟推广条款。
5. [证据定位](SOURCE_EVIDENCE.md)：28条固定commit、文件、行号、SHA256。`local_experience_index.json`记录八份本地报告身份，不包含服务器连接资料。
6. [回复格式](PRO_DECISION_TEMPLATE.md)：请按D01–D30给具体裁决，不要只评价整体“很好/可用”。

## 希望你判断什么

- 哪些条款可直接采用，哪些需改写、限定版本/对象/场景，哪些需要补证或不纳入？
- 哪些属于通用FDTD知识，哪些属于某个MCP框架约束，哪些只是本项目历史实现？
- 如何统一2D/quasi-2D、对象属性、结果读取、归一化、时间/网格比较、材料分解等口径？
- 如何支持快速趋势验证，而不把完整材料/全三维审计强制放在每次小任务前面？
- 自动修复/重试/加倍时长/修改网格的适用边界是什么？如何区分脚本错误与实际已启动/退出未知？
- 哪些模块要引入实现代码，哪些只需要参考资料？引入代码需要什么许可证与版本核查？
- 以什么有限、与风险相称的测试判断skill改善了执行？哪些检查可完全离线，哪些未来才需要授权的原生操作？

这不是申请仿真名额。用户已撤销人为MAIN/DIAG/CAD/检查次数/累计wall额度；Pro是技术顾问，不是额度或用户授权审批者。技术裁决不能自己启动仿真、修改已有作业或取代用户的操作权限边界。

## 草案当前边界

本轮只有公开源码下载、解包、本地静态阅读、文本综合和包结构核验。没有执行任何上游安装器/测试/脚本/MCP，没有访问求解器，没有服务器轮询、CAD、solve、旧数据重积分或Git写入，也没有向Pro/其他线程发送内容。

未裁决条款在候选skill里仍为议题，不是可执行默认值。当前项目的直接用户限制仍有效，不能因讨论自动重试就调用旧run。其余技术选项没有因被列入而被判定正确或错误。

## 包里包含什么、不包含什么

轻量审阅ZIP包含原创综述、候选skill、来源清单、行号链接、历史经验摘要、决策/测试模板与结构核验结果。不包含私有FSP、raw数据、凭据、连接脚本、进程身份或原始本地运行报告全文，也不重新分发上游大体积手册。

六仓库完整ZIP与1,606个解包文件另留本地 `upstream/`。这次不将六套代码机械拼成一个运行包；具体代码采用由D29/D30等裁决后再实现。

## 验证声明

归档身份、文件存在、相对链接、编号一致性、frontmatter和打包可读性可以本地核验。它们不证明API兼容、物理正确性、科学收敛、代码安全或综合skill行为优于原版。
上游测试和本项目旧测试均未重跑；行为验证方案只列入[待执行场景](candidate/lumerical-fdtd-integrated/references/validation-scenarios.md)，未伪报通过。


---

原文件：`SOURCE_CATALOG.md`

# 六套上游完整归档

所有原始文件已解包，安装器/测试/MCP/server/solver均未执行。只重点阅读FDTD入口及相关模块，并未逐行审计所有源码或阅读每份PDF。

|ID|仓库|固定commit|文件数|ZIP大小(MB)|
|---|---|---|---:|---:|
|S01|[username421421/nanophotonics-codex-skills](https://github.com/username421421/nanophotonics-codex-skills/tree/394261d9616a409cbda7880d6bd778f52ef8b1f9)|`394261d9616a409cbda7880d6bd778f52ef8b1f9`|1118|34.47|
|S02|[ansys/pylumerical-mcp](https://github.com/ansys/pylumerical-mcp/tree/7ae8d862c30f51dfeb2357ee62ca76e4e0c1035f)|`7ae8d862c30f51dfeb2357ee62ca76e4e0c1035f`|92|0.19|
|S03|[Lex669/LumericalFDTD-skill](https://github.com/Lex669/LumericalFDTD-skill/tree/f26674b2990c1847445f1da061185b58ecd5012c)|`f26674b2990c1847445f1da061185b58ecd5012c`|22|0.05|
|S04|[wfy-op/codex-for-comsol-lumerical](https://github.com/wfy-op/codex-for-comsol-lumerical/tree/375c4dafa24d8f75f45ac5ace92d80eafb7ec596)|`375c4dafa24d8f75f45ac5ace92d80eafb7ec596`|156|442.38|
|S05|[davydov-nikita/lumerical-mcp](https://github.com/davydov-nikita/lumerical-mcp/tree/fc88cc95ad04ca46ae23bea290e0fde1361257e7)|`fc88cc95ad04ca46ae23bea290e0fde1361257e7`|180|0.40|
|S06|[zxqcreations/Lumerical_MCP_Skill](https://github.com/zxqcreations/Lumerical_MCP_Skill/tree/40ccd5eefe2b065448d150140044610fe46727f7)|`40ccd5eefe2b065448d150140044610fe46727f7`|38|0.10|

S01/S03/S04含标准SKILL.md；S02/S05是MCP工具库；S06包含skill/lumerical.md及MCP实现。不能把全部仓库都称为已可直接安装的同格式skill。

本地原始归档：`../upstream/S01` 至 `../upstream/S06`，每项包含原ZIP、source/和file_inventory.csv。轻量Pro包不含原始源码/手册，固定版本链接可用于查阅。

## 许可记录（非法律结论）

- S01：保留NOTICE.md；不能把其他子目录的LICENSE推定适用于lumerical-fdtd全部材料。
- S02：根目录Apache-2.0 LICENSE。
- S03：根目录MIT LICENSE.txt。
- S04：根目录未发现通用LICENSE；某嵌套COMSOL runtime的许可证不扩展到全部FDTD内容。
- S05：根目录MIT LICENSE，另有benchmark参考文件的单独license.txt。
- S06：pyproject声明MIT；归档没有独立LICENSE正文，保留此差异待核。

目前没有复制上游实现到候选skill，也未替上游重设许可证。是否能整合、再分发哪些代码另列D29。

## 获取说明

匿名GitHub API首次HTTP403限流；改用公开codeload归档，无凭据。提交号来自GitHub ZIP comment，完整归档及每个解包文件都记录SHA256；commit日期未单独查证，manifest中保留null。branch只作发现入口。

全包中的非FDTD资料也保持原样，但不因此自动纳入综合skill。

---

原文件：`candidate/lumerical-fdtd-integrated/SKILL.md`

---
name: lumerical-fdtd-integrated
description: Use when reviewing or designing Ansys Lumerical FDTD modeling, solver settings, automation and result interpretation workflows. This review draft organizes multiple sources and project experience; it is not an activated execution skill.
---

# Lumerical FDTD Integrated

**DRAFT_FOR_REVIEW / NOT_INSTALLED / TECHNICAL_CHOICES_UNADJUDICATED**

本草案拟将六套上游能力与历史经验整理为一个可按需读取的skill。它当前只服务方案审阅，不授权或驱动CAD、solve、远程会话、kill、重试、安装或配置改变。不能把本草案的候选条款当成已获裁决的执行指令。

## 拟议能力

|用户任务|候选输出|按需阅读|相关决策|
|---|---|---|---|
|描述结构并建模|几何/材料/源/边界/网格/监视器参数契约与建模脚本方案|[modeling](candidate/lumerical-fdtd-integrated/references/modeling.md)|D01–D09|
|做快速趋势验证|目标量、保真边界、成本分项与可比较范围|[modeling](candidate/lumerical-fdtd-integrated/references/modeling.md)|D10–D14|
|读取现有结果|数据轴、坐标、归一化、缺失状态和目标量定义|[results](candidate/lumerical-fdtd-integrated/references/results.md)|D15–D22|
|连接、运行、修复|会话所有权、具体副作用、运行身份与失败分类方案|[execution](candidate/lumerical-fdtd-integrated/references/execution.md)|D23–D28|
|组织可靠性证据|各目标量的适用证据、剩余缺口和候选对照|[validation scenarios](candidate/lumerical-fdtd-integrated/references/validation-scenarios.md)|D11–D14、D20–D22|
|维护或移植skill|版本、来源、许可、实现依赖与模块边界|[decision register](candidate/lumerical-fdtd-integrated/references/decision-register.md)|D29–D30|

## 本轮审阅方式

1. 对照用户真实目标，区分“只问设置”“建模但不求解”“处理已有数据”“启动新例”等请求。不要因为参考包提供了全流程能力就替用户扩大任务。
2. 将上游说法、具体版本、历史观察、候选推广和未决问题分别呈现；[决策表](candidate/lumerical-fdtd-integrated/references/decision-register.md)是未决项的唯一清单。
3. 每个拟采用条款应能追溯到来源或标注为本次综合提议。参考[来源映射](candidate/lumerical-fdtd-integrated/references/source-map.md)与[经验摘要](candidate/lumerical-fdtd-integrated/references/experience.md)。
4. 不替Pro预选方案。收到实际裁决后，在具体版本、对象、前提、例外、证据和措辞层面更新；相互冲突的裁决单独列出，不能静默选一个。
5. 本草案不重新解释现有的用户权限、项目隔离、禁止覆盖历史、暂停轮询或无人工额度要求。技术方案的裁决和实际执行授权是不同事项。

## 拟议工作产物

未来实现可按任务选用[模板](candidate/lumerical-fdtd-integrated/references/templates.md)，不要求每次小改动生成整套工程档案：

- `model_contract`：对象、材料、源、边界、网格、记录方式、目标量与近似。
- `operation_intent`：动作、输入、已有结果可复用性、预期副作用、失败后的事实记录。
- `result_summary`：量的定义、实际时间/频率/坐标、归一化、适用范围和缺失证据。
- `decision_record`：来源、版本、裁决范围、必要验证和实际做过的检查。

这些字段只是候选结构，不是要求引入新的通用launcher/consumer框架。现有能完成任务的项目工具是否复用、哪些代码需要引入，留给D28–D30。

## 不能声称已经完成的事项

没有融合运行上游六套后端；没有完成其v241/v252/v261兼容测试；没有完成科学裁决或独立行为测试；没有建立新的材料权重接口；没有新的轻量模型或仿真结果。本轮交付的是可追溯、可裁决的综合设计草案。


---

原文件：`candidate/lumerical-fdtd-integrated/references/decision-register.md`

# 待 Pro 裁决的30项具体取舍

所有项状态均为 **PENDING_PRO_REVIEW**。下列“方案”只是可讨论选项，顺序不代表推荐；Pro可提出新方案。来源E编号见审阅包SOURCE_EVIDENCE.md；L编号见experience.md。未声称每项都是直接矛盾，有些是互补能力、上下文差异或本项目希望新增的内容。

## D01 2D、quasi-2D与3D
来源：E02、E03；S03列禁止2D并使用薄3D周期替代，S02描述原生2D的坐标与偏振约定。
方案：保留S03限制作为特定案例模板；允许按不变方向选原生2D；将quasi-2D单列为需说明的模型近似。
请裁决：各方案适用的物理前提、版本、TE/TM定义、可比较量是什么？如何避免自动把本项目3D三角柱替换成2D？

## D02 newproject与求解器对象生命周期
来源：E23、E17、E18；S03禁止newproject，MCP实现同时提供新建/载入/切layout接口。
方案：禁用某入口；只在新空白会话允许；在保存与所有权条件下按阶段开放。
请裁决：创建新项目与修改已有分析项目分别应怎样处理？限制是否属于框架约定而非API不存在？

## D03 mesh order与对象属性
来源：E11、E12；S03称多边形不支持mesh order，S01描述结构对象的mesh order及override前置条件。
方案：保留对象/版本特例；运行时查询后设置；使用材料库顺序或其他建模表达。
请裁决：对象级和材料级属性如何区分，具体版本需查哪些证据？不能只凭一份快照给全版本结论。

## D04 属性查询与默认值
来源：E01、E07、E13、L07；有安装版API/快照检索、v261接口清单和本项目原生属性名修正经验。
方案：保存已验证属性表并限定版本；每个新对象局部查询；建立版本适配层。
请裁决：哪些变更才值得打开CAD查询？缺docs.json/快照无条目与运行时无接口如何区分？

## D05 API、CLI还是MCP
来源：E01、E06、E18、E20；S02偏持久Python片段，S04偏API优先与CLI fallback，S01兼容既有项目脚本，S06有多产品工具层。
方案：统一MCP；直接lumapi/LSF为主；按交互与批处理分后端。
请裁决：现有远端WinPS/LSF链是否需要替换？何时仅导入参考知识？各方式的会话与版本依赖如何表达？

## D06 Periodic、Bloch、PML与跨边界几何
来源：E10、E19及本项目periodic/halo背景。
方案：按源角度/周期向量分支；调用验证工具给建议；使用经限定的结构模板。
请裁决：需要检查哪些几何覆盖、周期一致性、网格和入射条件？静态风险与已证明边界伪影分别怎么描述？

## D07 对称边界与缩小计算域
来源：E10、E19；上游讨论通过对称减少区域，并要求相应源/场奇偶性及对照。
方案：仅用户明确指定；自动提出候选但不代入；有对称证据后采用。
请裁决：三角阵列/层状材料/偏振共同满足哪些条件才可缩域？成本收益如何报告而不承诺倍数？

## D08 材料库、拟合与薄层表达
来源：E11、E13、E14、L04。
方案：继承项目材料；重新拟合目标频段；用体材料或有明确前提的等效表面表示。
请裁决：复n/epsilon、频散拟合区间、被动性、薄层网格与模型变化要分开记录哪些内容？等效表达是否适用于当前层叠不能预设。

## D09 源类型、带宽、偏振与频点
来源：E14、E15、L01。
方案：固定宽带源仅改记录频率；目标窄带源；依目标使用plane/Gaussian/TFSF/mode等模板。
请裁决：改变源带宽对脉冲长度、材料拟合和可比性的要求？少记录频点能削减哪些开销，不能直接推出哪些加速？

## D10 真正快速验证的目标和保真边界
来源：L01、L07及本对话用户“轻量快速验证”纠偏；E13、E15。
方案：完整物理几何只减记录/时长；数值粗筛；在已证明等价条件下缩域；另行定义物理近似模型。
请裁决：各自可保留哪些结论？用网格量、步数、记录量和实际runtime怎样区分成本来源？是否只做一个代表试算再决定后续？

## D11 时间窗口与auto-shutoff
来源：E13、E19、E26、L01、L02。
方案：按停止状态分类；按目标量随时间变化判断；自动延时或给出有条件的延时建议。
请裁决：max-time结束、auto结束、局部点尾场分别可说明什么？哪种证据足以支持特定R/T或热点量的时间结论？

## D12 S30/S35等网格配对
来源：E19、E27、L01。
方案：短窗口先比较敏感性；先取得时间证据再做网格结论；成本允许时并行采集但分开解释。
请裁决：实际dt、截止时间、源、几何、记录面、频率哪些必须可比？单点/整谱/热点各自如何定义指标？

## D13 容差、near-zero和certified标签
来源：E09、E27；S05默认相对tol0.02并产生certified标签；本项目曾用绝对0.002作为特定目标量的工作指标。
方案：按目标量指定绝对/相对或混合容差；保留后端标签并写范围；改用局部稳定性描述。
请裁决：归约方式和near-zero分母如何设定？一个数值控制的稳定性可支持多宽的结论？所有数字仍是待审议例子，未设新默认。

## D14 自动加密、延时与停止条件
来源：E05、E26、E27、L01。
方案：自动循环执行；只生成下一步建议；按已授权的具体实验设计逐例执行。
请裁决：如何判别新的有效证据与重复运行？如何避免同一auto截止的复跑？何时足以交探索性结果？不得引入人为配额替代技术判断。

## D15 监视器插值、共点图与native Yee数据
来源：E15、L04、L05、L06。
方案：nearest-mesh共点图；none/native分量数据；按可视化与定量积分分开导出。
请裁决：各输出可支持哪些物理量？如何记录实际分量坐标/offset，避免把漂亮场图当定量材料积分？

## D16 getresult/getdata及dataset成员
来源：E08、E22；S03直接getresult(Ex)示例，S01区分result名与成员名。
方案：按对象的已知schema读取；先枚举相关结果再取dataset成员；按版本封装不同路径。
请裁决：哪些对象/接口允许直接Ex，哪些需要E dataset或getdata？列表读取、shape查询是否会实际搬运大数组？

## D17 维度、shape与序列化
来源：E18、L02。
方案：按原生dataset轴schema解码；只对已证明singleton维度适配；维持原shape并由下游显式选择。
请裁决：如何区分4D点时序、矩阵场、坐标scalar、复数JSON与真实ndarray？何时允许squeeze/reshape而不掩盖轴置换？

## D18 CW、sourcepower与原始功率
来源：E14、E15、L04、L05。
方案：显式记录导出归一化；继承同一次已保存设置；对未知历史数据仅给限定解释/必要新证据。
请裁决：native transmission、P/Pin、E幅值分别需要哪些定义？何时可能重复归一化？少量样本一致的证明范围是什么？

## D19 Apodization与频域结果用途
来源：E15、E13。
方案：功率响应与谐振分析分别设置；继承原monitor设置；允许任务指定窗函数。
请裁决：窗函数对功率归一化、Q提取和对比的影响应如何说明？不能给所有monitor统一默认而不区分目标。

## D20 缺失功率、复功率与控制域口径
来源：E16、L03、L04。
方案：完整预算与partial-known分列；规定可用性schema；在具备适用依据时采用实功率预算、虚部诊断。
请裁决：placeholder0、null、无数据与物理零如何区别？Q含背景的定义、法向符号、复功率处理与R/T/A关系分别如何命名？

## D21 材料分解、conformal与混合单元
来源：E08、E11、L04、L05。
方案：仅输出有效介质损耗；有材料权重证据后分量积分；限定纯材料内部/特定界面的解释。
请裁决：切向、法向、侧壁、角点需要哪些不同证据？geometry fraction、nearest-n或二维E图乘厚度在哪些前提下可用或不可用？本轮不作结论。

## D22 节点身份、记录支持与闭合
来源：L03、L04、L06。
方案：分别报告名义坐标、实际坐标、节点身份与覆盖；建立特定误差界；以额外原生记录验证。
请裁决：serialization-compatible节点是否能替代物理坐标相等？component envelope、边链抵消、full3D coverage及native energy分别需要什么？

## D23 出错后的重试策略
来源：E04、E05、E06、L03、L08。
方案：次数有界重试；按失败发生阶段与确切退出决定；保留结果并只处理失败的后段。
请裁决：纯语法错误、未调用start、start未知、MPI存活、结果已保存分别怎么处理？次数参数应是工具机制还是项目额度？当前历史noReplay不因讨论而解除。

## D24 会话、进程所有权与停止接口
来源：E18、E20、L03、L05、L01。
方案：MCP命名session；单机handle；远端明确run/input/PID/birth/parent链。
请裁决：哪类工作需要何种强度身份核验？close_all/cancel/stop如何限定所有权？本项目smpd经验怎样抽象而不硬编码所有平台？

## D25 超时、退出和健康状态
来源：E25、E17、L03、L05、L01。
方案：按操作配置调用timeout；异步handle后续闭合；由独立观察确认完成。
请裁决：controller超时、worker退出、MPI退出、runner失败、task Running、local session closed如何分别表达？如何避免把端口可达当认证恢复？

## D26 环境、许可与MPI/GPU资源设置
来源：E06、E07、E20、L01。
方案：仅使用既有环境；在子进程内覆盖已授权变量；由外部配置提供后端参数。
请裁决：API fallback、许可变量、PATH和资源改变属于什么副作用？本项目现有“不改许可路由/账户/服务/策略”等用户限制继续有效。

## D27 资源估算与实测
来源：L01、L07；S05/S06包含资源工具，E20。
方案：使用已有适用估算；必要时一次实测；由监控策略按风险触发。
请裁决：基础网格、时间步数、记录、收集峰值、磁盘、CPU/带宽和许可怎样共同判断？不能把“有空闲RAM”直接翻译成保证加速，也不恢复无目的重复RAM预检。

## D28 工程证据强度与流程负担
来源：E01、E18、L03、L08。
方案：轻量文件版本记录；必要时锁定输入与实际buffer；大任务使用现有可靠入口和事务记录。
请裁决：哪些任务需SHA/bytes/实际执行代码身份/锁，哪些只需小范围验证？怎样避免每个小修复生成新框架、重复测试或审计报告替代科学进展？

## D29 许可、依赖与实现代码合并
来源：E21及SOURCE_CATALOG.md许可记录；S02/S03/S05的根许可证、S04/S06不同许可材料分别保留。
方案：只综合原创说明和链接；逐模块许可确认后复制；将后端保持独立外部依赖。
请裁决：哪些代码真的值得纳入、相应许可/NOTICE/依赖约束是什么？技术判断不替代权利人的许可；未发现根LICENSE不自动判有权或无权。

## D30 Skill边界、测试与发布
来源：六源整体、L01–L08。
方案：一个按任务路由的skill；多个建模/执行/分析子skill；独立backend适配加共用知识层。
请裁决：Meep/FDTDX/MODE/DEVICE/优化是否仅附录还是本期范围？如何测技能检索和决策行为？安装、自动触发、版本更新和失败回退如何组织？本轮结构检查不等于行为或物理验证。


---

原文件：`candidate/lumerical-fdtd-integrated/references/modeling.md`

# 建模与快速验证：候选综合工作页

状态：待裁决设计，不是可执行配置。对应D01–D14。

## 将自然语言要求转成可检查的模型

拟将S03的需求分解、S01的API/物理主题路由、S02的分阶段构建和S05的设置检查组成如下工作页。是否采纳各步骤及自动化程度待Pro决定。

|层次|候选记录字段|可复用上游材料|待判断的分支|
|---|---|---|---|
|研究目标|R/T、场图、局部通量、材料吸收、Q、远场、S参数；频段/点频率；趋势或定量|S01 how-to；S05 recipes/FOM|目标不同是否使用不同验收和输出|
|物理对象|尺寸、层厚、周期向量、有限阵列/周期阵列、入射介质、坐标原点|S03 modeling；S01 geometry-materials|原生2D/quasi-2D/3D及缩域条件|
|几何表示|原始对象、组、相对坐标、跨周期碎片、重叠顺序|S01 geometry-materials；S02 geometry|对象/材料mesh order、材料交叠和周期边界覆盖|
|材料|材料名、数据库/自定义模型、拟合频段、复n/epsilon、各向异性|S02 materials；S05 materials|薄膜等效、模型变更和版本可比性|
|光源|类型、位置、方向、偏振、幅值、相位、频带、时间包络|S01 sources；S02 fdtd_source_types|源带宽与记录频率分开设置|
|区域与边界|每轴边界、PML profile/layers/距离、对称条件、Bloch波矢|S01 boundaries-symmetry；S02 fdtd_boundary_conditions|边界/源/几何适配及对照方式|
|离散化|requested override、实际axes/dt、conformal、growth、稳定性|S01 mesh；S02 fdtd_mesh_and_convergence|薄层/角点、粗筛与网格对照|
|记录契约|对象名、类型、组件、频点、插值、downsample、apodization、实际坐标|S01 monitors-results；S03 building-blocks|图像用途与native积分用途|

不在这份草案中设定通用默认的波长、网格步长、PML距离、auto阈值、仿真时长或容差。上游示例数值保留出处，由对应决策确定适用范围。

## 从一次建模任务走到产物的候选阶段

需求/已有模型识别 → 参数化几何 → 材料与源 → 区域/边界/mesh → 监视器 → 独立新模型保存 → 相关设置回读 → 资源与执行意图说明。

这里只描述分段产物，不预先要求每次必须打开CAD、跑小试或重新进行全物理审计。只改文档、后处理图例或单个解析器时不自动进入这条完整流水线。具体轻量检查由D28裁决。

## 快速验证候选卡

每种加速策略分别回答“改变什么、节省哪个部分、保留哪个量、损失哪个量、如何验证”。

|候选策略|需报告的改变|需观察的成本|可比较范围待Pro定义|
|---|---|---|---|
|只减DFT频点/组件/记录面|源保持或改变必须写明|monitor累积/收集/保存大小|目标频点场图/功率是否足够|
|缩短运行窗口|max time、实际stop和衰减状态|真实步数、初始化与运行时间|有限时趋势/热点是否稳定|
|数值粗筛|mesh/conformal/dt变化|native网格量与步数|哪些指标只作探索，怎样建立对照|
|对称/最小等价胞|几何与源的对称/平移条件|计算域减少及通信开销|是否与原完整周期问题等价|
|物理近似模型|删减结构、维度或材料表达|网格和求解器变化|仅回答哪个问题、不能回答哪个问题|
|并行/后端改变|ranks/threads/GPU/license|实际吞吐、峰值、共享带宽|性能比较与数值一致性分开|

本项目“减少记录但仍大网格”的经验作为L01/L07背景。它不预先排除减记录的价值，也不证明其他策略对当前三角阵列必然有效。

## 网格/时间对照的候选对比契约

记录case pair、真正改变项、保持项、actual source/frequency、实际时间/网格/dt、对应目标量、绝对差/相对差定义、near-zero处理、遗漏证据。是否允许并行采集、先时间后网格、跨窗口比较，分别交D11–D14。


---

原文件：`candidate/lumerical-fdtd-integrated/references/results.md`

# 结果读取与科学解释：候选综合工作页

状态：待裁决设计。对应D15–D22；来源E08、E13–E19、E22、L02–L06。

## 结果层次

拟分开保存下列信息，是否纳入正式schema及粒度由Pro判断：

1. 结果属于哪个saved model/run/export，是否完整、可用、只读或仍被写入。
2. 原生对象名、result name、dataset成员、getresult/getdata路径与所用版本。
3. 数据shape、dtype/complex、轴顺序、xyz/f/t、分量offset、插值与采样。
4. CW/脉冲/原始幅值模式、Pin或源参考、monitor法向与符号。
5. 计算的目标量、单位、空间/频率/时间范围、缺失值与实际用到的数据。
6. 图像表达、数值比较与科学结论的各自范围。

候选接口优先级尚未选定：复用已验证schema、按需枚举、针对版本封装等都留在D16。不能把本表里的字段可记录等同于已取得这些证据。

## 四种不相同的分析任务

|任务|候选必要输入|拟议输出|还需Pro判断|
|---|---|---|---|
|R/T与控制域通量|native P/T/Pin、方向、背景、记录频率|原始值与明确定义的归一化量|R+T+A关系、背景贡献、复功率、缺失面|
|局部场图|Ex/Ey/Ez和实际坐标/插值|复场、幅值或强度图及切片信息|共点合成、热点可比性、图像能否支持定量声明|
|材料吸收|相应材料/场/constitutive信息、体积与覆盖|在已判定适用条件下的材料量|混合单元权重、法向/切向、端点、conformal与积分|
|Q/远场/S参数|适合该目标的monitor与analysis/source模式|目标特定指标|时窗、投影介质、端口归一化、模态与相位定义|

## 数据接口候选要求

- 原始数组与JSON序列化结构分别描述。L02中专用点shape修复不作为“全部数据都flatten”的通用许可。
- 对读取成本建立标注：只列名称、读取header、传输完整数组、运行analysis、导出结果分别有什么实际开销。不能只看工具名字判断它是纯metadata操作。
- 缺失/未知/真实零使用何种schema由D20裁决；历史原始记录不因新schema被重写。
- 浮点坐标、节点索引、snapped monitor位置及名义几何分别保留的形式由D22裁决。ULP、绝对容差和唯一匹配的阈值不从本案例复制成普适常数。
- 在有限内存中逐块读取、计算与释放的实现候选可以来自现有项目工具；是否引入新缓存、并集去重或通用consumer须另评估，不能因为skill综合就重算旧积分。

## 科学声明候选字典

`source_definition`、`normalization_scope`、`actual_cutoff`、`metric_time_sensitivity`、`metric_grid_sensitivity`、`material_assignment`、`recording_coverage`、`energy_balance_scope`。

这是比单个全局PASS更细的表达提议。标签数量和措辞可以调整；Pro需指定哪些支持“探索性”“限定范围稳定”“定量验证”等表述。本轮未授权给任何旧数据升级资格。


---

原文件：`candidate/lumerical-fdtd-integrated/references/execution.md`

# 连接、执行和失败处理：候选综合工作页

状态：待裁决设计。对应D05、D23–D30。没有可直接运行的launcher或MCP配置。

## 三种后端候选

|后端|已有素材|需要界定的范围|
|---|---|---|
|直接lumapi/LSF脚本|S01/S03/S04；项目已用脚本|安装路径、Python/WinPS版本、进程所有权、输出目录与退出|
|官方PyLumerical MCP|S02持久Python会话和guidelines|会话名、预置handle、片段执行、工具依赖及版本兼容|
|社区MCP|S05校验/恢复/FOM；S06多产品/MPI等|工具声明与真实行为、自动副作用、并发模型、任意eval权限|

这些不是必须同时安装的三个层。哪些只作参考、哪些被采用，由D05/D30决定。命令/工具可用性不从README反推为当前已连接。

## 动作和潜在副作用清单

|操作类别|候选例子|需要记录的副作用边界|
|---|---|---|
|离线文档查询|S01 lum_docs/lum_example|是否只读安装文件/缓存，快照适用版本|
|会话探测|S04 probe、S02 open_session|是否启动CAD、消耗许可证、写日志/临时文件|
|模型构建|add/set/delete/save|是否修改已有会话或新副本；保存目标|
|读取结果|getresult/getdata/export|是否完整数组搬运、运行analysis、改norm或写盘|
|启动/扫描|run/run_sweep/auto_run|新进程、资源占用、多个case、实际start未知|
|重置/取消|newproject/switchtolayout/reset/stop/cancel|已有结果、活动任务、所有权和可恢复性|
|环境与资源|许可变量、PATH、MPI、GPU|当前子进程还是共享配置，是否触及未授权路由|

## 失败阶段候选分类

本轮不预设自动重试次数或自动延时策略。提供以下事实分类供D23/D25裁决：

- 输入/语法/导入失败，确认未调用原生start。
- 会话打开失败，未获得已认证远端身份。
- 已调用start，但返回/handle/actual PID不完整。
- 原生进程仍在运行，controller已超时或断开。
- 原生进程已退出但保存/导出/传输失败。
- 结果已保存，后处理/身份查询/状态写入失败。
- 元数据事务已开始但未完成，是否存在更新的状态。

对每类分别回答：允许修复什么、需要什么新证据、是否允许重新运行科学producer、如何保留旧error/exit/null。L03的saved-result核验可作一种案例，不把它强制为所有工具的通用架构。

## 保护与可追溯性的粒度

候选层次从文件路径/版本/参数记录，到input SHA与输出manifest，再到实际buffer/锁/进程创建时间/parent链。D28决定在不同风险下选什么，不预设“每个小改动都必须最大审计”。

本项目现有无Git写入、暂停自动轮询、不改活模型/账户/服务/许可路由/策略、保留历史的直接要求不因新skill而消失。它们是本项目权限边界，不是Pro需裁定的物理命题，也不应硬编码成所有其他项目的固定路径/PID/次数。


---

原文件：`candidate/lumerical-fdtd-integrated/references/experience.md`

# 既有经验：观察、候选推广和未决问题

本节是历史材料的本地复读，不是今天的服务器状态或新的原生核验。所有经验都保留适用范围；“候选推广”不是本轮已采用的通用规则。八份报告的相对路径/SHA/bytes见审阅包 `local_experience_index.json`。

|ID|历史事实/报告范围|候选推广方向|留给Pro的问题|
|---|---|---|---|
|L01|P30 S30短例生成了601×448×999网格、约39.4GB原生估算；启动确认只看到meshing。该报告不证明后来状态|区分准备、启动、步进、完成和资格；分开物理模型轻量与记录轻量|如何让快筛更快且保留目标量？短窗口网格对照怎样解释？|
|L02|原生点trace有(96783,1,1,1)；原vector解析失败，经专用单点轴/dt校验适配|保存原生轴语义，针对已知结构解码|通用schema与专用adapter的边界是什么？|
|L03|worker保存产物退出0，而controller在退出后身份查询WinError31退出1；独立处理保存结果，未重跑producer|区分计算结果、运行包装器、状态消费的独立事实|哪些恢复能只处理已保存数据？不能只从controller1推出solve失败，也不能抹去它|
|L04|四历史面记录power unavailable，数值0为placeholder；原有效损耗积分未取得完整CW/材料权重/coverage资格|缺失与零、effective loss与材料吸收、形式预算与物理闭合分开|如何设计小而明确的数据/结果标签，避免变成永无止境的全域审计？|
|L05|243个复场样本旧/loaded/明确CW相同，但未证明全域及历史UI；engine真实parent含smpd|样本证据不自动扩大；进程链按实际平台|何时需更多样本/全域证据？怎样防止为补历史证据重复大导出？|
|L06|两个非零坐标差以原值保留；在限定条件下节点身份相容；边链抵消与175/107/78记录包络诊断分开|将节点身份、坐标相等、覆盖与能量身份分成不同声明|哪些量能共享容差？哪些拓扑结果不能替代物理闭合？阈值怎样重新确定？|
|L07|P30准备首次拒绝pulse length，实际属性为pulselength；准备验证另遇scalar/matrix结构差异|API精确属性与运行时结构和版本绑定|怎样优先复用已知API，避免每次完整探针？|
|L08|Windows路径/API、实际父管道验证通过后仍可在原生格式解析阶段失败|把filesystem/transport/native-format/science分层|工程验证的最小充分范围是什么？哪些无须跨两种shell反复验证？|

## 本对话的执行经验，不冒充科学测量

- 用户希望轻量快速验证；此前减少监视器后仍保留完整大网格，并继续长时/细网格/材料审查，后来被用户纠偏。这是目标与执行路线的偏差，不能仅靠增加审计解决。
- 用户允许有实际容量时推进有用仿真，并撤销人为次数/名额/累计wall额度。不能把技术工具里的max_retries之类参数重新解释为项目额度。
- 已完成操作被重复检查或为已知缺口不断生成准备/等待文件，不能算新的科学证据。如何既保留必要保护又减少流程负担，交D28裁决。
- 原生接口不可得、未导出或历史未记录，应作为具体缺项，不据此自动改物理模型或虚构数据。哪些缺项影响哪个目标量需明确，而不是全项目一律停工。

## 记忆使用范围

历史记忆仅用于定位相关主题，最终经验条目来自本轮复读的八份本地报告和本对话。其他项目“每步等Pro”的旧约定未引入本综合草案，也未修改任何记忆文件。没有查询当前作业健康、RAM或完成情况。


---

原文件：`candidate/lumerical-fdtd-integrated/references/source-map.md`

# 候选资源映射

固定commit和文件哈希在审阅包的SOURCE_CATALOG.md、SOURCE_EVIDENCE.md与source_manifest.json中。这里是拟议使用范围，不是采用决定。

|来源|已有可综合的知识/实现|与草案的连接|尚未做的事|
|---|---|---|---|
|S01 nanophotonics-codex-skills|lumerical-fdtd入口、物理/API主题参考、waveguide/grating/dipole示例；lum_docs.py、lum_example.py、lint_lumerical.py、lum_introspect.py、inspect_results.py|建模、版本查询、结果schema、定向验证|未运行脚本；未确认快照与本项目版本逐项兼容；未采用其所有其他skill|
|S02 ansys/pylumerical-mcp|contexts下general/fdtd/geometry/materials等指南，持久会话和Python执行|官方主题说明与一种后端方案|未安装MCP/PyLumerical；未迁移现有v241脚本|
|S03 Lex669/LumericalFDTD-skill|modeling/simulation/analysis/full四模块、building-blocks/common-errors/API/diffraction参考及模板|需求分解、建模/执行/分析分段、图表产物|未启用自动修复循环；未把模块里的版本约束判成通用物理规律|
|S04 wfy-op/codex-for-comsol-lumerical|lumerical-fdtd的probe_lumerical.py/.sh、automation参考和profiles|连接故障分类、API/CLI选项|未运行probe、改PATH或许可环境；未采用COMSOL部分|
|S05 davydov-nikita/lumerical-mcp|validate/assess/diagnose/converge/loop、工具封装、FOM、benchmark和examples|设置检查、自动化候选、指标抽取、未来测试素材|未执行mock或live测试；未接受certified为项目全局科学资格|
|S06 zxqcreations/Lumerical_MCP_Skill|skill/lumerical.md、tools目录；MPI、inverse design、CML、AALI接口|工具分类、多产品扩展、并行/资源候选|未安装；未核v261功能能用于v241；未启用stop/reset/close_all|

## 尚未合并的实现

候选skill当前不包含上游Python/LSF/PowerShell实现。原始源码均保存在包外的upstream/并保持原样。
后续如需采用某个脚本，请Pro标明：文件与commit、采用的具体能力、需要修改的语义、版本条件、依赖/许可证、离线和原生验证分别是什么。不能以“整仓库都装上”替代这些具体选择。


---

原文件：`candidate/lumerical-fdtd-integrated/references/templates.md`

# 候选模板字段

这些是综合设计的数据字段，不是运行配置。所有物理值由具体任务提供；`unspecified`和空数组是明确未填写状态，不得直接转换成solver默认值。是否采用/简化由D28/D30裁决。

## 模型契约

```yaml
study_question: unspecified
target_quantities: []
model_identity:
  solver_version: unspecified
  api_backend: unspecified
  parent_input: unspecified
  geometry_and_materials: unspecified
  approximation_scope: unspecified
source_and_domain:
  source_definition: unspecified
  boundaries: unspecified
  mesh_requested: unspecified
  mesh_actual: unspecified
  time_requested: unspecified
  stop_observed: unspecified
recording:
  quantities: []
  frequencies: []
  interpolation_and_components: unspecified
  normalization: unspecified
comparison:
  changed_parameters: []
  preserved_parameters: []
  metric_and_tolerance: unspecified
```

## 操作意图

```yaml
requested_action: unspecified
authorization_scope: unspecified
existing_result_reuse: unspecified
new_evidence_expected: unspecified
input_identity: unspecified
outputs_and_side_effects: []
actual_capacity_evidence: unspecified
start_state: NOT_EXECUTED
failure_stage: NOT_OBSERVED
replay_or_recovery_policy: PENDING_TASK_SPECIFIC_DECISION
```

## 结果摘要

```yaml
quantity_definition: unspecified
units_and_sign: unspecified
domain_and_background: unspecified
frequency_and_actual_cutoff: unspecified
data_axes_and_shape: unspecified
availability: UNKNOWN
normalization_evidence: unspecified
performed_checks: []
reused_evidence: []
pending_evidence: []
claim_scope: unspecified
```

这些字段不会生成新的启动脚本，不以“填写完表格”代替科学或运行证据。小任务可只填写相关部分。


---

原文件：`candidate/lumerical-fdtd-integrated/references/validation-scenarios.md`

# 裁决后的候选验证场景

状态：NOT_EXECUTED。本表是后续测试设计，不是本轮测试通过清单。Pro先定义适用行为，再决定怎样测试；本轮不通过预设科学答案抢先裁决。

|编号|输入情境|需要观察的行为|对应决策|
|---|---|---|---|
|V01|只要求建模脚本，不运行|是否保持请求范围；哪些检查只在本地完成|D02、D05、D30|
|V02|明确二维不变方向问题，上游2D条款不同|是否识别来源/条件差异并按裁决处理|D01|
|V03|v241工程遇到v261快照属性|是否区分文档快照、实际版本与接口错误|D03、D04|
|V04|controller超时但原生process可能存活|如何判断状态、保存未知、决定是否新启动|D23–D25|
|V05|worker0保存结果但后处理1|如何处理结果及保留历史，是否误重跑solver|D23、D28|
|V06|point trace为(t,1,1,1)，另一数据是真矩阵|是否按轴语义处理而不是统一flatten|D17|
|V07|monitor名存在但某result为dataset成员|是否按实际schema选择读取接口|D16|
|V08|两面available=false但数值字段为0|预算如何表达缺失，避免无证据闭合|D20|
|V09|局部E图归一化已知，历史全场未知|声明范围和下一步数据需求是否清楚|D15、D18、D21|
|V10|只想500nm趋势，上游建议全体积扫描|是否能按裁决定义最小相关操作及资源成本|D09、D10、D27、D28|
|V11|S35/S30都短窗口且stop不同|时间与网格结论如何分开|D11–D14|
|V12|用户要求材料吸收但仅有背景控制域Q|如何界定已有结果和缺失证据|D20、D21|
|V13|上游工具会close_all或改资源/许可变量|是否说明所有权与副作用，不越出项目授权|D24、D26|
|V14|同一已完成分析又被默认验证流程调用|能否复用现有证据、减少重复操作|D28|
|V15|新skill仅调整文字说明或图例|验证强度是否与风险相称|D28、D30|

候选分级：文本/接口schema的离线检查；隔离mock后端；独立新目录小模型原生验证；最后才是经授权的真实项目操作。哪些等级必要由具体裁决决定，不强制每项走全套。

本轮已做的只是包结构检查、编号/链接/来源完整性和ZIP可读性，不是上述行为或任何原生兼容性测试。


---

原文件：`SOURCE_EVIDENCE.md`

# 来源定位表

每条均为已下载固定commit中的文件定位，不代表科学结论已被认可。没有把上游说明当成本轮执行指令。

## E01 / S01
保持项目选定安装版本；文档快照与运行时分开；按任务读取相关资料。
- 文件：`skills/lumerical-fdtd/SKILL.md`，行6–22。
- [固定版本原文](https://github.com/username421421/nanophotonics-codex-skills/blob/394261d9616a409cbda7880d6bd778f52ef8b1f9/skills/lumerical-fdtd/SKILL.md#L6-L22)
- SHA256：`1113565318304C8C20C76DE28D4A4C4E0B0CB43674ACFA68EE13BA04E6FAD76D`

## E02 / S03
该建模模块列出禁止2D、使用quasi-2D的约束；适用边界待判断。
- 文件：`skills/LumericalFDTD-modeling/SKILL.md`，行96–105。
- [固定版本原文](https://github.com/Lex669/LumericalFDTD-skill/blob/f26674b2990c1847445f1da061185b58ecd5012c/skills/LumericalFDTD-modeling/SKILL.md#L96-L105)
- SHA256：`5ACA0269D1FE42DE28B007D6CEE72595E594E9A599C0A12FF17F2D3E4C2E07B3`

## E03 / S02
官方MCP指南包含2D FDTD的z-normal、平面及偏振约定。
- 文件：`src/ansys/lumerical/mcp/contexts/fdtd.py`，行78–94。
- [固定版本原文](https://github.com/ansys/pylumerical-mcp/blob/7ae8d862c30f51dfeb2357ee62ca76e4e0c1035f/src/ansys/lumerical/mcp/contexts/fdtd.py#L78-L94)
- SHA256：`056D679C06CCB19BA19D289A2CFC85731FFCDE68892ABE2A0B93F4313A80E11C`

## E04 / S03
该执行模块定义最多5次修复重试循环。
- 文件：`skills/LumericalFDTD-simulation/SKILL.md`，行82–98。
- [固定版本原文](https://github.com/Lex669/LumericalFDTD-skill/blob/f26674b2990c1847445f1da061185b58ecd5012c/skills/LumericalFDTD-simulation/SKILL.md#L82-L98)
- SHA256：`57C3D31882CF74BE6B647DD98873BC56578867F1411790E5343B37A59AD88F48`

## E05 / S05
该实现有默认max_retries=2的恢复入口和其他自动迭代入口。
- 文件：`lumerical_mcp/lumerical/_loop.py`，行72–88。
- [固定版本原文](https://github.com/davydov-nikita/lumerical-mcp/blob/fc88cc95ad04ca46ae23bea290e0fde1361257e7/lumerical_mcp/lumerical/_loop.py#L72-L88)
- SHA256：`52415EBFD31600FB1BC6B4B82C36208422A3B9FDA14310C2357EF11FB80124CF`

## E06 / S04
该skill列出设置许可环境变量、PATH与CLI fallback的默认做法。
- 文件：`lumerical-fdtd/SKILL.md`，行54–70。
- [固定版本原文](https://github.com/wfy-op/codex-for-comsol-lumerical/blob/375c4dafa24d8f75f45ac5ace92d80eafb7ec596/lumerical-fdtd/SKILL.md#L54-L70)
- SHA256：`DE0516369AE517D769DBA9AADAF125AF9F2F856C2C65CC215F872178C96DCDF0`

## E07 / S06
该skill说明以v261为目标，并包含MPI、逆设计和AALI接口。
- 文件：`skill/lumerical.md`，行173–189。
- [固定版本原文](https://github.com/zxqcreations/Lumerical_MCP_Skill/blob/40ccd5eefe2b065448d150140044610fe46727f7/skill/lumerical.md#L173-L189)
- SHA256：`55E070DAFF6B2C091B972862C4E4FB488901D896CD13885A155F725D4FEA9BA4`

## E08 / S01
结果列表、可直接获取的结果及dataset成员分别说明。
- 文件：`skills/lumerical-fdtd/references/results.md`，行56–72。
- [固定版本原文](https://github.com/username421421/nanophotonics-codex-skills/blob/394261d9616a409cbda7880d6bd778f52ef8b1f9/skills/lumerical-fdtd/references/results.md#L56-L72)
- SHA256：`261A14D17620F71BEB5C1327BB1C43D2F9082923A09A38C11B46780B11137889`

## E09 / S05
该实现按某一数值控制的变化和容差生成certified/uncertified标签。
- 文件：`lumerical_mcp/lumerical/_converge.py`，行154–170。
- [固定版本原文](https://github.com/davydov-nikita/lumerical-mcp/blob/fc88cc95ad04ca46ae23bea290e0fde1361257e7/lumerical_mcp/lumerical/_converge.py#L154-L170)
- SHA256：`D5EA24C81CE300304AA92C451CF9B76F27B3176527046FDC10D7B5D4BCDA3DA6`

## E10 / S02
官方MCP指南涵盖PML、对称、Periodic、Bloch的任务分支。
- 文件：`src/ansys/lumerical/mcp/contexts/fdtd.py`，行889–905。
- [固定版本原文](https://github.com/ansys/pylumerical-mcp/blob/7ae8d862c30f51dfeb2357ee62ca76e4e0c1035f/src/ansys/lumerical/mcp/contexts/fdtd.py#L889-L905)
- SHA256：`056D679C06CCB19BA19D289A2CFC85731FFCDE68892ABE2A0B93F4313A80E11C`

## E11 / S01
该参考说明重叠结构的mesh order及其前置开关。
- 文件：`skills/lumerical-fdtd/references/geometry-materials.md`，行164–180。
- [固定版本原文](https://github.com/username421421/nanophotonics-codex-skills/blob/394261d9616a409cbda7880d6bd778f52ef8b1f9/skills/lumerical-fdtd/references/geometry-materials.md#L164-L180)
- SHA256：`2F6E0546C92D94C63775B751641DA100635E72F0CDDFA615FBFFA4C1E5AD059A`

## E12 / S03
该建模skill列出多边形不支持mesh order的约束。
- 文件：`skills/LumericalFDTD-modeling/SKILL.md`，行94–105。
- [固定版本原文](https://github.com/Lex669/LumericalFDTD-skill/blob/f26674b2990c1847445f1da061185b58ecd5012c/skills/LumericalFDTD-modeling/SKILL.md#L94-L105)
- SHA256：`5ACA0269D1FE42DE28B007D6CEE72595E594E9A599C0A12FF17F2D3E4C2E07B3`

## E13 / S02
官方MCP指南提供网格、conformal、时间、auto-shutoff和发散相关做法。
- 文件：`src/ansys/lumerical/mcp/contexts/fdtd.py`，行1013–1029。
- [固定版本原文](https://github.com/ansys/pylumerical-mcp/blob/7ae8d862c30f51dfeb2357ee62ca76e4e0c1035f/src/ansys/lumerical/mcp/contexts/fdtd.py#L1013-L1029)
- SHA256：`056D679C06CCB19BA19D289A2CFC85731FFCDE68892ABE2A0B93F4313A80E11C`

## E14 / S01
光源种类、位置、偏振、模式及相关API的候选知识。
- 文件：`skills/lumerical-fdtd/references/sources.md`，行1–15。
- [固定版本原文](https://github.com/username421421/nanophotonics-codex-skills/blob/394261d9616a409cbda7880d6bd778f52ef8b1f9/skills/lumerical-fdtd/references/sources.md#L1-L15)
- SHA256：`79BEBC6F25C4C9767192BC65EA86C344078578646B445A9F7BF8952109072329`

## E15 / S01
监视器类型、频率、插值、采样与结果的候选知识。
- 文件：`skills/lumerical-fdtd/references/monitors-results.md`，行1–15。
- [固定版本原文](https://github.com/username421421/nanophotonics-codex-skills/blob/394261d9616a409cbda7880d6bd778f52ef8b1f9/skills/lumerical-fdtd/references/monitors-results.md#L1-L15)
- SHA256：`5698E3319511D6FFAAFC8363615643FD3DE5A1F45070231833FE108B6038F629`

## E16 / S05
仓库描述validate_setup、assess_results及其检查范围；本轮未验证这些检查的科学充分性。
- 文件：`README.md`，行36–52。
- [固定版本原文](https://github.com/davydov-nikita/lumerical-mcp/blob/fc88cc95ad04ca46ae23bea290e0fde1361257e7/README.md#L36-L52)
- SHA256：`45A40ADAD0FCE95D9E8192E3F5EEA4D47FDA4FFD93A02AD8300968A2EB7FBA75`

## E17 / S05
该模块的run入口调用求解器；读取结果和switch_to_layout是不同入口。
- 文件：`lumerical_mcp/lumerical/_runtime.py`，行29–45。
- [固定版本原文](https://github.com/davydov-nikita/lumerical-mcp/blob/fc88cc95ad04ca46ae23bea290e0fde1361257e7/lumerical_mcp/lumerical/_runtime.py#L29-L45)
- SHA256：`9EA2FA88762C10FDF1AAF8E3F5ADAA48CAB7BA1582D67C63348A8977728D7125`

## E18 / S02
官方MCP使用持久会话中的Python片段，而不是独立脚本；该限制有具体工具上下文。
- 文件：`src/ansys/lumerical/mcp/contexts/general.py`，行67–83。
- [固定版本原文](https://github.com/ansys/pylumerical-mcp/blob/7ae8d862c30f51dfeb2357ee62ca76e4e0c1035f/src/ansys/lumerical/mcp/contexts/general.py#L67-L83)
- SHA256：`250ABB0A3531B5FB279C6CABB692CC7F14B9F0D42E27B58ADACC33795F3B2621`

## E19 / S01
按关注指标和单项数值控制组织验证的候选清单。
- 文件：`skills/lumerical-fdtd/references/convergence-checklist.md`，行1–15。
- [固定版本原文](https://github.com/username421421/nanophotonics-codex-skills/blob/394261d9616a409cbda7880d6bd778f52ef8b1f9/skills/lumerical-fdtd/references/convergence-checklist.md#L1-L15)
- SHA256：`31113C81E199FF5B8E6E5AD988066569E443405C537E117939A0E3A38D244B0F`

## E20 / S06
该接口清单同时包含读取、运行、reset、stop及资源修改。
- 文件：`skill/lumerical.md`，行44–60。
- [固定版本原文](https://github.com/zxqcreations/Lumerical_MCP_Skill/blob/40ccd5eefe2b065448d150140044610fe46727f7/skill/lumerical.md#L44-L60)
- SHA256：`55E070DAFF6B2C091B972862C4E4FB488901D896CD13885A155F725D4FEA9BA4`

## E21 / S01
该仓库声明包含不同来源材料，未授予这些材料额外的再分发权利。
- 文件：`NOTICE.md`，行1–15。
- [固定版本原文](https://github.com/username421421/nanophotonics-codex-skills/blob/394261d9616a409cbda7880d6bd778f52ef8b1f9/NOTICE.md#L1-L15)
- SHA256：`0207E8FD271B940391AC49A0E2D9A48C8F8A5C9EB72A49F87432B9BDB1942D1C`

## E22 / S03
该执行skill给出直接getresult取得Ex的示例；对象/版本适用性待判断。
- 文件：`skills/LumericalFDTD-simulation/SKILL.md`，行111–127。
- [固定版本原文](https://github.com/Lex669/LumericalFDTD-skill/blob/f26674b2990c1847445f1da061185b58ecd5012c/skills/LumericalFDTD-simulation/SKILL.md#L111-L127)
- SHA256：`57C3D31882CF74BE6B647DD98873BC56578867F1411790E5343B37A59AD88F48`

## E23 / S03
该建模skill禁止newproject，关联求解器对象被清除的说明。
- 文件：`skills/LumericalFDTD-modeling/SKILL.md`，行87–103。
- [固定版本原文](https://github.com/Lex669/LumericalFDTD-skill/blob/f26674b2990c1847445f1da061185b58ecd5012c/skills/LumericalFDTD-modeling/SKILL.md#L87-L103)
- SHA256：`5ACA0269D1FE42DE28B007D6CEE72595E594E9A599C0A12FF17F2D3E4C2E07B3`

## E24 / S01
该skill讨论switchtolayout对已有结果的影响和按需提取。
- 文件：`skills/lumerical-fdtd/SKILL.md`，行65–81。
- [固定版本原文](https://github.com/username421421/nanophotonics-codex-skills/blob/394261d9616a409cbda7880d6bd778f52ef8b1f9/skills/lumerical-fdtd/SKILL.md#L65-L81)
- SHA256：`1113565318304C8C20C76DE28D4A4C4E0B0CB43674ACFA68EE13BA04E6FAD76D`

## E25 / S03
该执行skill按规模列出5/20/100分钟调用超时。
- 文件：`skills/LumericalFDTD-simulation/SKILL.md`，行74–90。
- [固定版本原文](https://github.com/Lex669/LumericalFDTD-skill/blob/f26674b2990c1847445f1da061185b58ecd5012c/skills/LumericalFDTD-simulation/SKILL.md#L74-L90)
- SHA256：`57C3D31882CF74BE6B647DD98873BC56578867F1411790E5343B37A59AD88F48`

## E26 / S05
该自动流程包含延长时间、降低稳定性因子和网格比较等分支。
- 文件：`lumerical_mcp/lumerical/_loop.py`，行119–135。
- [固定版本原文](https://github.com/davydov-nikita/lumerical-mcp/blob/fc88cc95ad04ca46ae23bea290e0fde1361257e7/lumerical_mcp/lumerical/_loop.py#L119-L135)
- SHA256：`52415EBFD31600FB1BC6B4B82C36208422A3B9FDA14310C2357EF11FB80124CF`

## E27 / S05
该比较实现默认tol=0.02；实际归约和near-zero处理需单独判断。
- 文件：`lumerical_mcp/lumerical/_converge.py`，行53–69。
- [固定版本原文](https://github.com/davydov-nikita/lumerical-mcp/blob/fc88cc95ad04ca46ae23bea290e0fde1361257e7/lumerical_mcp/lumerical/_converge.py#L53-L69)
- SHA256：`D5EA24C81CE300304AA92C451CF9B76F27B3176527046FDC10D7B5D4BCDA3DA6`

## E28 / S06
该README的最低版本说明与skill正文目标版本分别保留，不自动合并成兼容结论。
- 文件：`README.md`，行104–115。
- [固定版本原文](https://github.com/zxqcreations/Lumerical_MCP_Skill/blob/40ccd5eefe2b065448d150140044610fe46727f7/README.md#L104-L115)
- SHA256：`72BB0590F4274C581B546E57BE46B368AA43D9B42E96D170DF9C7E2CFE97FB8D`


---

原文件：`PRO_DECISION_TEMPLATE.md`

# Pro 逐项回复模板

状态：全部待裁决。未替你选择任何方案。

请结合固定版本来源、候选条款和历史证据逐项回答。官方/社区/历史经验的身份不能代替适用条件。
可以采用、改写、限定场景、补证后再定或不纳入，也可以提出未列出的方案。空白保留未决，不视为同意。

技术意见不构成启动/停止仿真、安装、改配置或修改现有作业的用户授权；不恢复人为额度。

## 总体意见

- 拟议skill适用范围：待填写
- 模块组织与复杂度：待填写
- 快速500nm趋势验证与完整科学资格验证的分工：待填写

## 逐项裁决

|编号|议题|裁决|适用前提/版本/例外|建议措辞与证据|
|---|---|---|---|---|
|D01|2D、quasi-2D与3D|待填写|待填写|待填写|
|D02|newproject与求解器对象生命周期|待填写|待填写|待填写|
|D03|mesh order与对象属性|待填写|待填写|待填写|
|D04|属性查询与默认值|待填写|待填写|待填写|
|D05|API、CLI还是MCP|待填写|待填写|待填写|
|D06|Periodic、Bloch、PML与跨边界几何|待填写|待填写|待填写|
|D07|对称边界与缩小计算域|待填写|待填写|待填写|
|D08|材料库、拟合与薄层表达|待填写|待填写|待填写|
|D09|源类型、带宽、偏振与频点|待填写|待填写|待填写|
|D10|真正快速验证的目标和保真边界|待填写|待填写|待填写|
|D11|时间窗口与auto-shutoff|待填写|待填写|待填写|
|D12|S30/S35等网格配对|待填写|待填写|待填写|
|D13|容差、near-zero和certified标签|待填写|待填写|待填写|
|D14|自动加密、延时与停止条件|待填写|待填写|待填写|
|D15|监视器插值、共点图与native Yee数据|待填写|待填写|待填写|
|D16|getresult/getdata及dataset成员|待填写|待填写|待填写|
|D17|维度、shape与序列化|待填写|待填写|待填写|
|D18|CW、sourcepower与原始功率|待填写|待填写|待填写|
|D19|Apodization与频域结果用途|待填写|待填写|待填写|
|D20|缺失功率、复功率与控制域口径|待填写|待填写|待填写|
|D21|材料分解、conformal与混合单元|待填写|待填写|待填写|
|D22|节点身份、记录支持与闭合|待填写|待填写|待填写|
|D23|出错后的重试策略|待填写|待填写|待填写|
|D24|会话、进程所有权与停止接口|待填写|待填写|待填写|
|D25|超时、退出和健康状态|待填写|待填写|待填写|
|D26|环境、许可与MPI/GPU资源设置|待填写|待填写|待填写|
|D27|资源估算与实测|待填写|待填写|待填写|
|D28|工程证据强度与流程负担|待填写|待填写|待填写|
|D29|许可、依赖与实现代码合并|待填写|待填写|待填写|
|D30|Skill边界、测试与发布|待填写|待填写|待填写|

## 每项需要展开时

```text
编号：Dxx
裁决：
建议采用的具体条款：
适用物理前提、软件版本、对象/接口：
例外与不可推广范围：
来源或推理：
还需要的离线/模拟/原生验证及预期行为：
尚未解决的分歧：
```

请勿把上游advertised/certified、本包结构核验或历史报告摘要直接等同于物理正确、收敛、兼容或可部署。
机器可读回复可填写decisions.json的null字段；不需要执行包内或上游任何代码。

