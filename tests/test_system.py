import copy,json,socket,sqlite3
from datetime import datetime,timezone,timedelta
from unittest.mock import patch
import pytest
from fastapi.testclient import TestClient
from farmsignal.service import Service
from farmsignal.api import app
from farmsignal.assessment import assess
from farmsignal.config import ROOT,DEPTHS
@pytest.fixture(scope='module')
def service():return Service()
def test_normal_bilingual(service):
 for text in ['Can I grow maize here?','کیا میں یہاں مکئی اُگا سکتا ہوں؟']:
  r=service.respond(text,log=False);assert r['intent']=='planting';assert r['agronomic_confidence'] is None;assert r['data_sources'];assert 'safe to plant' not in r['message']
def test_missing_location(service):assert service.respond('Can I grow maize here?',farm_id='unregistered',log=False)['next_step_reason']=='location'
def test_outside(service):assert service.respond('Can I grow maize here?',farm_id='outside',log=False)['next_step_reason']=='outside'
def test_unsupported_crop(service):assert service.respond('Can I grow maize here?',crop='rice',log=False)['next_step_reason']=='unsupported'
def test_referral_failure(service):
 r=service.respond('I need an agricultural officer',referral_fail=True,log=False);assert r['referral']['status']=='simulated_failed';assert not r['referral']['officer_notified']
@pytest.mark.parametrize('text',['🛸🛸','bonjour comment allez vous','How much fertilizer for maize?','Tell me a joke','مکئی کے لیے کتنی کھاد ڈالوں؟'])
def test_unknown(service,text):assert service.respond(text,log=False)['intent']=='unknown'
def test_network_blocked(service):
 with patch.object(socket.socket,'connect',side_effect=AssertionError('network forbidden')),patch('socket.getaddrinfo',side_effect=AssertionError('DNS forbidden')):
  assert service.respond('Can I grow maize here?',log=False)['data_sources']
def fixture_evidence():
 # Explicitly synthetic boundary fixtures, not downloaded observations.
 return {'soil':[dict(property='phh2o',depth=d,statistic=s,value=v,unit='pH') for d in DEPTHS for s,v in [('mean',6),('Q0.05',5.5),('Q0.95',6.5)]],'forecasts':[]}
def test_missing_soil():assert 'soil_pH_0-5cm' in assess({'soil':[]},{})['missing_information']
@pytest.mark.parametrize('unit',['percent',None])
def test_invalid_units(unit):
 e=fixture_evidence();e['soil'][0]['unit']=unit;assert any('valid_soil' in x for x in assess(e,{})['missing_information'])
def test_wide_uncertainty():
 e=fixture_evidence();e['soil'][1]['value']=4;assert 'soil_uncertainty_crosses_reference' in assess(e,{})['possible_limitations']
def test_reversed_quantiles():
 e=fixture_evidence();e['soil'][1]['value']=8;assert 'valid_soil_uncertainty_0-5cm' in assess(e,{})['missing_information']
def test_expired_weather():
 e=fixture_evidence();n=datetime.now(timezone.utc);e['forecasts']=[dict(issue_time=(n-timedelta(days=3)).isoformat(),valid_from=(n-timedelta(days=3)).isoformat(),valid_until=(n-timedelta(days=1)).isoformat(),unit='mm/24h',source='synthetic fixture',temperature_c=25.,rain_mm=2.)];assert assess(e,{},n)['forecast_status']=='stale'
def test_future_issue():
 e=fixture_evidence();n=datetime.now(timezone.utc);e['forecasts']=[dict(issue_time=(n+timedelta(hours=1)).isoformat(),valid_from=n.isoformat(),valid_until=(n+timedelta(days=1)).isoformat(),unit='mm/24h',source='synthetic fixture',temperature_c=25.,rain_mm=2.)];assert assess(e,{},n)['forecast_status']=='stale'
def test_observations_change_reply(service):
 assert service.respond('Can I grow maize here?',standing_water=True,log=False)['next_step_reason']=='drainage'
 assert service.respond('Can I grow maize here?',dry_soil=True,log=False)['next_step_reason']=='dry'
