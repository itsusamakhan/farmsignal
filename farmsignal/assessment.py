import json,math
from datetime import datetime,timezone,timedelta
from .config import ROOT,DEPTHS
RULES=json.loads((ROOT/'data/rules.json').read_text())
def assess(evidence,observations,now=None):
 now=now or datetime.now(timezone.utc); limitations=[];missing=[]; findings=[]
 ph_rule=RULES['rules'][0];lo,hi=ph_rule['optimal_min'],ph_rule['optimal_max']
 for depth in DEPTHS:
  records={r['statistic']:r for r in evidence['soil'] if r['property']=='phh2o' and r['depth']==depth}
  if not all(s in records for s in ('mean','Q0.05','Q0.95')):
   missing.append('soil_pH_'+depth);continue
  if any(r.get('unit')!='pH' or not isinstance(r.get('value'),(float,int)) or not math.isfinite(r['value']) or not 0<r['value']<=14 for r in records.values()):
   missing.append('valid_soil_units_or_values_'+depth);continue
  mean,lower,upper=[records[s]['value'] for s in ('mean','Q0.05','Q0.95')]
  if lower>upper:missing.append('valid_soil_uncertainty_'+depth);continue
  finding=dict(depth=depth,mean=mean,lower=lower,upper=upper,unit='pH',rule='maize_ph')
  if mean<lo or mean>hi:limitations.append('mapped_pH_outside_reference')
  if lower<lo or upper>hi:limitations.append('soil_uncertainty_crosses_reference')
  findings.append(finding)
 fresh=[]
 for f in evidence.get('forecasts',[]):
  try:
   issue=datetime.fromisoformat(f['issue_time']);start=datetime.fromisoformat(f['valid_from']);end=datetime.fromisoformat(f['valid_until'])
   if all(isinstance(f.get(k),(int,float)) and math.isfinite(f[k]) for k in ['temperature_c','rain_mm']) and f['rain_mm']>=0 and issue<=start<end and issue<=now and now-issue<=timedelta(hours=48) and start<=now<end and f['unit']=='mm/24h' and f['source']:
    fresh.append(f)
  except (ValueError,TypeError,KeyError):pass
 if not fresh:missing.append('fresh_forecast')
 if observations.get('standing_water') is True:limitations.append('reported_standing_water')
 if observations.get('standing_water') is None:missing.append('field_drainage_observation')
 if observations.get('dry_soil') is True:limitations.append('reported_dry_soil')
 missing.extend(['field_soil_test','variety_and_planting_date','root_zone_moisture'])
 return dict(possible_limitations=sorted(set(limitations)),missing_information=missing,soil_findings=findings,forecast_used=fresh[0] if fresh else None,forecast_status='fresh' if fresh else 'stale' if evidence.get('forecasts') else 'unavailable',rule_version=RULES['version'],rules=RULES['rules'],agronomic_confidence=None,uncertainty_reason='Mapped soil and historical weather cannot establish field-level planting suitability.')
