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