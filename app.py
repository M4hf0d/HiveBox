import sys
from datetime import datetime, timedelta
import requests
from flask import Flask, jsonify

app = Flask(__name__)

API_BASE_URL = "https://api.opensensemap.org/boxes"



@app.route("/version")
def version():
    return "<p>v0.0.1</p>"

@app.route("/temperature", methods=['GET'])
def temperature():
    one_hour_ago = (datetime.utcnow() - timedelta(hours=5)).isoformat() + "Z"
    temps = []
    # Fetch senseBoxes with temperature data within the last hour
    params = {
        "date": one_hour_ago,
        "phenomenon": "temperature",
        "format": "json"
    }
    try:
        print(f"Request URL: {requests.Request('GET', API_BASE_URL, params=params).prepare().url}")
        response = requests.get(API_BASE_URL, params=params, timeout=62)
        response.raise_for_status()
        boxes = response.json()
    except requests.RequestException as e:
        return jsonify({"error": f"Failed to fetch data: {str(e)}"}), 500   
    for box in boxes: 
        for sensor in box['sensors']:
            if sensor['title'] == "Temperatur":
               print(sensor['lastMeasurement']['value'])
               temps.append(float(sensor['lastMeasurement']['value']))

    avg_temp = sum(temps) / len(temps)
    return jsonify({"temperature": avg_temp})          
