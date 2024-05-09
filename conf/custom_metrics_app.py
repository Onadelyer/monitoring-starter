import random

from fastapi import FastAPI, HTTPException, Response 
from fastapi.middleware.cors import CORSMiddleware
import prometheus_client
import uvicorn

city_coords = [
    {"city": "Tokyo, Japan", "latitude": 35.6895, "longitude": 139.6917, "population": 37.434, "id": 1, "health": 30},
    {"city": "Delhi, India", "latitude": 28.6139, "longitude": 77.2088,"population": 31.181, "id": 2, "health": 10},
    {"city": "Shanghai, China", "latitude": 31.2304, "longitude": 121.4737, "population": 26.415, "id": 3, "health": 30},
    {"city": "São Paulo, Brazil", "latitude": -23.5505, "longitude": -46.6333, "population": 12.3, "id": 4, "health": 10},
    {"city": "Mexico City, Mexico", "latitude": 19.4326, "longitude": -99.1332, "population": 21.8, "id": 5, "health": 30},
    {"city": "New York City, USA", "latitude": 40.7128, "longitude": -74.0059, "population": 8.8, "id": 6, "health": 10},
    {"city": "London, UK", "latitude": 51.5098, "longitude": -0.1180, "population": 8.9, "id": 7, "health": 30},
    {"city": "Paris, France", "latitude": 48.8566, "longitude": 2.3522, "population": 2.165, "id": 8, "health": 10},
    {"city": "Buenos Aires, Argentina", "latitude": -34.8580, "longitude": -56.1771, "population": 15.091, "id": 9, "health": 30},
    {"city": "Cairo, Egypt", "latitude": 30.0444, "longitude": 31.2357, "population": 20.4, "id": 10, "health": 10},
]

datacenter_relations = [
    {"datacenter_id": 1, "source": 1, "target": 3},
    {"datacenter_id": 2, "source": 2, "target": 10},
    {"datacenter_id": 3, "source": 7, "target": 8},
    {"datacenter_id": 4, "source": 5, "target": 6},
    {"datacenter_id": 5, "source": 4, "target": 9}
]

app = FastAPI () 

app.add_middleware( 
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers= ["*"],
)

random_metric1 = prometheus_client.Gauge("random_metric1", "Random metric 1")
random_metric2 = prometheus_client.Gauge("random_metric2", "Random metric 2")
random_metric3 = prometheus_client.Gauge("random_metric3", "Random metric 3")

geoip = prometheus_client.Gauge("geoip_requests", "Number of requests to the GeoIP service", ["id", "Location", "Latitude", "Longitude"])
relations = prometheus_client.Gauge("datacenter_relations", "Number of relations between datacenters", ["datacenter_id", "source", "target"])
population_increase = prometheus_client.Counter("population_increase", "An increasing metric", ["Gender"])

@app.get("/metrics")
async def get_metrics():
    random_metric1.set(float(random.random() * 10) + 1)
    random_metric2.set(float(random.random() * 10) + 1)
    random_metric3.set(float(random.random() * 10) + 1)

    for city in city_coords:
        geoip.labels(
            id=str(city["id"]),
            Location=city["city"],
            Latitude=str(city["latitude"]),
            Longitude=str(city["longitude"]),
        ).set(random.randint(1, 100))

    for relation in datacenter_relations:
        relations.labels(
            datacenter_id=str(relation["datacenter_id"]),
            source=str(relation["source"]),
            target=str(relation["target"])
        ).set(1)

    population_increase.labels(Gender="Female").inc(random.randint(1, 10))
    population_increase.labels(Gender="Male").inc(random.randint(1, 10))

    return Response(
        media_type = "text/plain",
        content = prometheus_client.generate_latest()
    )

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=9101)