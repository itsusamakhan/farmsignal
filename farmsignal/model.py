import re,unicodedata
import joblib
from .config import ROOT
KEYS={'officer':['officer','human','adviser','expert','extension','person','افسر','انسان','مشیر','ماہر','شخص'], 'weather':['rain','weather','temperature','forecast','hot','بارش','موسم','درجہ حرارت','گرمی'], 'soil':['soil','acid','clay','sandy','waterlog','drain','مٹی','تیزابی','پانی کھڑا','نکاسی'], 'planting':['maize','corn','plant','sow','cultivat','مکئی','کاشت','بوؤں']}
def normalize(t):
 return ''.join(c for c in unicodedata.normalize('NFKC',t.lower()) if unicodedata.category(c)!='Mn')
def baseline(t):
 t=normalize(t)
 for label,keys in KEYS.items():
  if any(k in t for k in keys):return label
 return 'unknown'
class IntentModel:
 def __init__(self):
  obj=joblib.load(ROOT/'models/intent.joblib');self.pipeline=obj['pipeline']; self.threshold=obj['threshold']
 def predict(self,text):
  t=normalize(text); p=self.pipeline.predict_proba([t])[0]; i=int(p.argmax()); raw=str(self.pipeline.classes_[i]); conf=float(p[i])
  # Language is a conservative script heuristic, not validated language identification.
  lang='ur' if re.search('[\u0600-\u06ff]',t) else 'en' if re.search('[a-z]',t) else 'unknown'
  recognizable=any(any(k in t for k in keys) for keys in KEYS.values())
  label=raw if conf>=self.threshold and recognizable else 'unknown'
  return {'intent':label,'raw_intent':raw,'intent_confidence':conf,'language':lang,'abstained':label=='unknown'}
