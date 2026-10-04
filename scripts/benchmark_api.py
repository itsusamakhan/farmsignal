"""Measure a running localhost API; no remote endpoints."""
import time,json,statistics
from pathlib import Path
import requests
ROOT=Path(__file__).resolve().parents[1]
lat=[]
for _ in range(30):
 start=time.perf_counter();r=requests.post('http://127.0.0.1:8765/api/message',json={'text':'Can I grow maize here?'},timeout=10);r.raise_for_status();assert r.json()['crop']=='maize';lat.append((time.perf_counter()-start)*1000)
lat.sort();out={'localhost_http_samples':len(lat),'p50_ms':statistics.median(lat),'p95_ms':lat[int(.95*(len(lat)-1))],'includes':'HTTP, input validation, inference, evidence lookup, JSON serialization and audit logging'}
(ROOT/'reports/api-latency.json').write_text(json.dumps(out,indent=2));print(out)