def test_negation(service):assert service.respond('My maize field has no standing water',log=False)['observations']['standing_water'] is False
def test_split_integrity():
 rows=json.loads((ROOT/'data/intents.json').read_text());families={}
 for r in rows:families.setdefault(r['family'],set()).add(r['split'])
 assert all(len(s)==1 for s in families.values());assert len({r['text'] for r in rows})==len(rows)
def test_api():
 with TestClient(app) as c:
  assert c.get('/').status_code==200;assert c.get('/health').json()['sms_delivery'] is False
  assert c.post('/api/message',json={'text':'Can I grow maize here?'}).json()['crop']=='maize'
  assert c.post('/api/message',json={'text':''}).status_code==422
  assert c.post('/api/message',json={'text':'x','farm_id':"'; DROP TABLE farms;"}).status_code==422
def test_fresh_forecast():
 e=fixture_evidence();n=datetime.now(timezone.utc);e['forecasts']=[dict(issue_time=(n-timedelta(hours=3)).isoformat(),valid_from=(n-timedelta(hours=3)).isoformat(),valid_until=(n+timedelta(hours=21)).isoformat(),unit='mm/24h',source='synthetic fixture',temperature_c=25.,rain_mm=2.)];assert assess(e,{},n)['forecast_status']=='fresh'
def test_missing_crop(service):
 with patch.object(service.store,'farm',return_value={'lat':1.02,'lon':35.,'crop':None}):assert service.respond('Check planting suitability',log=False)['next_step_reason'] in ['crop','clarify']
def test_missing_cell_response(service):
 with patch.object(service.store,'evidence',return_value={'soil':[],'weather':{},'forecasts':[]}):assert service.respond('Can I grow maize here?',log=False)['next_step_reason']=='soil_missing'

@pytest.mark.parametrize('text',["My maize soil is not dry", "My maize soil isn't dry", 'میری مکئی کی مٹی خشک نہیں'])
def test_dry_negation(service,text):
 assert service.respond(text,log=False)['observations']['dry_soil'] is False

def test_explicit_unsupported_before_classifier(service):
 assert service.respond('Can I grow rice here?',log=False)['next_step_reason']=='unsupported'

def test_refusal_explained(service):
 r=service.respond('Can I grow maize here?',farm_id='unregistered',log=False)
 assert r['uncertainty_reason'] and r['advice_status']=='insufficient_evidence'
 assert not r['intent_abstained']

@pytest.mark.parametrize('invalid',[None,float('nan'),float('inf'),-1])
def test_forecast_invalid_rain(invalid):
 e=fixture_evidence();n=datetime.now(timezone.utc)
 e['forecasts']=[dict(issue_time=(n-timedelta(hours=3)).isoformat(),valid_from=(n-timedelta(hours=3)).isoformat(),valid_until=(n+timedelta(hours=21)).isoformat(),unit='mm/24h',source='fixture',temperature_c=25.,rain_mm=invalid)]
 assert assess(e,{},n)['forecast_status']=='stale'

def test_tomorrow_not_covered(service):
 e=fixture_evidence();n=datetime.now(timezone.utc)
 end=n.replace(hour=23,minute=59,second=59)
 e['weather']={};e['forecasts']=[dict(issue_time=(n-timedelta(hours=1)).isoformat(),valid_from=(n-timedelta(hours=1)).isoformat(),valid_until=end.isoformat(),unit='mm/24h',source='fixture',temperature_c=25.,rain_mm=2.)]
 with patch.object(service.store,'evidence',return_value=e):
  r=service.respond('Will it rain tomorrow?',log=False)
  assert r['next_step_reason']=='forecast_horizon'

def test_crop_substring_not_a_crop(service):
 r=service.respond('What is the price of a tractor?',log=False)
 assert r['next_step_reason']=='clarify'

def test_zero_filled_ph_rejected():
 e=fixture_evidence()
 for r in e['soil']:r['value']=0
 a=assess(e,{})
 assert not a['soil_findings']
 assert 'valid_soil_units_or_values_0-5cm' in a['missing_information']
