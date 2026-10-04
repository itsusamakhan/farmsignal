# Measured evaluation

Measured on 2026-10-04. These are prototype results, not evidence of field readiness.

| Language (20 held-out examples each) | Keyword macro-F1 | Raw classifier macro-F1 | Classifier with abstention macro-F1 |
|---|---:|---:|---:|
| en | 0.628 | 0.597 | 0.306 |
| ur | 0.848 | 0.889 | 0.686 |

The learned model underperforms the keyword baseline in English. The conservative gate increases abstention substantially and reduces macro-F1. This is a negative result worth retaining: do not present the model as production-ready. No tuning used the held-out test errors. A compact multilingual model may be a later comparison, after collecting independently labelled real questions; adding complexity cannot repair an unrepresentative evaluation set.

- en: abstention 70%; incorrect accepted classifications 2/20. Accepted means the model exceeded the chosen threshold and passed the keyword gate; it does not mean its probability was calibrated.
- ur: abstention 45%; incorrect accepted classifications 1/20. Accepted means the model exceeded the chosen threshold and passed the keyword gate; it does not mean its probability was calibrated.

All per-class precision, recall, F1, support and misclassified examples are retained in `evaluation.json`. Five intent classes: planting, soil, weather, officer, unknown. Source: 140 AI-authored examples grouped by bilingual family (80/20/40 train/validation/test). Same-author bias and small sample size limit generalization.

## Timing and footprint

Hardware: macOS-26.2-arm64-arm-64bit arm64. Python 3.12.5 (v3.12.5:ff3bc82f7c9, Aug  7 2024, 05:32:06) [Clang 13.0.0 (clang-1300.0.29.30)]. Model 69,600 bytes (68.0 KiB).

- Warm service latency: p50 20.3 ms; p95 55.9 ms, 100 sequential runs, logging disabled.
- Cold process through first reply: p50 1788.9 ms; p95 6548.0 ms, only 5 runs. Startup variation is large and the p95 estimate is unstable.
- Peak evaluation-process memory: 139.2 MiB. Includes evaluation libraries. See `inference-memory.json` for a separate fresh inference process.
- See `api-latency.json` for measured localhost HTTP latency including serialization and audit logging.

## Offline and behavioral verification

The test suite checks source units, absent soil, wide/reversed uncertainty, unknown messages, unsupported crop, missing/outside location, observation-dependent replies, stale/future/current forecast windows, referral failure, split integrity and API validation. The macOS OS sandbox denied an explicit network connection and then completed the cached demo. See `tests.txt` and `os-offline.txt`.

No farmer trial, independently reviewed translation, modem delivery or field suitability accuracy has been measured.
