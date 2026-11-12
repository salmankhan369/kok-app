import os
try:
    import redis  # type: ignore[import-not-found]
except ImportError:
    redis = None
from flask import Flask, jsonify

app = Flask(__name__)

# ConfigMap se values aayengi
APP_ENV = os.getenv("APP_ENV", "local")
WELCOME_MSG = os.getenv("WELCOME_MSG", "Welcome to KOK-APP!")
REDIS_HOST = os.getenv("REDIS_HOST", "redis-service")

r = redis.Redis(
    host=REDIS_HOST,
    port=6379,
    decode_responses=True,
    socket_connect_timeout=2
) if redis else None

@app.route("/")
def home():
    try:
        hits = r.incr("page_hits")
    except Exception as e:
        hits = f"Redis not connected: {str(e)}"
    return jsonify({
        "app": "kok-app",
        "environment": APP_ENV,
        "message": WELCOME_MSG,
        "visitor_count": hits,
        "pod_name": os.getenv("HOSTNAME", "unknown")
    })

# Liveness Probe endpoint
@app.route("/healthz")
def health():
    return jsonify({"status": "alive"}), 200

# Readiness Probe endpoint
@app.route("/ready")
def ready():
    try:
        r.ping()
        return jsonify({"status": "ready"}), 200
    except Exception:
        return jsonify({"status": "not ready - db down"}), 503

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)