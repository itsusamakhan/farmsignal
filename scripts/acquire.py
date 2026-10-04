"""Online-only acquisition. Cache immutable responses and provenance, never fabricate."""
import hashlib, json, sys, math
from datetime import datetime, timezone
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import requests
import rasterio
from rasterio.warp import transform_bounds
from farmsignal.config import ROOT, BBOX, PROPERTIES, DEPTHS, IGH, DEMO_FARM
RAW=ROOT/'data/raw'; RAW.mkdir(parents=True,exist_ok=True)
MAN=ROOT/'data/manifest.json'
entries=json.loads(MAN.read_text()) if MAN.exists() else {}
def fetch(name,url,license,kind,**metadata):
 p=RAW/name
 # Reuse a cached file only when it came from the same request (a new region changes the URL).
 if p.exists() and name in entries and entries[name].get('url')==url and hashlib.sha256(p.read_bytes()).hexdigest()==entries[name].get('sha256'): return p
 entry=dict(url=url,license=license,kind=kind,retrieved_at=datetime.now(timezone.utc).isoformat(),**metadata)
 try:
  r=requests.get(url,timeout=(10,45)); r.raise_for_status()
  if name.endswith('.tif') and r.content[:4] not in (b'II*\x00',b'MM\x00*'): raise ValueError('Not a TIFF: '+r.text[:300])
  if name.endswith('.json'): r.json()
  p.write_bytes(r.content); entry.update(status='downloaded',bytes=len(r.content),sha256=hashlib.sha256(r.content).hexdigest())
 except Exception as e:
  entry.update(status='failed',error=str(e)); p=None
 entries[name]=entry; MAN.write_text(json.dumps(entries,indent=2,ensure_ascii=False)); print(name,entry['status'],flush=True)
 return p

def main():
 fetch('power.json',f'https://power.larc.nasa.gov/api/temporal/daily/point?parameters=T2M,PRECTOTCORR&community=AG&longitude={DEMO_FARM[1]:.2f}&latitude={DEMO_FARM[0]:.2f}&start=20230101&end=20251231&format=JSON&time-standard=UTC','NASA open data; acknowledge NASA POWER','historical reanalysis',version='POWER API response header retained',resolution='0.5 x 0.625 degrees meteorology',bbox=BBOX,period=['2023-01-01','2025-12-31'],forecast_issue_time=None)
 fetch('soilgrids-capabilities.xml','https://maps.isric.org/mapserv?map=/map/phh2o.map&SERVICE=WCS&VERSION=2.0.1&REQUEST=GetCapabilities','CC-BY-4.0','service metadata')
 fetch('soilgrids-description.xml','https://maps.isric.org/mapserv?map=/map/phh2o.map&SERVICE=WCS&VERSION=2.0.1&REQUEST=DescribeCoverage&COVERAGEID=phh2o_0-5cm_mean','CC-BY-4.0','native projection metadata')
 bounds=transform_bounds('EPSG:4326',IGH,*BBOX,densify_pts=21)
 west,south,east,north=[math.floor(v/250)*250 if i<2 else math.ceil(v/250)*250 for i,v in enumerate(bounds)]
 # Aligned native projection, no upsampling or reprojecting grid values.
 failed=0
 for prop,(divisor,unit) in PROPERTIES.items():
  for depth in DEPTHS:
   for stat in ['mean','Q0.05','Q0.95']:
    name=f'{prop}_{depth}_{stat}'
    url=f'https://maps.isric.org/mapserv?map=/map/{prop}.map&SERVICE=WCS&VERSION=2.0.1&REQUEST=GetCoverage&COVERAGEID={name}&FORMAT=image/tiff&SUBSET=x({west},{east})&SUBSET=y({south},{north})'
    p=fetch(name+'.tif',url,'CC-BY-4.0; ISRIC SoilGrids 2.0','mapped soil prediction',version='SoilGrids 2.0',depth=depth,statistic=stat,property=prop,divisor=divisor,unit=unit,native_resolution_m=250,bbox=BBOX)
    failed += p is None
    if failed>=3:
     fetch('isda-ph-metadata.json','https://isdasoil.s3.amazonaws.com/soil_data/ph/ph.json','CC-BY-4.0; iSDA','alternative metadata',note='30m EPSG:3857; 0–20/20–50cm; pH x/10; mean and SD, not SoilGrids quantiles')
     print('Repeated soil service failures. Remaining soil layers not attempted; no synthetic replacement.'); return
if __name__=='__main__': main()
