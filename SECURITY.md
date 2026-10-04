# Security and deployment scope

FarmSignal is a localhost research prototype. Do not expose the API publicly without authentication, authorization, rate limiting and an operational security review. SMS, real farmer registration and external referrals are not implemented.

Model files use joblib and must come from a trusted source. Dataset checksums detect accidental changes; they are not digital signatures or proof that a source is trustworthy.

Do not put credentials, phone numbers or private farmer data into GitHub issues. Report suspected vulnerabilities privately to the repository owner using an agreed private channel. If GitHub private vulnerability reporting is enabled later, use it. No dedicated reporting mailbox is configured by this prototype.
