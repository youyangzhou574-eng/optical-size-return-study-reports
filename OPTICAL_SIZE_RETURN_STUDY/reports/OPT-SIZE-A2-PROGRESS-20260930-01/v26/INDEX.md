# v26 文件索引

- [REPORT.md](REPORT.md)：完整放行前网格、资源、时限、顺序、STOP与用户预算要求。
- [mesh_memory_time_cases.csv](mesh_memory_time_cases.csv)：四case逐项完整精度核算。
- [forecast_summary.json](forecast_summary.json)：假设、来源SHA、历史校准与四case结果。
- [resource_forecast.py](resource_forecast.py)、[test_resource_forecast.py](test_resource_forecast.py)：标量核算及15测试，不是runner或CAD脚本。
- [test_history.json](test_history.json)：RED、名义CFL/native区分及最终验证回执。
- [scope_and_release.json](scope_and_release.json)：授权/预算门与明确未启动状态。
- [manifest.json](manifest.json)：白名单文件大小与SHA。

所有资源数是offline forecast，不是CAD实测。仅v26新文件，不重新上传旧raw、结果FSP、日志或其他项目数据。

本地计算器 `main` 使用受保护的两份原几何审计和一份历史日志做SHA检查；本报告不重复上传这些旧证据。公共代码可以直接运行 `python -m unittest test_resource_forecast -v`，15测试无需CAD或数据。完整标量输入、维度、公式及结果在REPORT/CSV/JSON中可读复算；它不是可以直接运行的FDTD模型。
