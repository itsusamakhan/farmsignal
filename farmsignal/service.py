import re,json,time,hashlib
from datetime import datetime,timezone
from .config import BBOX,ROOT
from .model import IntentModel,normalize
from .store import Store
from .assessment import assess
from .templates import render
from .adapters import Simulator
class Service:
 def __init__(self,store=None):self.model=IntentModel();self.store=store or Store();self.adapter=Simulator()
 def respond(self,text,farm_id='demo',crop=None,standing_water=None,dry_soil=None,referral_fail=False,log=True):
  start=time.perf_counter(); prediction=self.model.predict(text);lang=prediction['language'];t=normalize(text);farm=self.store.farm(farm_id)
  # Explicit structured fields take precedence. No guessed coordinates from messages.
  unsupported=['wheat','rice','cocoa','cotton','tomato','گندم','چاول','کپاس','ٹماٹر']
  explicit_bad=next((x for x in unsupported if x in t),None)
  used_crop=crop.lower() if crop else explicit_bad or ('maize' if any(x in t for x in ['maize','corn','مکئی']) else (farm or {}).get('crop'))
  if standing_water is None:
   if any(s in t for s in ['no standing water','not waterlogged','پانی کھڑا نہیں']):standing_water=False
   elif any(s in t for s in ['standing water','waterlogged','puddles','پانی کھڑا ہے']):standing_water=True
  if dry_soil is None and any(s in t for s in ['dry soil','soil is dry','خشک مٹی','مٹی خشک']):dry_soil=True
  obs={'standing_water':standing_water,'dry_soil':dry_soil}
  r=dict(**prediction,crop=used_crop,location_used=None,data_sources=[],possible_limitations=[],missing_information=[],uncertainty_reason=None,referral={'status':'not_requested','delivered':False,'officer_notified':False},observations=obs,agronomic_confidence=None,template_review_status='AI source-checked draft; human review pending')
  unsafe=any(k in t for k in ['pesticid','fertilizer','disease','spray','کھاد','کیڑے مار','بیماری'])
  if prediction['intent']=='officer':
   r['referral']=self.adapter.refer(referral_fail);key='referral_failed' if referral_fail else 'referral'
  elif prediction['intent']=='unknown' or unsafe or lang=='unknown':
   key='clarify';r['intent']='unknown';r['abstained']=True;r['uncertainty_reason']='Unsupported, ambiguous, or low-confidence message.'
  elif not farm or farm['lat'] is None or farm['lon'] is None:key='location';r['missing_information']=['registered_location']
  else:
   lat,lon=farm['lat'],farm['lon'];r['location_used']={'lat':lat,'lon':lon,'source':'registered farm','farm_id':farm_id}
   if not BBOX[0]<=lon<=BBOX[2] or not BBOX[1]<=lat<=BBOX[3]:key='outside';r['missing_information']=['regional_coverage']
   elif used_crop is None:key='crop';r['missing_information']=['crop']
   elif used_crop!='maize':key='unsupported';r['uncertainty_reason']='Crop outside scope'
   else:
    e=self.store.evidence(lat,lon);a=assess(e,obs);r.update(a);r['data_sources']=[e['weather']]+e['soil']+e['forecasts'];r['historical_weather']=e['weather']
    limits=a['possible_limitations'];missing=a['missing_information']
    if prediction['intent']=='weather':key='weather' if a['forecast_status']!='fresh' else 'forecast'
    elif 'reported_standing_water' in limits:key='drainage'
    elif 'reported_dry_soil' in limits:key='dry'
    elif any(s.startswith(('soil_pH_','valid_soil_')) for s in missing):key='soil_missing'
    elif limits:key='ph'
    elif standing_water is None:key='drainage_question'
    elif a['forecast_status']!='fresh':key='weather'
    else:key='moisture'
  r.update(message=render(key,lang),next_step_reason=key,response_time_ms=round((time.perf_counter()-start)*1000,3),created_at=datetime.now(timezone.utc).isoformat())
  if key=='forecast':
   f=r['forecast_used'];end=f['valid_until'][:16].replace('T',' ')
   r['message']=(f"محفوظ پیش گوئی {end} UTC تک ہے۔ بوائی سے پہلے کھیت کی نمی دیکھیں۔" if lang=='ur' else f"The saved forecast ends {end} UTC. Check moisture in your field before sowing.")
  if key in ('location','outside','crop','unsupported','soil_missing','weather','clarify'):r['abstained']=True
  if log:
   # Do not store raw messages, phone numbers, or exact farm locations in audit logs.
   entry={k:r[k] for k in ['intent','next_step_reason','created_at','response_time_ms']}
   with (ROOT/'data/audit.jsonl').open('a') as f:f.write(json.dumps(entry)+'\n')
  return r
