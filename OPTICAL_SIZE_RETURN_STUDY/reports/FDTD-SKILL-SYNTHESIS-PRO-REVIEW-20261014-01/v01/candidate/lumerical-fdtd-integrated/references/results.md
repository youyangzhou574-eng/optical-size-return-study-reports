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
