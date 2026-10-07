# OPT-SIZE-A2-PROGRESS-20260930-01 v42

## 目标与当前裁定请求

目标仍是十一月上旬开题所需的两尺寸结构光吸收效率比较。用户已明确批准 v41 首选整包，并直接要求“行吧，把现在这个模型先停了，开始新方案吧”。本轮已实际停止旧大例，并把 v41 做成实际 LSF 和未求解 FSP，完成三次有界 CAD 操作。不是再次请求同一人类启动许可，也不重开 Flat v25。

目前新 MPI 为 0。需要裁定的是新的实质材料归属问题，以及剩余原生执行资源证据，而不是时域监视器的小接口错误。既有科学门和资源 STOP 全部保留。

## 已执行与原始限制

旧 `P30_X_FINE_500NM_DIRECT_USER_20261002_01`：精确 PID、原生创建时间、名称和输入路径绑定后，仅发送一次针对 engine48968 的停止信号。MPI55928、runner36420随后自行退出。真实退出为 engine -1、MPI -3、runner1，task Ready/1；精确旧输入引擎数0。记为 USER_CANCELLED_NOT_NUMERICAL_COMPLETION，不称成功，不退账，不覆盖原文件或历史回执。

第一次停止控制器在本机错误地重复构造凭据，尚未创建远端会话；错误保留，沿既有凭据初始化方式修复后才发生唯一实际服务器停止。没有输出或公开凭据。

新首选仍是 P15/P30完整原周期，S35 35/35/25 nm柱bbox、平膜仅Z12.5 nm、halo35 nm，柱高9 μm、PDMS基底10 μm、ITO100 nm、Fe25 nm，原X源350–800 nm、BC/PML/M0/A2冻结；2900 fs、auto1e-8，计划4MPI×1thread。不得小单胞、Fe加厚、改PML或启动基准例。

本地六项聚焦测试通过：两尺寸几何、完整材料覆盖、C/U/D/W闭合分区、共享面去重、实际LSF记录范围、未知门阻断。P15候选20个局部E区/124个500nm功率面，P30候选16个局部E区/126个功率面；每例原四面十点功率、六个E-only点时序、一处小运行期index见证。不是全胞十点三维材料场，也不是代表柱倍乘。

## 实际 Native 结果

P30组合输入已在v241 CAD中生成，未求解 FSP895270 bytes，SHA256 `38AA2A1AD7DDB15D1E7CD5A3A5FF21BD3733C5065185124891368FBF30481BA7`。全采集方案的CPU报告：

| 项目 | GiB |
|---|---:|
| Running Simulation | 29.703251608647406 |
| Data Collection | 5.921217545866966 |
| FSP Saved Monitor Data | 2.230953 |
| Internal EM fields/index | 26.6456028977409 |

精确bytes见phase_memory.csv；最后一项不是额外监视器。以上为native预估，不是实测峰值。Conformal内存可靠性warning原样保留。最后CAD前服务器空闲110.1248245 GiB，单例admission仍57.6 GiB；不是周期RAM监控，也不能把这份快照当后继启动时的free。

共享资源配置实际读回28 processes、1 thread，不是拟启动4MPI的独立开销证明。未更改共享resource manager。native报告没有列出 COMBO_E_PILLAR_011 的单项内存，但同份FSP重开确认16个E对象全部存在、唯一且enabled，Ex/Ey/Ez开启、H关闭；不能把缺一行当对象缺失，也不能用已列监视器求和当总峰值。

第一次CAD真实exit0但XML errors1，原因是点时域monitor的`down sample time`为不可直接赋值的派生属性。只修接口：通过min sampling per cycle要求每个dt采样，并读取实际downsample；第二次CAD exit0、stderr0、完整marker，XML不存在/errors null。六个实际downsample均1。这个小错误自行修正留档，未单独请示。

第三次CAD仅重开该未求解FSP、检查16个E设置及一个小3D顶帽index_detail，845空间点，上限4096，无run/save/物理改动，exit0/stderr0/完整marker，XML不存在/errors null。grid/dt前后完全相同。文件逐个传输bytes/SHA核定。

