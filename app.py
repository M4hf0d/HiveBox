import os
import sys
from datetime import datetime, timedelta
import requests
from flask import Flask, jsonify
from prometheus_client import Counter, generate_latest, REGISTRY


# Prometheus metrics
REQUEST_COUNT = Counter('hivebox_requests_total', 'Total number of requests', ['endpoint'])

# Configurable senseBox IDs via env vars (default to example IDs)
SENSEBOX_IDS = os.getenv('SENSEBOX_IDS')


app = Flask(__name__)

API_BASE_URL = "https://api.opensensemap.org/boxes"


@app.route("/version")
def version():
    REQUEST_COUNT.labels(endpoint='/version').inc()
    return "<p>v0.0.3</p>"


@app.route("/metrics")
def get_metrics():
    REQUEST_COUNT.labels(endpoint='/metrics').inc()
    return generate_latest(REGISTRY), 200, {'Content-Type': 'text/plain; version=0.0.4; charset=utf-8'}


@app.route("/temperature", methods=["GET"])
def temperature():
    REQUEST_COUNT.labels(endpoint='/temperature').inc()
    one_hour_ago = (datetime.utcnow() - timedelta(hours=5)).isoformat() + "Z"
    temps = []
    # Fetch senseBoxes with temperature data within the last hour
    params = {"date": one_hour_ago, "phenomenon": "temperature", "format": "json"}
    try:
        print(
            f"Request URL: {requests.Request('GET', API_BASE_URL, params=params).prepare().url}"
        )
        response = requests.get(API_BASE_URL, params=params, timeout=62)
        response.raise_for_status()
        boxes = response.json()
    except requests.RequestException as e:
        return jsonify({"error": f"Failed to fetch data: {str(e)}"}), 500
    # Append temperature data for each box into list
    for box in boxes:
        for sensor in box["sensors"]:
            if sensor["title"] == "Temperatur":
                temps.append(float(sensor["lastMeasurement"]["value"]))


    if not temps:
        return {"error": "No valid temperature data found in the last hour"}, 404

    avg_temp = sum(temps) / len(temps)
    if avg_temp < 10:
        status = "Too Cold"
    elif 11 <= avg_temp <= 36:
        status = "Good"
    else:
        status = "Too Hot"
    return {"average_temperature": avg_temp, "unit": "°C", "count": len(temps), "status": status}
