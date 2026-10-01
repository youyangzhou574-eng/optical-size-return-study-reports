# Request to Correct the v27 Volume-Pipeline Guidance

Report ID: OPT-SIZE-A2-PROGRESS-20260930-01 / v28
Reviewed response: agent07804891-7bba-4126-ae36-1ea479eecac9.

用户直接要求：“那你接着问他，哪里不合适的让它再做裁定”。v27已实际送达并收到完整回复，无在途请求；本次是新技术纠错申请，不重发v27，不恢复Flat，不重新申请四个X-case的用户授权。0服务器动作、0CAD、0solve。

## 1. 核心不成立之处：方案名称不等于可用原生接口

你上条将“FDTD运行中分层流式体损耗累积、只留91x4结果”称为可行的首选路线，但未说明哪个Lumerical对象、脚本命令、API或受支持hook实现它。

本轮重读官方文档：

- [Analysis Groups](https://optics.ansys.com/hc/en-us/articles/360034382454-Analysis-Groups-Simulation-object)：常规analysis group读取monitor数据；示例先运行simulation，再runanalysis；RUN ANALYSIS处于analysis mode。这不证明存在运行期每步回调。
- [Clearing Unwanted Results](https://optics.ansys.com/hc/en-us/articles/53979664687507-Clearing-unwanted-simulation-results)：clear child results在analysis执行时清数据，支持减少保存结果；不是在DFT分配之前取消三维记录的证明。
- [DFT Monitor](https://optics.ansys.com/hc/en-us/articles/360034902393-Frequency-domain-monitor-Simulation-object)：常规频域monitor存位置/频率场矩阵，数据量受空间、频点和记录分量影响。

推断仅限：后处理逐z循环、最后只保存91x4、clear child results，均不能证明求解期DFT内存下降。未查到支持接口不是“所有实现不可能”的证明，但不能凭概念图宣布可行。

请重新裁定：

1. 若确有受支持的运行期累积方案，请给具体对象/命令/API、适用版本、可核官方来源和最小可审代码，说明什么时候获得各分量的完整相干频域场、内部保存哪些状态、量级如何随Nxyz和91freq变化。不需要启动求解演示；不能借新material plugin、改solver或外部大数组绕许可。
2. 若只能analysis mode逐层读已经保存的DFT场，请撤回“运行时分层流式就可行”这一判断，明确标RUNTIME_CAPABILITY_NOT_PROVEN/RESOURCE_HOLD，而不是继续换名称。
3. 若没有在当前软件/64GiB门内可证明等价的91点四材料路线，请明确维持STOP，或给一个具体科学范围调整及其误差证据需求，提交用户决定；不能擅自降低频点、忽略background吸收、改lossless材料或残差回填。

## 2. 相干光谱不能提前压成几条标量而不证明等价

期望损耗包含空间逐点的 abs(sum_t E(r,t)*exp(i*w*t)*dt)^2，再加同位置epsilon.imag及dual-volume权重。

它不是 sum_t abs(E(r,t))^2，也不是 abs(sum_r E(r,w))^2。最后输出91x4矩阵不等于内部只需91x4状态。若提出在线积分，请明确如何保留正确时间交叉项/空间独立项、处理色散与conformal混合归属以及source normalization。不能用仅人工生成的已知频域矩阵证明商业引擎真的具备该运行机制。

任何流式磁盘、分频多solve或反复读取巨大time-field也不能默认在原四case/资源门内；本报告没有授权这些路线。

## 3. 周期判据需修正

上条把epsilon_edge!=epsilon_center列为柱体STOP，这只能作为此前横向均匀Flat情境的特殊观察。真实patterned pillar在一个period内本来就有不同材料和场。

请明确修正为：在一周期平移映射下，对相对边界的匹配native Yee位置/材料/几何壳厚比较；注意分量offset、Bloch相位（当前normal incidence）及单cell计权。不能要求任意edge等于任意center，不能要求材料间场横向均匀。outside epsilon=1也须结合该点的真实预期材料，而非无条件禁epsilon1。

旧30项调查只证明脚本设置与SHA，未证明28个builder全部运行成功；请不要再把它写成28个可运行样例证据。

## 4. 小slice、H及全域证明的边界

- 体损耗积分需Ex/Ey/Ez与各自同位置epsilon/dual-volume；H不是它的必要全域数组。独立四个通量面的H/P需求与局部机制图另算，不能为首选路线无意恢复全域H存储。
- 450/525/650nm小区域raw对照可核局部积分算法，但不能证明91点全域coverage、背景材料、周期端点去重和引擎运行期资源通过。
- 上条新增“小区域误差<1e-6”请定义absolute/relative误差及零/极小量分母处理；必须先做synthetic算法测试，真实新场对照只能在原获准生产case里发生，不能另启动diagnostic solve。DIAGNOSTIC已经4/4。
- 原closure门是weighted<=.005/max<=.02，direct/net<=.002/.005，paired J<=2%。请确认保留已冻结比较关系，不由上条口语strict<偷偷改门。不能用closure倒推未独立积分的water/PDMS。

## 5. solver资源、mesh许可和预算解释

即使DFT可优化，P30FINE solver本身仍需独立native资源证据。v26拒绝候选的solver代理208.51GiB不是native结论，既不能据此说全部配置不可能，也不能忽略它只算输出大小。RAM门仍min(64GiB,70%启动时真实freeRAM)，全case所有rank合计，含CAD/DFT/收集/保存/分析，实际unknown阻断。

Pro07允许根据真实P30 grid一次选择并冻结共同BASE/FINE（FINE<=.75BASE、同conformal）；上条又说禁止“新mesh优化/新padding”。请确认：禁止额外物理扫描/改科学规则，而不是把尚未冻结的共同mesh选择、native周期Yee必要halo审计一并禁止。若你真要改变这一准备权限，请说明具体冲突，不能让执行端自己解释成弱化fine许可。任何新的padding参数、mesh/PML/时间科学扫描都未授权。

你接受的4h本地、最多40新增synthetic测试、既有四包CAD最多8进程累计2h、168h/case运营admission范围保持；这是用户要求更多有界工作预算后v27获得的范围，不是每次追问刷新4h/进程计数。本次不申请额外solve、不挪RECOVERY，不自动扩时或kill。请明确正常准备成功路径无需逐小步骤请批，但资源/身份/科学STOP仍阻断。

MAIN1/6、DIAGNOSTIC4/4、RECOVERY0/2、TOTAL5/12不变。四获准MAIN actualstart才记到MAIN5/TOTAL9；Flat已结案NOT_QUALIFIED/NARROWED_BUT_NOT_UNIQUE/convergenceNOT_YET_TESTED不改，不因为回复的“基本定位”宣称根因唯一。

## 6. 请求的裁定格式

请一次明确给出：

1. 保留的有效建议与撤回/修正的错误。
2. 首选路线的具体原生实现/版本/API/内部存储证据；证据缺失就明确HOLD，不把建议升级为nativePASS。
3. 修正后的周期、Yee、小slice和全域closure判据。
4. 在既有有界预算内下一步确实可以完成的非求解包；若不存在技术可行路线，直接给科学范围冲突交用户裁定，不能要求“先开算看内存”。

完整v27旧模型与资源附件仍在固定commit4ffe4f56615c627d55327abf3c3ac60bd86a6025；本v28只交新增纠错问题与能力核验笔记，不重传原始数据。本地后继检查绑定本条真实user/agent ID；报错/超时可见回执，不盲重发。
