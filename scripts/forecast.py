"""Download two ECMWF GRIB messages by byte range; retain one pilot gridpoint."""
import sys,json,hashlib
from pathlib import Path
from datetime import datetime,timedelta,timezone
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import requests
from eccodes import codes_grib_new_from_file,codes_grib_find_nearest,codes_release,codes_get
from farmsignal.config import ROOT,DEMO_FARM
from scripts.acquire import fetch,RAW,MAN,entries

def main():
 now=datetime.now(timezone.utc);chosen=None
 for offset in range(4):
  day=(now-timedelta(days=offset)).strftime('%Y%m%d')
  for hour in ['12','00']:
   issue=datetime.strptime(day+hour,'%Y%m%d%H').replace(tzinfo=timezone.utc)
   if issue>now or now-issue>timedelta(hours=48):continue
   base=f'https://data.ecmwf.int/forecasts/{day}/{hour}z/ifs/0p25/oper/{day}{hour}0000-24h-oper-fc'
   p=fetch(f'ecmwf-{day}{hour}.index',base+'.index','CC-BY-4.0; ECMWF','forecast index',issue_time=issue.isoformat())
   if p:
    try: index=[json.loads(line) for line in p.read_text().splitlines()];chosen=(base,index,issue);break
    except ValueError:pass
  if chosen:break
 if not chosen:print('No forecast available; inference will abstain.');return
 base,index,issue=chosen;values={};sources=[]
 for param in ['2t','tp']:
  e=next(x for x in index if x.get('param')==param and x.get('levtype')=='sfc');start=e['_offset'];length=e['_length'];url=base+'.grib2'
  name=f'ecmwf-{issue:%Y%m%d%H}-{param}.grib2';p=RAW/name
  if not p.exists():
   r=requests.get(url,headers={'Range':f'bytes={start}-{start+length-1}'},timeout=45);r.raise_for_status()
   if r.status_code!=206 or len(r.content)!=length:raise ValueError('Server did not honor bounded byte-range request')
   p.write_bytes(r.content)
  entries[name]=dict(url=url,license='CC-BY-4.0; ECMWF',kind='forecast',status='downloaded',retrieved_at=now.isoformat(),sha256=hashlib.sha256(p.read_bytes()).hexdigest(),bytes=p.stat().st_size,byte_range=[start,start+length-1],issue_time=issue.isoformat(),version='IFS open data 0p25',note='One GRIB message is a global grid; only the pilot point is used.')
  with p.open('rb') as f:
   gid=codes_grib_new_from_file(f);v=codes_grib_find_nearest(gid,*DEMO_FARM)[0];unit=codes_get(gid,'units');values[param]={'value':v['value'],'units':unit,'lat':v['lat'],'lon':v['lon'],'distance_km':v['distance']};codes_release(gid)
  sources.append(name)
 assert values['2t']['units']=='K' and values['tp']['units']=='m',values
 record=dict(issue_time=issue.isoformat(),valid_from=issue.isoformat(),valid_until=(issue+timedelta(hours=24)).isoformat(),downloaded_at=now.isoformat(),source='ECMWF IFS 0.25 degree; '+', '.join(sources),temperature_c=values['2t']['value']-273.15,rain_mm=values['tp']['value']*1000,unit='mm/24h',gridpoint=values,temperature_valid_time=(issue+timedelta(hours=24)).isoformat(),precipitation_period='Accumulation from issue to +24h, not the next 24h from query time')
 (ROOT/'data/forecast.json').write_text(json.dumps(record,indent=2));MAN.write_text(json.dumps(entries,indent=2));print(json.dumps(record,indent=2))
if __name__=='__main__':main()
