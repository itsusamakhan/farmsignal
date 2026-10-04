import json,sqlite3,sys,hashlib
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import numpy as np
import rasterio
from rasterio.warp import transform
from farmsignal.config import *
SCHEMA='''
CREATE TABLE soil(property TEXT, depth TEXT, statistic TEXT, row INTEGER, col INTEGER, lon REAL, lat REAL, value REAL, unit TEXT, source TEXT, PRIMARY KEY(property,depth,statistic,row,col));
CREATE INDEX soil_lookup ON soil(property,depth,statistic);
CREATE INDEX soil_cell ON soil(source,row,col);
CREATE TABLE weather(date TEXT PRIMARY KEY, temperature_c REAL, rain_mm REAL, source TEXT, observation_time TEXT, forecast_issue_time TEXT, valid_time TEXT, downloaded_at TEXT, kind TEXT);
CREATE TABLE farms(id TEXT PRIMARY KEY, name TEXT, lat REAL, lon REAL, crop TEXT);
CREATE TABLE forecasts(issue_time TEXT, valid_from TEXT, valid_until TEXT, downloaded_at TEXT, source TEXT, temperature_c REAL, rain_mm REAL, unit TEXT);
'''
def main():
 man=json.loads((ROOT/'data/manifest.json').read_text()); tmp=DB.with_suffix('.tmp')
 tmp.unlink(missing_ok=True)
 # WCS TIFFs omit nodata metadata. Joint zero pH and bulk density is
 # suspect fill, not usable agricultural evidence. Preserve raw files.
 suspect=None
 ph=ROOT/'data/raw/phh2o_0-5cm_mean.tif';bd=ROOT/'data/raw/bdod_0-5cm_mean.tif'
 if ph.exists() and bd.exists():
  with rasterio.open(ph) as a,rasterio.open(bd) as b:
   assert a.shape==b.shape and a.transform==b.transform
   suspect=(a.read(1)==0)&(b.read(1)==0)
 report={'bbox_wsen':BBOX,'suspect_joint_zero_cells_per_layer':int(suspect.sum()) if suspect is not None else None,'soil':{},'weather':{},'limitations':['Mapped soils are not field measurements.','Three historical years are context, not climate normals or a current forecast.','No local agronomist or native Urdu review has been performed.']}
 with sqlite3.connect(tmp) as c:
  c.executescript(SCHEMA)
  c.executemany('INSERT INTO farms VALUES (?,?,?,?,?)',[('demo','Sahiwal demonstration farm',*DEMO_FARM,'maize'),('unregistered','No farm registered',None,None,None),('outside','Outside downloaded region',*OUTSIDE_FARM,'maize')])
  for filename,entry in man.items():
   p=ROOT/'data/raw'/filename
   if entry['status']!='downloaded' or not p.exists(): continue
   assert hashlib.sha256(p.read_bytes()).hexdigest()==entry['sha256'],f'Checksum mismatch: {filename}'
   if filename.endswith('.tif'):
    prop=entry['property']; divisor,unit=PROPERTIES[prop]
    assert entry['unit']==unit and entry['divisor']==divisor
    with rasterio.open(p) as ds:
     assert abs(ds.res[0]-250)<.01 and abs(ds.res[1]-250)<.01
     crs=ds.crs or IGH  # WCS DescribeCoverage declares native EPSG:152160; TIFF omits pseudo CRS
     a=ds.read(1,masked=True)
     if suspect is not None:
      assert a.shape==suspect.shape
      a=np.ma.masked_where(suspect,a)
     count=0
     for row in range(ds.height):
      for col in range(ds.width):
       if np.ma.is_masked(a[row,col]): continue
       x,y=ds.xy(row,col); lon,lat=transform(crs,'EPSG:4326',[x],[y]); value=float(a[row,col])/divisor
       if not np.isfinite(value): continue
       c.execute('INSERT INTO soil VALUES (?,?,?,?,?,?,?,?,?,?)',(prop,entry['depth'],entry['statistic'],row,col,lon[0],lat[0],value,unit,filename));count+=1
     report['soil'][filename]={'valid_cells':count,'missing_cells':int(a.size-count),'resolution':list(ds.res),'crs':str(crs),'unit':unit,'depth':entry['depth'],'range':[float(a.min())/divisor,float(a.max())/divisor] if count else None}
   if filename=='power.json':
    d=json.loads(p.read_text()); params=d['properties']['parameter']; units={k:v['units'] for k,v in d['parameters'].items()}
    assert units['T2M']=='C' and units['PRECTOTCORR']=='mm/day',units
    missing=0
    for date,t in params['T2M'].items():
     rain=params['PRECTOTCORR'].get(date,-999); t=None if t==-999 else t; rain=None if rain==-999 else rain
     missing+=int(t is None or rain is None); iso=f'{date[:4]}-{date[4:6]}-{date[6:]}'
     c.execute('INSERT INTO weather VALUES (?,?,?,?,?,?,?,?,?)',(iso,t,rain,filename,iso,None,iso,entry['retrieved_at'],'historical reanalysis'))
    report['weather']={'days':len(params['T2M']),'missing_days':missing,'units':units,'header':d['header'],'coordinates':d['geometry']['coordinates']}
 with sqlite3.connect(tmp) as c:
  fp=ROOT/'data/forecast.json'
  if fp.exists():
   f=json.loads(fp.read_text());c.execute('INSERT INTO forecasts VALUES (?,?,?,?,?,?,?,?)',tuple(f[k] for k in ['issue_time','valid_from','valid_until','downloaded_at','source','temperature_c','rain_mm','unit']))
 tmp.replace(DB); (ROOT/'reports/data-quality.json').write_text(json.dumps(report,indent=2));print(json.dumps({'soil_layers':len(report['soil']),'weather':report['weather'].get('days',0)}))
if __name__=='__main__':main()
