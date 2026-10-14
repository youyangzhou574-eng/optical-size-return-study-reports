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
|描述结构并建模|几何/材料/源/边界/网格/监视器参数契约与建模脚本方案|[modeling](references/modeling.md)|D01–D09|
|做快速趋势验证|目标量、保真边界、成本分项与可比较范围|[modeling](references/modeling.md)|D10–D14|
|读取现有结果|数据轴、坐标、归一化、缺失状态和目标量定义|[results](references/results.md)|D15–D22|
|连接、运行、修复|会话所有权、具体副作用、运行身份与失败分类方案|[execution](references/execution.md)|D23–D28|
|组织可靠性证据|各目标量的适用证据、剩余缺口和候选对照|[validation scenarios](references/validation-scenarios.md)|D11–D14、D20–D22|
|维护或移植skill|版本、来源、许可、实现依赖与模块边界|[decision register](references/decision-register.md)|D29–D30|

## 本轮审阅方式

1. 对照用户真实目标，区分“只问设置”“建模但不求解”“处理已有数据”“启动新例”等请求。不要因为参考包提供了全流程能力就替用户扩大任务。
2. 将上游说法、具体版本、历史观察、候选推广和未决问题分别呈现；[决策表](references/decision-register.md)是未决项的唯一清单。
3. 每个拟采用条款应能追溯到来源或标注为本次综合提议。参考[来源映射](references/source-map.md)与[经验摘要](references/experience.md)。
4. 不替Pro预选方案。收到实际裁决后，在具体版本、对象、前提、例外、证据和措辞层面更新；相互冲突的裁决单独列出，不能静默选一个。
5. 本草案不重新解释现有的用户权限、项目隔离、禁止覆盖历史、暂停轮询或无人工额度要求。技术方案的裁决和实际执行授权是不同事项。

## 拟议工作产物

未来实现可按任务选用[模板](references/templates.md)，不要求每次小改动生成整套工程档案：

- `model_contract`：对象、材料、源、边界、网格、记录方式、目标量与近似。
- `operation_intent`：动作、输入、已有结果可复用性、预期副作用、失败后的事实记录。
- `result_summary`：量的定义、实际时间/频率/坐标、归一化、适用范围和缺失证据。
- `decision_record`：来源、版本、裁决范围、必要验证和实际做过的检查。

这些字段只是候选结构，不是要求引入新的通用launcher/consumer框架。现有能完成任务的项目工具是否复用、哪些代码需要引入，留给D28–D30。

## 不能声称已经完成的事项

没有融合运行上游六套后端；没有完成其v241/v252/v261兼容测试；没有完成科学裁决或独立行为测试；没有建立新的材料权重接口；没有新的轻量模型或仿真结果。本轮交付的是可追溯、可裁决的综合设计草案。
