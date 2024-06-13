import random

from fastapi import FastAPI, HTTPException, Response 
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import prometheus_client
import uvicorn
import re
import json

metrics = [
    {"dc": "cnhe-ash1.edc", "env": "prod", "instance": "54.85.230.153:9100", "ip": "54.85.230.153", "job": "nnie2emon", "org_id": "4639274", "region": "us-east-1", "team": "cnhe", "value": 18.894144},
    {"dc": "cnhe-atl1.edc", "env": "prod", "instance": "54.85.230.153:9100", "ip": "54.85.230.153", "job": "nnie2emon", "org_id": "4639274", "region": "us-east-1", "team": "cnhe", "value": 14.5764},
    {"dc": "cnhe-cdg1.edc", "env": "prod", "instance": "15.188.223.30:9100", "ip": "15.188.223.30", "job": "nnie2emon", "org_id": "4639274", "region": "eu-west-3", "team": "cnhe", "value": 14.501176},
    {"dc": "cnhe-chi1.edc", "env": "prod", "instance": "3.136.6.6:9100", "ip": "3.136.6.6", "job": "nnie2emon", "org_id": "4639274", "region": "us-east-2", "team": "cnhe", "value": 20.161592},
    {"dc": "cnhe-cph1.edc", "env": "prod", "instance": "15.188.223.30:9100", "ip": "15.188.223.30", "job": "nnie2emon", "org_id": "4639274", "region": "eu-west-3", "team": "cnhe", "value": 18.015432},
    {"dc": "cnhe-den1.edc", "env": "prod", "instance": "54.241.60.9:9100", "ip": "54.241.60.9", "job": "nnie2emon", "org_id": "4639274", "region": "us-west-1", "team": "cnhe", "value": 17.366592},
    {"dc": "cnhe-dfw1.edc", "env": "prod", "instance": "54.85.230.153:9100", "ip": "54.85.230.153", "job": "nnie2emon", "org_id": "4639274", "region": "us-east-1", "team": "cnhe", "value": 17.957824},
    {"dc": "cnhe-fra1.edc", "env": "prod", "instance": "52.211.81.150:9100", "ip": "52.211.81.150", "job": "nnie2emon", "org_id": "4639274", "region": "eu-west-1", "team": "cnhe", "value": 17.374056},
    {"dc": "cnhe-lax1-cicd.edc", "env": "prod", "instance": "15.156.21.209:9100", "ip": "15.156.21.209", "job": "nnie2emon", "org_id": "4639274", "region": "ca-central-1", "team": "cnhe", "value": 0},
    {"dc": "cnhe-lax1.edc", "env": "prod", "instance": "54.241.60.9:9100", "ip": "54.241.60.9", "job": "nnie2emon", "org_id": "4639274", "region": "us-west-1", "team": "cnhe", "value": 16.430512},
    {"dc": "cnhe-lon1.edc", "env": "prod", "instance": "15.188.223.30:9100", "ip": "15.188.223.30", "job": "nnie2emon", "org_id": "4639274", "region": "eu-west-3", "team": "cnhe", "value": 21.092928},
    {"dc": "cnhe-mad1.edc", "env": "prod", "instance": "15.188.223.30:9100", "ip": "15.188.223.30", "job": "nnie2emon", "org_id": "4639274", "region": "eu-west-3", "team": "cnhe", "value": 16.719928},
    {"dc": "cnhe-mel1.edc", "env": "prod", "instance": "52.220.222.213:9100", "ip": "52.220.222.213", "job": "nnie2emon", "org_id": "4639274", "region": "ap-southeast-1", "team": "cnhe", "value": 13.664672},
    {"dc": "cnhe-mia1.edc", "env": "prod", "instance": "3.136.6.6:9100", "ip": "3.136.6.6", "job": "nnie2emon", "org_id": "4639274", "region": "us-east-2", "team": "cnhe", "value": 15.893448},
    {"dc": "cnhe-mil1.edc", "env": "prod", "instance": "52.211.81.150:9100", "ip": "52.211.81.150", "job": "nnie2emon", "org_id": "4639274", "region": "eu-west-1", "team": "cnhe", "value": 14.379496},
    {"dc": "cnhe-min1.edc", "env": "prod", "instance": "54.85.230.153:9100", "ip": "54.85.230.153", "job": "nnie2emon", "org_id": "4639274", "region": "us-east-1", "team": "cnhe", "value": 18.42728},
    {"dc": "cnhe-mrs1.edc", "env": "prod", "instance": "52.211.81.150:9100", "ip": "52.211.81.150", "job": "nnie2emon", "org_id": "4639274", "region": "eu-west-1", "team": "cnhe", "value": 15.020696},
    {"dc": "cnhe-nrt2.edc", "env": "prod", "instance": "35.73.247.36:9100", "ip": "35.73.247.36", "job": "nnie2emon", "org_id": "4639274", "region": "ap-northeast-1", "team": "cnhe", "value": 18.642992},
    {"dc": "cnhe-nyc1.edc", "env": "prod", "instance": "3.136.6.6:9100", "ip": "3.136.6.6", "job": "nnie2emon", "org_id": "4639274", "region": "us-east-2", "team": "cnhe", "value": 20.635024},
    {"dc": "cnhe-pao1-cicd.edc", "env": "prod", "instance": "15.156.21.209:9100", "ip": "15.156.21.209", "job": "nnie2emon", "org_id": "4639274", "region": "ca-central-1", "team": "cnhe", "value": 0},
    {"dc": "cnhe-pao1.edc", "env": "prod", "instance": "44.231.169.158:9100", "ip": "44.231.169.158", "job": "nnie2emon", "org_id": "4639274", "region": "us-west-2", "team": "cnhe", "value": 19.051648},
    {"dc": "cnhe-rio1.edc", "env": "prod", "instance": "54.85.230.153:9100", "ip": "54.85.230.153", "job": "nnie2emon", "org_id": "4639274", "region": "us-east-1", "team": "cnhe", "value": 20.030528},
    {"dc": "cnhe-sao1.edc", "env": "prod", "instance": "18.231.229.212:9100", "ip": "18.231.229.212", "job": "nnie2emon", "org_id": "4639274", "region": "sa-east-1", "team": "cnhe", "value": 16.415176},
    {"dc": "cnhe-sin1.edc", "env": "prod", "instance": "52.220.222.213:9100", "ip": "52.220.222.213", "job": "nnie2emon", "org_id": "4639274", "region": "ap-southeast-1", "team": "cnhe", "value": 15.456824},
    {"dc": "cnhe-sto1.edc", "env": "prod", "instance": "52.211.81.150:9100", "ip": "52.211.81.150", "job": "nnie2emon", "org_id": "4639274", "region": "eu-west-1", "team": "cnhe", "value": 17.667136},
    {"dc": "cnhe-syd1.edc", "env": "prod", "instance": "54.206.88.92:9100", "ip": "54.206.88.92", "job": "nnie2emon", "org_id": "4639274", "region": "ap-southeast-2", "team": "cnhe", "value": 18.390616},
    {"dc": "cnhe-yvr1.edc", "env": "prod", "instance": "54.241.60.9:9100", "ip": "54.241.60.9", "job": "nnie2emon", "org_id": "4639274", "region": "us-west-1", "team": "cnhe", "value": 17.609064},
    {"dc": "cnhe-yyz1.edc", "env": "prod", "instance": "54.85.230.153:9100", "ip": "54.85.230.153", "job": "nnie2emon", "org_id": "4639274", "region": "us-east-1", "team": "cnhe", "value": 17.23},
    {"dc": "lab-sjc4-cicd.edc", "env": "dev", "instance": "15.156.21.209:9100", "ip": "15.156.21.209", "job": "nnie2emon", "org_id": "4639274", "region": "ca-central-1", "team": "cnhe", "value": 0}
]

