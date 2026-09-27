from datetime import date
from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import JSONResponse
from .service import predict_cci, predict_whc, model_metadata

app=FastAPI(title="Sydney Weather Intelligence API",version="1.0.0",description="UTS 36120 AT2 ML as a Service — Student 26019772")

@app.get("/")
def root():
    return {"project":"Sydney Weather Intelligence API","description":"Machine-learning services for CCI and WHC forecasting","version":"1.0.0","student":"Muthu Kumaran Chandrasekar Jayanthi","student_id":"26019772","endpoints":["/","/health","/predict/index/comfort_climate","/predict/category/weather_hazard","/model-metadata","/docs"]}

@app.get("/health")
def health():
    md=model_metadata(); return {"status":"healthy" if len(md)==4 else "degraded","message":"Weather Intelligence API is running","loaded_model_metadata":len(md)}

def validate_date(value: str):
    try: d=date.fromisoformat(value)
    except ValueError: raise HTTPException(status_code=422,detail="date must use YYYY-MM-DD format")
    if d >= date(2026,1,1): raise HTTPException(status_code=422,detail="date must be before 2026-01-01 for this historical demonstration service")
    if d < date(2010,2,1): raise HTTPException(status_code=422,detail="date must be on or after 2010-02-01 so lag/rolling context is available")
    return value

@app.get("/predict/index/comfort_climate")
def comfort_climate(date: str=Query(...,description="Input date YYYY-MM-DD")):
    value=validate_date(date)
    try: pred=predict_cci(value)
    except FileNotFoundError as e: raise HTTPException(status_code=503,detail=str(e))
    except Exception as e: raise HTTPException(status_code=502,detail=f"Prediction service error: {e}")
    return {"input_date":value,"predictions":{"comfort_climate":pred}}

@app.get("/predict/category/weather_hazard")
def weather_hazard(date: str=Query(...,description="Input date YYYY-MM-DD")):
    value=validate_date(date)
    try: pred=predict_whc(value)
    except FileNotFoundError as e: raise HTTPException(status_code=503,detail=str(e))
    except Exception as e: raise HTTPException(status_code=502,detail=f"Prediction service error: {e}")
    return {"input_date":value,"predictions":{"weather_hazard":pred}}

@app.get("/model-metadata")
def metadata(): return model_metadata()
