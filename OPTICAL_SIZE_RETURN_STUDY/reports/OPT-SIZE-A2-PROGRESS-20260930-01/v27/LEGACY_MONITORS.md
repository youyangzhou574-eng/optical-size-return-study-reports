# 旧三维监视器只读对照

本轮按用户要求仅检查本地旧脚本、导出代码和已有CSV。不访问服务器，不打开FSP，不运行CAD/求解，不改旧模型，不向Pro提交。构建脚本设置不是重新核实的native FSP属性。

## 搜索范围与结果

排除GitHub/GPT/paper打包副本后，在旧pillar trap、1.5/5 conformal pillar、1.5/5 hole和size/depth sweep四组目录中核对30个build脚本。28个柱/孔脚本明确指定局部mesh为dx=dy20nm、dz15nm；另外2个Flat脚本只显式细化薄膜区dz5nm，横向网格不能从前述变量推断。所有30个脚本都定义metrics_lambda=500nm，显式诊断frequency points值均为1。这里只针对这些脚本明确设置的诊断监视器；R/T或index继承默认频率另列，不能推断所有监视器均为1点。

代表性设置：

| 旧模型 | 三维体场范围 | 显式体场频率 |
|---|---|---|
| 1.5um侧长/5um高柱 |14个柱体局部包围盒，含外壳及XY80nm余量 |500nm单点 |
| 1.5um侧长/9um高indexaudit及1/3/5/7/11/13um系列 |14个柱体包围盒E及index，加0-125nm的薄膜flat-stack volume |500nm单点E，index频点没有逐对象显式设置 |
| 1.5/2/2.5um侧长、3/5/7um深孔 |逐孔局部体场及平面诊断 |500nm单点 |
| Flat indexaudit |覆盖薄膜stack，而非整块10um PDMS |500nm单点E |
| 已核旧directRT91包（独立比较，不在30项计数中） |删除flat-stack及14柱的重型E/index |保留91点R/T/P面输出 |

在这30个build脚本内未发现显式down sample/spatial interpolation设置，也未发现主动关闭H/P输出。不能将“脚本没写”冒充保存FSP实际downsample=1或interpolation=none。旧1.5/9导出代码先得到Ex/Ey/Ez然后构造E2，并在柱体部分读取Hx/Hy计算Pz；这与当前要求保留各分量原生Yee数据的积分方法并不等价。已有indexmask计算代码明确TARGET_WAVELENGTH_NM=500，进一步确认旧组件分析为单波长诊断。

旧包围盒也并非稀疏Fe壳层：它同时包含PDMS核心和部分water，彼此可能重叠或跨周期。缩小采样域、去重、材料归属、Yee halo和切边计权仍须证明，不能直接复制旧box定义宣称通过新科学门。

## 必要性

1. 仅R/T、控制体总净吸收：面通量即可，不需巨型3D E/index。
2. Fe/ITO分别吸收及当前J_Fe^X：需材料分辨的三维场/损耗或已证明并获许可的等价方法；单波长500nm诊断不能当91点全光谱。
3. 场图/能流机理展示：局部2D切片或少数波长局部3D即可；不能让它们把所有生产case变成全高度全频点场存储。
4. E-loss积分只需要E及同位置实际epsilon；H/P额外输出只有独立能流诊断有用途，不能因为旧默认就全保留。

全控制体×91频点巨大数组是v26的拒绝候选/保守估算，不是Pro强制指定的监测实现，也不能由此推论所有四case实现均不可能。Pro07允许比较局部shell、material-loss或数学等价路线；当前监视器可行性仍未通过，不启动。

官方说明支持缩小3D域、仅记录所需场分量；矩形区域的总吸收可用更省资源的面监视器，非矩形多材料分解则需要空间/材料过滤。当前任务不得自行删91点组件输出、改材料损耗或放宽closure来节省RAM。

- https://optics.ansys.com/hc/en-us/articles/360034915673-Calculating-absorbed-optical-power-Simple-method
- https://optics.ansys.com/hc/en-us/articles/360034395254-Calculating-absorbed-optical-power-Higher-accuracy-method-with-multiple-materials
- https://optics.ansys.com/hc/en-us/articles/360034902393-Frequency-domain-monitor-Simulation-object

主证据：static_builder_inventory.json逐文件路径/SHA/显式设置；旧1.5/9 build_indexaudit_1p5_9.lsf第350-428行；对应export_indexaudit_1p5_9.lsf；calculate_indexmask_1p5_9.py第18/142行。所有本轮结论均重新读本地证据，而非把历史笔记当当前native验收。
