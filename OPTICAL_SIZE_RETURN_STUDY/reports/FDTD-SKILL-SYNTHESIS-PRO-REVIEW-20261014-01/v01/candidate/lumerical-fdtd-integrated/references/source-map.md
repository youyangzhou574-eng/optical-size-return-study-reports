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
