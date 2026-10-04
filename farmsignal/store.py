import sqlite3,json
from .config import DB,ROOT,BBOX,IGH
class Store:
 def __init__(self,path=DB):
  self.path=path
  self.manifest=json.loads((ROOT/'data/manifest.json').read_text())
  # Read local grid geometry once. Cache refresh requires a gateway restart.
  import rasterio
  self.grids=[]
  for name,e in self.manifest.items():
   if e.get('kind')!='mapped soil prediction' or e.get('status')!='downloaded':continue
   p=ROOT/'data/raw'/name
   if p.exists():
    with rasterio.open(p) as ds:self.grids.append((name,e,ds.crs or IGH,ds.transform,ds.width,ds.height))
 def connect(self):
  c=sqlite3.connect(f'file:{self.path}?mode=ro',uri=True);c.row_factory=sqlite3.Row;return c
 def farm(self,id):
  with self.connect() as c:
   row=c.execute('SELECT * FROM farms WHERE id=?',(id,)).fetchone();return dict(row) if row else None
 def evidence(self,lat,lon):
  from rasterio.warp import transform
  from rasterio.transform import rowcol
  soil=[];coords={}
  with self.connect() as c:
   for name,e,crs,affine,width,height in self.grids:
    key=str(crs)
    if key not in coords:coords[key]=transform('EPSG:4326',crs,[lon],[lat])
    x,y=coords[key];row,col=rowcol(affine,x[0],y[0]);row,col=int(row),int(col)
    if not 0<=row<height or not 0<=col<width:continue
    found=c.execute('SELECT * FROM soil WHERE source=? AND row=? AND col=?',(name,row,col)).fetchone()
    if found:
     record=dict(found);record.update(downloaded_at=e['retrieved_at'],url=e['url'],kind=e['kind'],observation_time=None);soil.append(record)
   w=c.execute('SELECT min(date) start,max(date) end,count(*) days,avg(temperature_c) mean_temperature_c,sum(rain_mm) total_rain_mm,count(temperature_c) temperature_days,count(rain_mm) rain_days FROM weather').fetchone()
   weather=dict(w);weather.update(kind='historical reanalysis',forecast=False,source=self.manifest.get('power.json',{}))
   forecasts=[dict(r) for r in c.execute('SELECT * FROM forecasts ORDER BY issue_time DESC')]
  return dict(soil=soil,weather=weather,forecasts=forecasts)
