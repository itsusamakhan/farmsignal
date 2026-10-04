# Intent model card

Version 0.1.0. Character 2–5 gram and word 1–2 gram TF-IDF, logistic regression C=4, seed 42. scikit-learn version is pinned in requirements.txt. Compressed joblib model: 69,600 bytes.

Training: 80 AI-authored English/Urdu questions. Validation: 20. Test: 40. Bilingual semantic families stay within one split. Urdu is AI-translated, not human-reviewed. No actual farmer records or Digital Green answers are included. Training features are fit only on the training set.

Validation chooses the confidence gate from 0.30–0.60 in 0.05 steps, preferring the higher threshold on tied macro-F1. Selected threshold: 0.4. A separate recognizable-keyword gate rejects unsupported requests at runtime. Probabilities are uncalibrated; no agronomic confidence derives from them.

The model predicts planting, soil, weather, officer, unknown. It does not predict maize success, weather or disease. The application retains it as a research experiment. English performance is weak and the simple baseline is stronger on this small English test set. Full metrics and failure examples: ../reports/evaluation.json. Do not use the headline Urdu score as evidence of broad Urdu understanding.

Known limitations: script-based language routing can confuse Arabic-script languages; mixed intents, uncommon crops, Roman Urdu, unfamiliar paraphrases and negation are not robust. Swahili is disabled. The application uses predefined source-linked templates and abstention, not generated agronomic answers. Requires independent real-world labels and local expert review before deployment.

Reproduce with `make train` and `make evaluate`. Only load trusted model files. MIT for the AI-authored prototype code/examples; third-party data licenses are separate.
