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
