from __future__ import annotations
from pathlib import Path
import json, joblib, requests, pandas as pd, numpy as np

ROOT=Path(__file__).resolve().parents[1]
ARCHIVE_URL="https://archive-api.open-meteo.com/v1/archive"
BASE=["temperature_2m","relative_humidity_2m","precipitation","cloud_cover","wind_speed_10m","wind_gusts_10m","snowfall"]

def _load(name):
    path=ROOT/name
    if not path.exists(): raise FileNotFoundError(f"Missing model artefact: {path.name}. Run experiments training and copy models into API/models.")
    model=joblib.load(path); meta=json.loads(path.with_suffix('.json').read_text()); return model,meta

def _fetch_context(input_date: str):
    end=pd.Timestamp(input_date)
    if end >= pd.Timestamp('2026-01-01'):
        raise ValueError("Dates from 2026 onward are reserved as production data and are not accepted by this historical demonstration endpoint.")
    start=end-pd.Timedelta(days=30)
    params={"latitude":-33.8688,"longitude":151.2093,"start_date":start.strftime('%Y-%m-%d'),"end_date":end.strftime('%Y-%m-%d'),"hourly":','.join(BASE),"timezone":"Australia/Sydney"}
    r=requests.get(ARCHIVE_URL,params=params,timeout=90); r.raise_for_status(); p=r.json()
    df=pd.DataFrame(p['hourly']); df['time']=pd.to_datetime(df['time']); df['date']=df['time'].dt.floor('D')
    d=df.groupby('date',as_index=False).agg(temperature_2m=('temperature_2m','mean'),relative_humidity_2m=('relative_humidity_2m','mean'),wind_speed_10m=('wind_speed_10m','mean'),wind_gusts_10m=('wind_gusts_10m','max'),cloud_cover=('cloud_cover','mean'),precipitation=('precipitation','sum'),snowfall=('snowfall','sum')).sort_values('date')
    # current-day target indices used only as historical lag features, not future target leakage
    t=np.maximum(0,1-np.abs(d.temperature_2m-22)/20); h=np.maximum(0,1-np.abs(d.relative_humidity_2m-50)/50); w=np.maximum(0,1-np.abs(d.wind_speed_10m-10)/40); c=np.maximum(0,1-d.cloud_cover/100); rr=np.maximum(0,1-d.precipitation/20)
    d['CCI']=100*(.35*t+.20*h+.15*w+.15*c+.15*rr)
    rh=np.minimum(d.precipitation/30,1); wh=np.minimum(d.wind_gusts_10m/100,1); ch=np.minimum(d.cloud_cover/100,1); sh=np.minimum(d.snowfall/15,1); th=np.minimum(np.abs(d.temperature_2m-22)/25,1)
    d['WHI']=100*(.30*rh+.30*wh+.20*ch+.10*sh+.10*th)
    dt=pd.to_datetime(d.date); d['month']=dt.dt.month; d['day_of_year']=dt.dt.dayofyear; d['doy_sin']=np.sin(2*np.pi*d.day_of_year/365.25); d['doy_cos']=np.cos(2*np.pi*d.day_of_year/365.25)
    for col in BASE+['CCI','WHI']:
        for lag in (1,2,3,7,14): d[f'{col}_lag_{lag}']=d[col].shift(lag)
    for col in BASE:
        for win in (3,7,14):
            s=d[col].shift(1).rolling(win,min_periods=win); d[f'{col}_rollmean_{win}']=s.mean(); d[f'{col}_rollstd_{win}']=s.std()
    return d.iloc[[-1]]

def predict_cci(input_date: str):
    row=_fetch_context(input_date); out={}
    for h in (1,2,3):
        model,meta=_load(f'models/comfort_climate/cci_h{h}.joblib')
        val=float(model.predict(row[meta['features']])[0]); out[(pd.Timestamp(input_date)+pd.Timedelta(days=h)).strftime('%Y-%m-%d')]=round(max(0,min(100,val)),2)
    return out

def predict_whc(input_date: str):
    row=_fetch_context(input_date); model,meta=_load('models/weather_hazard/whc_h7.joblib')
    cls=int(model.predict(row[meta['features']])[0]); labels={0:'Low Risk',1:'Moderate Risk',2:'High Risk',3:'Extreme Risk'}
    return {(pd.Timestamp(input_date)+pd.Timedelta(days=7)).strftime('%Y-%m-%d'):labels[cls]}

def model_metadata():
    items=[]
    for rel in [f'models/comfort_climate/cci_h{i}.joblib' for i in (1,2,3)]+['models/weather_hazard/whc_h7.joblib']:
        p=ROOT/rel
        if p.with_suffix('.json').exists(): items.append(json.loads(p.with_suffix('.json').read_text()))
    return items
