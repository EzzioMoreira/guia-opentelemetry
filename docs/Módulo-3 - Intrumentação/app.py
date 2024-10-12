from flask import Flask
import requests
from time import sleep
import random
import logging

app = Flask(__name__)
latency = random.randint(1, 5)

def fetch_data_from_external_service():
    # Simula uma solicitação HTTP GET para um serviço externo
    response = requests.get("http://httpbin.org/get")
    sleep(latency)
    logging.info(f"GET request to httpbin.org returned {response.status_code}")
    return f"GET request to httpbin.org returned {response.status_code}"

def submit_data_to_external_service():
    # Simula uma solicitação HTTP POST para um serviço externo
    response = requests.post("http://httpbin.org/post", json={"key": "value"})
    sleep(latency)
    logging.info(f"POST request to httpbin.org returned {response.status_code}")
    return f"POST request to httpbin.org returned {response.status_code}"

def simulate_error_response():
    # Simula uma solicitação HTTP que retorna um erro
    response = requests.get("http://httpbin.org/status/403")
    sleep(latency)
    logging.error(f"GET request to httpbin.org returned {response.status_code}")
    return f"GET request to httpbin.org returned {response.status_code}"

@app.route("/fetch-data")
def route_fetch_data():
    return fetch_data_from_external_service()

@app.route("/submit-data")
def route_submit_data():
    return submit_data_to_external_service()

@app.route("/simulate-error")
def route_simulate_error():
    return simulate_error_response()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
