"""Block Python networking before importing the service, then exercise real cache."""
import socket,sys,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
def denied(*a,**k):raise RuntimeError('Networking disabled for offline demonstration')
socket.socket.connect=denied;socket.socket.connect_ex=denied;socket.create_connection=denied;socket.getaddrinfo=denied
from farmsignal.service import Service
s=Service();scenarios=[dict(text='Can I grow maize here?'),dict(text='کیا میں یہاں مکئی اُگا سکتا ہوں؟'),dict(text='Can I grow maize here?',standing_water=True),dict(text='Can I grow maize here?',dry_soil=True),dict(text='Will it rain tomorrow?'),dict(text='Can I grow maize here?',farm_id='unregistered'),dict(text='Can I grow maize here?',farm_id='outside'),dict(text='I need an agricultural officer',referral_fail=True)]
results=[{'input':x,'response':s.respond(**x,log=False)} for x in scenarios]
(ROOT/'reports/offline-demo.json').write_text(json.dumps({'network_control':'Python socket connect/connect_ex/create_connection/DNS denied before imports; see OS sandbox report for native-code control','scenarios':results},indent=2,ensure_ascii=False))
for r in results:print(r['response']['next_step_reason'],r['response']['message'])
