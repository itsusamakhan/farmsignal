# Data decisions and quality

Sources checked and data retrieved on 2026-10-04. Exact times and checksums are in `data/manifest.json`. The small pilot box near Kitale is provisional, chosen after successful soil and weather acquisition. No field measurements, yield labels, or real farmer registration records are claimed.

## SoilGrids

[ISRIC layer definitions](https://docs.isric.org/globaldata/soilgrids/SoilGrids_faqs_01.html), [access and licensing](https://docs.isric.org/globaldata/soilgrids/SoilGrids_faqs_02.html), [WCS guidance](https://docs.isric.org/globaldata/soilgrids/wcs_from_R.html).

Eight properties × three depths × mean/Q0.05/Q0.95 = 72 layers. Each native regional raster is 10×10 pixels, at 250 m. The source is SoilGrids 2.0, CC BY 4.0, attributed to ISRIC. Soil predictions are static mapped estimates with no field-specific observation date or live update guarantee.

| Property | Raw units | Divide by | Stored units |
|---|---|---:|---|
| phh2o | pH × 10 | 10 | pH |
| sand, silt, clay | g/kg | 10 | % |
| soc | dg/kg | 10 | g/kg |
| cec | mmol(c)/kg | 10 | cmol(c)/kg |
| cfvo | cm³/dm³ | 10 | vol% |
| bdod | cg/cm³ | 100 | kg/dm³ |

Depths: 0–5, 5–15, 15–30 cm. Mean and quantiles are kept independently at each depth. Quantiles are prediction uncertainty, not repeat laboratory measurements. The rule checks pH only and never infers a crop-success label. Reported 90% intervals crossing a reference boundary prompt testing. Other properties remain context, with no invented thresholds. Missingness and min/max for every raster are in the generated quality report.

The WCS worked; the beta REST API was unnecessary. Native CRS metadata is documented in SCHEMA.md. iSDAsoil was investigated but not substituted: its public AWS COGs are 30 m in EPSG:3857, with 0–20 and 20–50 cm mean/standard-deviation bands. Its pH back-transform is x/10; other properties require individual metadata checks. CC BY 4.0. Its authenticated API needs signup, while AWS permits regional reads. [Official AWS guide](https://www.isda-africa.com/isdasoil/isdasoil-on-aws/). No iSDA soil values are used.

## Historical weather

[NASA POWER daily API](https://power.larc.nasa.gov/docs/services/api/temporal/daily/), [source/latency information](https://power.larc.nasa.gov/docs/faqs/data/), [resolution/revision guidance](https://power.larc.nasa.gov/docs/tutorials/service-data-request/api/).

One representative point, 1.02° N / 35° E, supplies 2023–2025 daily T2M and PRECTOTCORR in UTC. This is model/assimilation-derived historical context, not a station at the farm and not a forecast. Meteorological resolution is approximately 0.5° × 0.625°; the pilot area is much smaller. API units are checked as °C and mm/day. Dates and missing -999 values are preserved. NASA documents about 2–3 days of latency and later meteorological revisions. The fixed historical period avoids representing low-latency data as today's weather. Three years are insufficient for a climatological normal. Acknowledge the NASA POWER Project; NASA's public data are openly available, not relabelled as CC BY.

[CHIRPS v3](https://www.chc.ucsb.edu/data/chirps3) was considered but not needed in the minimum combination: 0.05° satellite/station rainfall, with delayed preliminary/final releases. Its daily series disaggregates pentad totals; it cannot supply a current forecast. No CHIRPS data were downloaded or used.

## Forecast

[ECMWF open data](https://www.ecmwf.int/en/forecasts/datasets/open-data). IFS 0.25° surface 2t and tp from the newest accessible 00/12 UTC operational run. Only two bounded GRIB messages are downloaded via HTTP ranges (a few MB, not the global dataset catalogue). The messages contain global grids; the nearest pilot gridpoint is extracted. The retained point is 1° N / 35° E, about 2.22 km from the demo registration, on a much coarser grid.

Kelvin is converted to °C and metres to millimetres after checking the GRIB unit metadata. Temperature is valid at issue +24h. Rain is accumulated from issue to +24h. That period must not be interpreted as the next 24h from an arbitrary request. The response shows the cached forecast's end time and does not infer a precise planting date. The application accepts a forecast only inside its stated valid interval, with issue time not in the future and issue age at most 48h (an application policy). Missing/expired forecasts trigger a fresh-local-forecast next step. CC BY 4.0, attribution ECMWF. The first 2026-10-04 00 UTC index was unavailable; this recorded failure led to the accessible prior run.

## Agronomic evidence

[FAO ECOCROP Zea mays](https://ecocrop.apps.fao.org/ecocrop/srv/en/dataSheet?id=2175) supports a global optimal pH reference of 5–7. This is a screening reference, not a field suitability verdict. [KALRO maize guidance](https://keep.kalro.org/good-agricultural-practices/Maize) supports checking drainage. [KALRO land preparation](https://www.kalro.org/maize/maize-land-preparation/) supports checking soil moisture before sowing. Kenyan guidance may use narrower optimal pH ranges depending on context; the global rule is explicitly provisional. No fertilizer, lime, pesticide, cultivar, or crop-success prescription is implemented. Local expert review remains pending.

## Language/model data

[Digital Green FarmerChat](https://www.digitalgreen.org/farmerchat) links to [DigiGreen/farmerchat-queries-large](https://huggingface.co/datasets/DigiGreen/farmerchat-queries-large). The downloaded dataset card declares CC BY 4.0 and English questions with AI-generated answers. A bounded five-row preview failed with a server-side Parquet scan-size limit; no actual Q&A rows were obtained, and none were used for training. No agronomic ground truth is claimed from it.

Instead, this build uses 140 AI-authored bilingual examples: 80 training, 20 validation, 40 test. Each pair is marked synthetic/AI-translated, with no fabricated human author or review. Families remain wholly in one split. The manual-family design limits direct translation leakage but does not eliminate same-author or linguistic-template bias. There is no suitability model, no spatially trained model, and no WoSIS evaluation; geographic leakage and overlap metrics therefore do not apply to this experiment.

### Data-quality correction

WCS TIFFs contain joint zero pH/bulk-density cells but omit nodata metadata. We conservatively exclude those aligned cells from all soil layers, retaining the unmodified downloads. The original demonstration location lies in such a cell: inference must report missing soil evidence. The regenerated quality report distinguishes valid from excluded cells; previous statements that all downloaded cells were valid were incorrect. No demonstration location was moved to conceal this issue.
