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
GitHub API Repository:
https://github.com/Muthu2125/36120-26SP-AT2-26019772-api

Render API:
https://three6120-26sp-at2-26019772-api.onrender.com

Swagger Documentation:
https://three6120-26sp-at2-26019772-api.onrender.com/docs

Docker Hub:
muthu211007/weather-api-26019772

Docker Tags:
latest
1.0.0

## Related Resources

**Experimentation Repository:**  
https://github.com/Muthu2125/36120-26SP-AT2-26019772-experiments

**TestPyPI Package:**  
https://test.pypi.org/project/uts-aml-weather-26019772/0.1.0/

**Docker Hub:**  
https://hub.docker.com/r/muthu211007/weather-api-26019772

**Render API:**  
https://three6120-26sp-at2-26019772-api.onrender.com

**Swagger Documentation:**  
https://three6120-26sp-at2-26019772-api.onrender.com/docs

## Production Verification

Example input date: `2025-01-01`

Climate Comfort Index endpoint:

- `2025-01-02` → `81.46`
- `2025-01-03` → `76.55`
- `2025-01-04` → `73.57`

Weather Hazard Category endpoint:

- `2025-01-08` → `Moderate Risk`

Invalid date inputs return HTTP `422` instead of causing the API to fail.

## Model Artefacts

The API repository contains the trained production artefacts:

### Climate Comfort
- `models/comfort_climate/cci_h1.joblib`
- `models/comfort_climate/cci_h1.json`
- `models/comfort_climate/cci_h2.joblib`
- `models/comfort_climate/cci_h2.json`
- `models/comfort_climate/cci_h3.joblib`
- `models/comfort_climate/cci_h3.json`

### Weather Hazard
- `models/weather_hazard/whc_h7.joblib`
- `models/weather_hazard/whc_h7.json`

The models can be regenerated using the experimentation repository if required.
