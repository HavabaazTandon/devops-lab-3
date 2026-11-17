import os
import logging
from flask import Flask, jsonify, render_template_string
from prometheus_client import Counter, generate_latest

app = Flask(__name__)

logging.basicConfig(level=logging.INFO)

REQUEST_COUNT = Counter(
    "app_requests_total",
    "Total application requests",
    ["endpoint"]
)

FEATURE_ENABLED = os.getenv("FEATURE_ENABLED", "true").lower() == "true"

@app.before_request
def track_request():
    from flask import request
    REQUEST_COUNT.labels(endpoint=request.path).inc()
    app.logger.info("Request received: %s", request.path)

@app.route("/")
def home():
    return render_template_string("""
    <h1>DevSecOps Lab 3</h1>
    <h2>Monitoring, Logging and Security</h2>
    <p>Flask application running successfully!</p>
    <p>Feature Flag: {{ status }}</p>
    <a href="/health">Health Check</a><br>
    <a href="/metrics">Metrics</a>
    """, status="ENABLED" if FEATURE_ENABLED else "DISABLED")

@app.route("/health")
def health():
    return jsonify(status="healthy", application="DevSecOps Lab 3")

@app.route("/api/feature")
def feature():
    return jsonify(feature_enabled=FEATURE_ENABLED)

@app.route("/metrics")
def metrics():
    from flask import Response
    return Response(generate_latest(), mimetype="text/plain")

@app.route("/error")
def error():
    app.logger.error("Demonstration error endpoint accessed")
    return jsonify(error="Demonstration error"), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
