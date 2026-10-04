# Contributing

Use Python 3.12 and `make setup`. Run `make test` before submitting changes. For classifier changes, also run `make train` and `make evaluate`; report regressions and baseline comparisons. Data sync requires internet, while `make offline` should not.

Keep changes focused and explain the behavior, evidence and verification in the pull request. Distinguish real observations, mapped estimates, forecasts and synthetic test fixtures. Include citations and unit metadata for any agricultural rule or source. New languages need independent review; do not mark AI translations as reviewed.

Do not commit credentials, phone numbers, actual farmer records, local virtual environments or audit logs. Raw data must have redistribution permission and attribution. Do not load model artifacts from untrusted contributors without review: joblib deserialization can execute code.

Related training examples and translations must stay in one split. Avoid tuning against the held-out test set. A changed model needs an updated model card and honest metrics. Keep the supported crop scope and offline operation explicit.
