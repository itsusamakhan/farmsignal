# Maintenance and institutional ownership

This is a proposed operating process, not a claim that production governance is implemented.

## Owners

Assign a programme owner, an agricultural content reviewer, local language reviewers, an ML/data maintainer and an operations maintainer. An independent evaluator should assess farmer usefulness and errors. Institutional sponsorship does not substitute for local agronomic review.

## Three update processes

1. **Data synchronization:** run `make data` while connected, inspect the manifest/quality report, then restart the gateway. Forecast expiry must remain enforced. A cached weather response is not guaranteed to stay current.
2. **Rules and language:** qualified reviewers approve the change, citation and applicability; increment the rules version and rerun relevant scenarios. Do not introduce fertilizer or pesticide prescriptions within this scope.
3. **Model releases:** collect consented questions, remove identifiers, label with local reviewers, group related messages into the same split, retrain, and compare against the baseline. Keep the final evaluation set independent of tuning.

## Release procedure

- Run `make test`, `make evaluate` and `make offline` using the proposed release artifacts.
- On macOS, run `sandbox-exec -f scripts/offline.sb .venv/bin/python scripts/verify_offline.py` to prove OS network denial and exercise cached scenarios.
- Review per-language/per-intent errors, abstentions and incorrect accepted predictions; passing software tests does not validate advice.
- Record dependency, model, dataset, rule and template versions, source licenses and checksums.
- Obtain agricultural/language approval, pilot with extension officers, and retain the preceding release for rollback.
- Production deployments should add signed updates, access control, incident reporting, backups, consent/retention controls and confirmed referral delivery. These are future requirements, not current features.

Never let incoming farmer messages automatically retrain the live model. Queue candidate examples for review. Do not treat AI-generated answers as agricultural ground truth.

## Refresh and recovery

The checked-in cache supports an offline demonstration. `make data` can produce different forecasts and source revisions: preserve old manifests when comparing runs. Failed requests appear in the manifest. Do not replace failures with synthetic observations. The cache rebuild writes a temporary database before replacing the previous one; stop/restart the gateway around planned updates. Keep a copy of the prior database and model before release.

## Pilot exit criteria to define before deployment

Agree on minimum per-language intent performance, acceptable incorrect-advice rates, maximum referral failure, operational uptime and farmer comprehension measures. No universal numeric thresholds are asserted here. The current synthetic test set is too small to establish deployment readiness.
