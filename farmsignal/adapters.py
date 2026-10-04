from typing import Protocol
class SMSAdapter(Protocol):
 def send(self,recipient:str,message:str)->dict: ...
class Simulator:
 def send(self,recipient,message):return {'status':'simulated','delivered':False,'message':message}
 def refer(self,fail=False):return {'status':'simulated_failed' if fail else 'simulated','delivered':False,'officer_notified':False}
