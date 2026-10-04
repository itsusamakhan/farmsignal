# Verification record

2026-10-04, macOS ARM64, Python 3.12.

1. Inspected supplied pitch and brief. Distinguished proposed capabilities from implemented behavior.
2. Checked official source documentation, source licenses, units, forecast dates and the language dataset card.
3. Downloaded 72 regional SoilGrids rasters and 1,096 daily POWER records. The extract contains 7,200 raw soil values, including suspect zero-filled cells identified and excluded in the later demo-readiness review. Weather has no missing days. Added two ECMWF GRIB messages through bounded byte ranges.
4. Initial import failed on a SQL placeholder-count mismatch. Fixed and rebuilt atomically.
5. Grid check exposed the omitted native CRS in WCS TIFFs. Saved the provider's DescribeCoverage and explicitly interpreted its documented Homolosine grid; retained raw files and native 250 m cells.
6. Ran the scenario/API suite, fixed issues, then reran after forecast integration and cache optimization. Final test output is tests.txt.
7. Executed the inference path under macOS sandbox-exec with all network access denied. The connection canary and actual bilingual/scenario outputs are in os-offline.txt.
8. Measured held-out baseline/model metrics without tuning on test errors, warm/cold timing, fresh-process memory, and HTTP latency. Negative model findings are preserved.
9. Opened the running simulator in the browser. Visually checked English/Urdu layout and exercised Urdu, forecast and missing-location replies. No console or UI success is inferred from a screenshot alone; the resulting messages were checked.

Port 8000 was already occupied, so the app uses 8765. Existing services were not stopped. Human agronomic/Urdu review and Linux validation remain outstanding. This is a research MVP, not a production deployment.
