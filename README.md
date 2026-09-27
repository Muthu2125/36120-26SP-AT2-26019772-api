# Sydney Weather Intelligence API

**Student:** Muthu Kumaran Chandrasekar Jayanthi  
**Student ID:** 26019772

FastAPI deployment repository for UTS 36120 AT2.

## Required endpoints
- `GET /`
- `GET /health`
- `GET /predict/index/comfort_climate?date=YYYY-MM-DD`
- `GET /predict/category/weather_hazard?date=YYYY-MM-DD`
- `GET /model-metadata`
- interactive docs at `/docs`

## Before running
Generate the four trained artefacts from the experimentation repository with:
```bash
python scripts/train_models.py
```
Then copy these files **and their matching JSON metadata** into this repository:
```text
models/comfort_climate/cci_h1.joblib
models/comfort_climate/cci_h1.json
models/comfort_climate/cci_h2.joblib
models/comfort_climate/cci_h2.json
models/comfort_climate/cci_h3.joblib
models/comfort_climate/cci_h3.json
models/weather_hazard/whc_h7.joblib
models/weather_hazard/whc_h7.json
```

## Local run
```bash
pip install -r requirements.txt
pytest -q
uvicorn app.main:app --reload --port 10000
```

## Docker
```bash
docker build -t weather-api-26019772 .
docker run -p 10000:10000 weather-api-26019772
```

## Render
Push this repository to private GitHub, connect it to Render, and deploy using the included `render.yaml`/Dockerfile. Keep the service accessible during marking.

## Error handling
Invalid date formats, dates outside the supported historical range, missing model artefacts, and upstream Open-Meteo failures return explicit HTTP errors rather than crashing the service.
