import json,sys,time,platform,resource,subprocess,statistics,socket
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import numpy as np
from sklearn.metrics import classification_report,f1_score
from farmsignal.config import ROOT
from farmsignal.model import IntentModel,baseline,normalize
from farmsignal.service import Service
rows=json.loads((ROOT/'data/intents.json').read_text());test=[r for r in rows if r['split']=='test'];m=IntentModel();out={}
for lang in ('en','ur'):
 subset=[r for r in test if r['language']==lang];y=[r['intent'] for r in subset];texts=[r['text'] for r in subset]
 out[lang]={}
 for name,pred in [('keyword',[baseline(t) for t in texts]),('classifier_raw',m.pipeline.predict([normalize(t) for t in texts]).tolist()),('classifier_with_abstention',[m.predict(t)['intent'] for t in texts])]:
  out[lang][name]={'macro_f1':f1_score(y,pred,average='macro'),'per_class':classification_report(y,pred,output_dict=True,zero_division=0),'errors':[{'text':t,'expected':a,'predicted':b} for t,a,b in zip(texts,y,pred) if a!=b]}
 s=[m.predict(t) for t in texts];out[lang]['abstention_rate']=sum(x['abstained'] for x in s)/len(s);out[lang]['incorrect_confident_count']=sum(x['intent']!=r['intent'] and not x['abstained'] for x,r in zip(s,subset))
# Timings include full response path, local data lookup, and logging, after warm-up.
s=Service();s.respond('Can I grow maize here?',log=False);lat=[]
for i in range(100):
 start=time.perf_counter();s.respond('Can I grow maize here?',log=False);lat.append((time.perf_counter()-start)*1000)
cold=[]
for _ in range(5):
 start=time.perf_counter();subprocess.run([sys.executable,'-c','from farmsignal.service import Service;Service().respond("Can I grow maize here?",log=False)'],cwd=ROOT,check=True,capture_output=True);cold.append((time.perf_counter()-start)*1000)
mem=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss;mem=mem/(1024*1024) if sys.platform=='darwin' else mem/1024
report={'language_results':out,'performance':{'warm_response_ms':{'p50':float(np.percentile(lat,50)),'p95':float(np.percentile(lat,95)),'samples':len(lat)},'cold_process_response_ms':{'p50':float(np.percentile(cold,50)),'p95':float(np.percentile(cold,95)),'samples':len(cold)},'peak_evaluation_process_rss_mib':mem,'model_bytes':(ROOT/'models/intent.joblib').stat().st_size,'hardware':platform.platform()+' '+platform.machine(),'python':sys.version},'limitations':['40 AI-authored test examples total; same author as training, so independence is limited.','Bilingual semantic families are assigned wholly to one split; no random row split.','Test errors not used to tune the model.','No farmer or agronomist validation, no suitability accuracy claim.','RSS includes evaluation libraries, model and data; not device-wide memory.']}
(ROOT/'reports/evaluation.json').write_text(json.dumps(report,indent=2,ensure_ascii=False));print(json.dumps({'f1':{l:{n:v['macro_f1'] for n,v in out[l].items() if isinstance(v,dict) and 'macro_f1' in v} for l in out},'performance':report['performance']},indent=2))
