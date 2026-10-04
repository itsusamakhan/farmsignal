# Local data schema

`data/manifest.json` maps filenames to URL, retrieval UTC, status, bytes, SHA-256, license, source version and property metadata. Failed requests retain the error and request time. Successful cache reuse validates the checksum. Raw downloads are preserved.

`data/cache.sqlite` contains:

| Table | Fields and meaning |
|---|---|
| soil | property, depth, statistic, native row/column, pixel-centre lon/lat, converted value, unit, source filename. Primary key: property/depth/statistic/row/column. Actual point lookup uses pixel containment in the native raster transform. Missing raster cells are omitted. |
| weather | date, temperature_c, rain_mm, source, observation_time (daily reanalysis date label), forecast_issue_time (null), valid_time, downloaded_at, kind. Missing -999 values become SQL NULL. |
| forecasts | issue_time, valid_from, valid_until, downloaded_at, source, temperature_c (+24h instantaneous), rain_mm (0–24h accumulation), unit (`mm/24h`). Full gridpoint and conversion metadata live in `data/forecast.json`. |
| farms | id, name, lat, lon, crop. Fictional demo registrations only. |

Soil map observation times are unknown; retrieval time is not a field sampling date. The native WCS service uses Interrupted Goode Homolosine, pseudo EPSG:152160. Its TIFFs have a valid affine transform but no recognized CRS. We use the saved DescribeCoverage definition (`+proj=igh +datum=WGS84 +units=m +no_defs`) without resampling. The manifest's requested WGS84 box and native raster grid metadata are retained. The grid includes a narrow padding outside the requested box, while inference checks the requested box first.

`data/intents.json`: text, intent, language, family, split, provenance. Bilingual counterparts share a family and split.

`data/rules.json`: version, review status, reference intervals, citations, scope, operational policies. No thresholds exist for the other seven soil properties.

`data/audit.jsonl`: UTC, predicted intent, response reason and latency only. UI text never becomes executable HTML.