halo35后X/Y三分量共六项原生Yee周期配对全部有实际坐标配对、无插值，maxRelative均0，原1e-6通过；以前halo30的X/index_x 6.79%失败历史不改。这里只证明这些native小见证，不冒称完整全胞动态周期验收。

## 顶帽问题已细化，不能再用“没有纯Fe”概括

原2D顶帽probe在9.1125μm名义位置吸附到了9.125μm附近，未覆盖全部Yee分量层。本次3D小块跨9.075–9.175μm，保存三分量的实际offset和全部复index。

- index_z在9.112500000000011μm有169/169纯Fe匹配点，证明先前“顶帽没纯Fe点”不能当消失证据。
- index_x/index_y在9.10000000000001和9.125000000000012μm各有169个不与任一纯材料fit匹配的节点，共676个混合/未归属节点。
- 邻近层有纯ITO和水点，所有复数与坐标见可读JSON/CSV。没有用field fitting反求epsilon，没有将最接近材料填为Fe。

当前薄Fe材料资格未放行。小块还不能证明全部斜侧壁分配正确。所有控制面native snapping、最终输入绑定、逐块CAD-only index_detail，以及4MPI全阶段附加缓冲/导出/Python峰值证据仍需完成。500nm混合账不冒充全域四材料独立体积分，FULL_VOLUME_CLOSURE_NOT_MEASURED保持。

## 请一次给出有界执行裁定

1. 依据实际小块raw和原生offset，是否可采用“由几何与分量dual-cell确定的二材料贡献权重、再与native复epsilon独立核对”的有界规则来处理顶帽切向混合节点？请明确它是否满足你v41所要求的既有经验证分配规则，或给出一项具体必要验证，不能只重复泛泛监视器建议。未验证前不积分成合格Fe，不允许field fitting、nearest material、残差回填；三材料或规则不适用一律UNASSIGNED/STOP。
2. 若该规则不能成立，请在原获准S35/S30网格对内给出唯一有限处理路线：可否先做尚未启动P30的S30 CAD薄层表示检查来判可实现性（0MPI），以及首个S35科学启动仍应停在哪个门。不要隐含把S30改为主算或耗费额外DIAGNOSTIC；物理/主矩阵实质改变须明确报用户。
3. 对native资源配置28/1与实际4/1，允许执行端怎样在不改共享manager/账户/策略的前提下取得有界4MPI资源上界？是否接受独立case资源配置、完整附加缓冲预算与即刻启动门。不得用29.7GiB单项当全阶段PASS，也不启动“资源测试solve”。请将坐标/块index/薄层/资源/P15先行的后继范围合并，避免每个实现小步骤请示。

## 用户要求的更多工程预算

用户此前明确要求下一次正常报告同时申请更多工作预算，本报告是正常新native实质结果报告，不单独追加预算消息。申请新增12h本地准备/分析、32项聚焦检查、6次有界CAD，分别用于混合Yee归属测试、native坐标和分块index输入绑定、case资源上界与P15/P30 build/reopen、实际结果验收准备。累计CAD墙钟7200s不增加，科学次数、2900fs/auto、资源与安全门不扩大。

当前工程账：检查161/161；CAD12/24、累计121.2712661s/7200s；本地36h上限、实际旧账持续扣除不重置。32项将累计检查上限变193，6次将CAD上限变30。本地上限48h，仅含工程工作，不是solver48h上限。

科学账仍MAIN2/6、DIAGNOSTIC4/4、RECOVERY0/2、TOTAL6/12。旧例取消不退账；余四MAIN仍仅两组合主算及条件性两S30确认，无新solve启动、无benchmark、无移类。获批前不得超过当前工程或科学预算。

Pro本轮既有实际3/50，当前报告如实际发送将第4次；读取不计次。执行端会绑定后继回复检查，记录已送达/生成中/错误/完整待消费/已消费，不因旧cache重发；新科学裁定不扩大人类与安全权限。

## 交付及证据边界

仅公开本项目白名单可读文件，原nativeFSP与服务器私有日志留本地，不公开凭据、许可路由、账户信息或别的项目。所有工程错误原记录保留。发布和发送不是Pro实际已读或科学验收。未创建任何额外网页对话，未切模型，无Git工作区写入。
