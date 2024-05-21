from flask import Flask, jsonify
import requests
from prometheus_client import Gauge, generate_latest, CollectorRegistry, exposition

app = Flask(__name__)

# Define Prometheus metrics registry and gauge
registry = CollectorRegistry()
datacenter_pairs_gauge = Gauge('datacenter_pairs', 'Datacenter Pairs Metrics', [
    'datacenter_id', 'source_location', 'target_location', 'source_health', 'target_health', 'average_health'], registry=registry)

PROMETHEUS_URL = 'http://prometheus-server:9090/api/v1/query'


def fetch_prometheus_data(query):
    response = requests.get(PROMETHEUS_URL, params={'query': query})
    return response.json()['data']['result']


def get_geoip_requests():
    return fetch_prometheus_data('geoip_requests')


def get_datacenter_relations():
    return fetch_prometheus_data('datacenter_relations')


def process_metrics():
    geoip_requests = get_geoip_requests()
    datacenter_relations = get_datacenter_relations()

    geoip_dict = {}
    for result in geoip_requests:
        metric = result['metric']
        value = float(result['value'][1])
        geoip_dict[metric['id']] = {
            'location': metric['Location'],
            'health': value
        }

    datacenter_pairs = []
    for relation in datacenter_relations:
        metric = relation['metric']
        source_id = metric['source']
        target_id = metric['target']

        source = geoip_dict.get(source_id, {'location': 'unknown', 'health': 0})
        target = geoip_dict.get(target_id, {'location': 'unknown', 'health': 0})

        average_health = (source['value'] + target['value']) / 2

        datacenter_pairs.append({
            'datacenter_id': metric['datacenter_id'],
            'source_location': source['location'],
            'target_location': target['location'],
            'source_health': source['health'],
            'target_health': target['health'],
            'average_health': average_health
        })

        datacenter_pairs_gauge.labels(
            datacenter_id=metric['datacenter_id'],
            source_location=source['location'],
            target_location=target['location'],
            source_health=source['health'],
            target_health=target['health'],
            average_health=average_health
        ).set(average_health)


@app.route('/metrics')
def metrics():
    process_metrics()
    return exposition.generate_latest(registry), 200, {'Content-Type': 'text/plain; charset=utf-8'}


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