app = FastAPI () 

app.add_middleware( 
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers= ["*"],
)

metricss = prometheus_client.Gauge("test_metrics", "Description", ["dc", "env", "instance", "ip", "job", "org_id", "region", "team"])

@app.get("/metrics")
async def get_metrics():
    for metric in metrics:
        metricss.labels(
            dc=metric["dc"],
            env=metric["env"],
            instance=metric["instance"],
            ip=metric["ip"],
            job=metric["job"],
            org_id=metric["org_id"],
            region=metric["region"],
            team=metric["team"]
        ).set(random.randint(0, 100))

    return Response(
        media_type = "text/plain",
        content = prometheus_client.generate_latest()
    )

def generate_random_numbers(count, min_value=0, max_value=100):
    return [random.randint(min_value, max_value) for _ in range(count)]

def calculate_region_health(dcs_list):
    num_dcs = len(dcs_list)
    num_metrics = len(next(iter(dcs_list.values()))[0])
    
    region_health_array = []
    for i in range(num_metrics):
        avg_value = sum(dcs_list[dc][0][i] for dc in dcs_list) / num_dcs
        region_health_array.append(avg_value)
    
    # Calculate the additional number
    additional_number = sum(dcs_list[dc][1] for dc in dcs_list) / num_dcs
    
    return (region_health_array, additional_number)

@app.get("/testjson")
async def getjson():
    num_metrics = 20
    
    us_west_1_dcs = {
        "ash1.edc": (generate_random_numbers(num_metrics), random.randint(0, 100)),
        "lon1.edc": (generate_random_numbers(num_metrics), random.randint(0, 100))
    }
    us_west_2_dcs = {
        "mad1.edc": (generate_random_numbers(num_metrics), random.randint(0, 100)),
        "mil1.edc": (generate_random_numbers(num_metrics), random.randint(0, 100)),
        "nyc1.edc": (generate_random_numbers(num_metrics), random.randint(0, 100))
    }
    
    data = {
        "us_west_1": {
            "region_health": calculate_region_health(us_west_1_dcs),
            "dcs_list": us_west_1_dcs
        },
        "us_west_2": {
            "region_health": calculate_region_health(us_west_2_dcs),
            "dcs_list": us_west_2_dcs
        }
    }
    
    formatted_data = json.dumps(data, indent=4)
    formatted_data = re.sub(r'\[\s+(\d)', r'[\1', formatted_data)
    formatted_data = re.sub(r',\s+(\d)', r', \1', formatted_data)
    formatted_data = re.sub(r'(\d)\s+\]', r'\1]', formatted_data)
    formatted_data = re.sub(r'(\d)\s+\]', r'\1]', formatted_data)

    return Response(content=formatted_data, media_type="application/json")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=9101)