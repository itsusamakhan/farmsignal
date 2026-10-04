# Demo readiness fixes

The application now handles explicit dry-soil negation, explains explicit unsupported crop requests before generic intent fallback, rejects missing/non-finite/negative forecast measurements, checks forecast chronology, and declines a tomorrow request when its cached forecast does not cover that day. Day-level forecast coverage currently uses UTC conservatively; farm-local date interpretation remains future work. Urdu “کل” can mean yesterday or tomorrow; this limited parser treats it as a future request and should be replaced with clarification in a broader language system.

Refusal responses include an uncertainty explanation. `intent_abstained` and `advice_status` distinguish question routing from evidence limitations. pH template wording no longer implies that every uncertainty interval proves acidic soil. The UI adds a reset button and readable soil/weather evidence while retaining the full JSON record.

Regression suite: 37 passing cases at this revision. No model weights, synthetic dataset or held-out classifier metrics were changed. The routing and evidence fixes do not establish improved classifier accuracy.

Still requires external work: local agronomist and native-language review, real farmer questions, independent model evaluation, a real SMS/modem integration, supervised farmer trials, cost and outcome measurement. None of these is silently claimed as fixed.

Video scripts: [technical explainer](video-kit/TECHNICAL_EXPLAINER.md), [one-minute demo](video-kit/DEMO_VIDEO.md), [recording guide](video-kit/RECORDING_GUIDE.md).

Final visual inspection also revealed zero-filled soil cells without nodata metadata. Preprocessing now excludes cells where both surface mean pH and bulk density are zero, treating them conservatively as suspect fill across aligned layers. Raw files are unchanged. The original demonstration registration remains unchanged and now correctly receives a missing-soil response. Earlier reports claiming all 7,200 cells were valid were incorrect; see the regenerated quality report. This is a data-quality exclusion, not a maize threshold.

Pre-submission update: the fictional demo registration moved about 250 m to the nearest valid soil cell (1.0207° N, 34.9980° E) so the main question shows real mapped evidence. The pH reply now states the mapped value, its 90% range and the FAO EcoCrop reference range. The forecast reply states cached rain and temperature. Explicit non-maize crops (for example peanuts) receive the maize-only reply. Urdu wording remains unreviewed.
