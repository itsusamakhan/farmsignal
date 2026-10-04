---
license: cc-by-4.0
language:
  - en
task_categories:
  - question-answering
  - text-generation
pretty_name: FarmerChat Agricultural Q&A (Large)
size_categories:
  - 1M<n<10M
tags:
  - agriculture
  - farming
  - india
  - africa
  - question-answering
configs:
  - config_name: default
    data_files: train-00000-of-00001.parquet
---

# FarmerChat Agricultural Q&A Dataset (Large)

A dataset of farmer questions and AI-generated answers from [FarmerChat](https://farmerchat.com), a conversational AI assistant serving 1.2M+ farmers across India and East Africa. Published by [Digital Green](https://www.digitalgreen.org).

All queries and responses are in English.

## Overview

**1,446,866 Q&A pairs** spanning **August 2024 — June 2026**, across farmers in India, Kenya, Nigeria, Ethiopia and other regions.

| Country | Q&A Pairs |
|---------|-----------|
| Kenya | 858,674 |
| Nigeria | 296,671 |
| India | 238,030 |
| Ethiopia | 38,114 |
| Other | 15,377 |

## Loading the data

```python
from datasets import load_dataset

ds = load_dataset("DigiGreen/farmerchat-queries-large", split="train")
```

## Data fields

| Field | Description |
|-------|-------------|
| `asset_type` | Type of asset the query relates to (`crop`, `livestock`, `generic`, `mixed`, ...; blank when not classified) |
| `asset_name` | Specific crop or livestock (canonical English name; `generic` = no specific asset; blank when not classified) |
| `query` | Farmer's question in English |
| `response` | Bot's response in English |
| `user_country` | Country of the farmer |
| `user_geo_level2` | State or province |
| `query_year_month` | Year and month of the conversation (`YYYY-MM`) |
| `language` | Language of the conversation (English) |

Names, phone numbers and other personal identifiers in `query` and `response` are masked with `[REDACTED]`.

## Selection criteria

Farmer-initiated messages from English-preferred users, August 2024 onwards.

## License

[Creative Commons Attribution 4.0 International (CC-BY 4.0)](https://creativecommons.org/licenses/by/4.0/)

```bibtex
@dataset{digitalgreen_farmerchat_large_2026,
  title={FarmerChat Agricultural Q&A Dataset (Large)},
  author={Digital Green},
  year={2026},
  url={https://huggingface.co/datasets/DigiGreen/farmerchat-queries-large},
  license={cc-by-4.0}
}
```

## About Digital Green

[Digital Green](https://www.digitalgreen.org) is a global development organization that uses AI and data to improve smallholder farmer outcomes across South Asia and Sub-Saharan Africa.
