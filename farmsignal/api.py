from contextlib import asynccontextmanager
from typing import Literal
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel,Field
from .config import ROOT
from .service import Service
@asynccontextmanager
async def lifespan(app):
 app.state.service=Service();yield
app=FastAPI(title='FarmSignal local SMS simulator',lifespan=lifespan)
app.mount('/static',StaticFiles(directory=ROOT/'static'),name='static')
class Message(BaseModel):
 text:str=Field(min_length=1,max_length=1000)
 farm_id:Literal['demo','unregistered','outside']='demo'
 crop:str|None=Field(default=None,max_length=40)
 standing_water:bool|None=None
 dry_soil:bool|None=None
 referral_fail:bool=False
@app.get('/')
def index():return FileResponse(ROOT/'static/index.html')
@app.get('/health')
def health():return {'status':'ok','mode':'local simulator','sms_delivery':False}
@app.post('/api/message')
def message(m:Message):return app.state.service.respond(**m.model_dump())
