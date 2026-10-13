# Optical Size Return Study Reports

Public report-delivery repository for **OPTICAL_SIZE_RETURN_STUDY** only.

## 当前执行入口 / Current task — 2026-10-13

**优先完成3 μm三角阵列开题光学验证；1.5 μm退出当前计算主线。**

- [完整任务：CURRENT_TASK.md](CURRENT_TASK.md)
- [执行与回执：Issue #1](https://github.com/youyangzhou574-eng/optical-size-return-study-reports/issues/1)
- [本次任务首次固定提交](https://github.com/youyangzhou574-eng/optical-size-return-study-reports/blob/d2acdaba7de54d0b7f34eb57187f80e5da8ef41e/CURRENT_TASK.md)

明确排程：精确停止仍在time stepping的两个P15长例及P30 S30长例；保留已有P30 S35长参考；补P30本身500 nm三截面场图，网格确认后置。已结束或正在collect/save的结果按任务中的保护分支处理，不盲停、不重跑。

**GitHub发布任务不等于服务器已经执行。桌面端必须在Issue #1填写实际逐run动作回执。**本仓库不直接触发求解或停止工作流。旧报告里的next_operation及历史额度不覆盖当前人类目标；不设置人为求解/CAD/检查/工时额度，科学限制与真实资源风险仍逐项如实记录。

This repository is independent of circuit and other materials projects. It is
not a simulation runner or production-input repository. Task documents record
user-directed work and technical decisions; merely creating or reading a file
does not prove that any server action has occurred.

## Report Layout

Future complete review packages belong under:

```text
OPTICAL_SIZE_RETURN_STUDY/reports/<report-id>/vNN/
  REPORT.md
  INDEX.md
  manifest.json
  attachments/
```

[Delivery rules](OPTICAL_SIZE_RETURN_STUDY/reports/README.md)

## Delivery Rules

- Publish complete reports as Markdown or TXT, with readable CSV/PNG exports.
- Send the paired decision conversation a short summary, file list, repository
  location, and links pinned to the exact commit. Do not split long report text
  into multiple conversation messages.
- Divide large attachments into meaningful files with an index, stable headers,
  row ranges, units, dataset identities, and reconstruction instructions.
- Retain original evidence locally. Manifests connect published files to source
  evidence with SHA-256 hashes and explicitly describe any redactions or
  transformations. A transformed export has its own hash; it must not be
  presented as byte-identical to the original.
- Do not use ZIP, native simulation binaries, or Git LFS pointers as the only
  review evidence.
- Exclude passwords, tokens, private keys, credentials, unrelated personal
  material, and files from other projects before publication.
- Reader access checks are useful but are not a required approval gate.
  Successful upload is not proof that the decision agent actually read a file.
- Do not resend material already received or reopen completed scientific work
  merely because the delivery method changes.

## Historical repository-initialization status

The following paragraph is preserved as the repository-initialization record,
not as the current execution queue or a replacement for case-specific status:

> The existing D2 diagnostic review is complete and accepted as localization
> evidence only. Overall scientific qualification remains **NOT_QUALIFIED**;
> root cause is **NARROWED_BUT_NOT_UNIQUE**; paired numerical convergence remains
> **NOT_YET_TESTED**. No new solve is authorized by creating this repository.

Current work, evidence dependencies and result limitations are in
[CURRENT_TASK.md](CURRENT_TASK.md) and its linked immutable reports. Historical
reports and original research evidence remain unchanged.
