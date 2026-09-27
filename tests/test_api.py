from fastapi.testclient import TestClient
from app.main import app
client=TestClient(app)

def test_root(): assert client.get('/').status_code==200
def test_health(): assert client.get('/health').status_code==200
def test_bad_date(): assert client.get('/predict/index/comfort_climate',params={'date':'bad'}).status_code==422
def test_2026_rejected(): assert client.get('/predict/category/weather_hazard',params={'date':'2026-01-01'}).status_code==422
