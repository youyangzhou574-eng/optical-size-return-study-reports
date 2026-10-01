# Optical Size Return Study Reports

Public report-delivery repository for **OPTICAL_SIZE_RETURN_STUDY** only.

This repository is independent of circuit and other materials projects. It is
not a simulation runner, production-input repository, or authorization to run
additional simulations.

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

## Scientific Status

The existing D2 diagnostic review is complete and accepted as localization
evidence only. Overall scientific qualification remains **NOT_QUALIFIED**;
root cause is **NARROWED_BUT_NOT_UNIQUE**; paired numerical convergence remains
**NOT_YET_TESTED**. No new solve is authorized by creating this repository.

No historical report or raw research attachment is republished by this initial
repository setup. Future packages require the usual project-specific scope and
pre-publication review.
