# Technical explainer — 60 seconds

Target: approximately 120 spoken words, with brief pauses. Rehearse once and adjust pacing. This script describes the current implementation, not planned capabilities.

| Time | Visual | Narration |
|---|---|---|
| 00–08 | FarmSignal title and the running interface | FarmSignal is an offline agricultural-assistance prototype that helps farmers identify what to check before growing maize. |
| 08–20 | Highlight message → TF-IDF → classifier in docs/ARCHITECTURE.md | A small classifier uses character and word TF-IDF features with logistic regression to identify planting, soil, weather, or human-help questions. Unclear requests trigger clarification. |
| 20–34 | Highlight registered farm → local cache → rules; briefly show the evidence panel | The backend retrieves the registered farm and cached SoilGrids, NASA POWER and ECMWF data. Cited rules check soil limitations, missing evidence and forecast validity. |
| 34–44 | Show an English reply, then an Urdu reply | Templates return one next step in English or Urdu. Inference runs locally, and we verified it with network access blocked. |
| 44–53 | On screen: “English model trails keyword baseline · 40 synthetic test examples” | The model remains experimental: English results trail our keyword baseline, and the test set is small and synthetic. |
| 53–60 | On screen: “Next: expert review + real questions + supervised pilot” | Real SMS delivery and expert-reviewed field validation are the next steps. |

## Copy-ready narration

FarmSignal is an offline agricultural-assistance prototype that helps farmers identify what to check before growing maize.

A small classifier uses character and word TF-IDF features with logistic regression to identify planting, soil, weather, or human-help questions. Unclear requests trigger clarification.

The backend retrieves the registered farm and cached SoilGrids, NASA POWER and ECMWF data. Cited rules check soil limitations, missing evidence and forecast validity.

Templates return one next step in English or Urdu. Inference runs locally, and we verified it with network access blocked.

The model remains experimental: English results trail our keyword baseline, and the test set is small and synthetic.

Real SMS delivery and expert-reviewed field validation are the next steps.

## Accuracy notes

- The fifth model class is unknown; the narration describes it as unclear requests.
- This is an intent classifier, not a crop-success predictor or a fine-tuned LLM.
- Urdu demonstrates multilingual handling; it is not claimed as the Kenyan pilot's primary language.
- “Verified offline” refers to reports/os-offline.txt, not a claim that a network-status icon proves isolation.
- Use the recorded evaluation figures without rounding them into an “accuracy percentage.”
