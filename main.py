from flask import Flask, request, jsonify
import requests
from flask_cors import CORS

app = Flask(__name__)
CORS(app, origins=["https://terid.github.io"])


@app.route("/routeinfo")
def routeinfo():
    # Force float parsing to avoid string placeholders like "${lat}"
    x = request.args.get("xcoord", type=float)
    y = request.args.get("ycoord", type=float)

    if x is None or y is None:
        return jsonify({"error": "Missing or invalid xcoord or ycoord"}), 400

    # ✅ These are real numbers now
    print(f"📥 Proxy received: x={x}, y={y}")

    url = "https://kytc-api-v100-lts-qrntk7e3ra-uc.a.run.app/api/route/GetRouteInfoByCoordinates"
    params = {
        "xcoord": x,
        "ycoord": y,
        "snap_distance": 250,
        "return_m": "True",
        "input_epsg": "4326",
        "return_multiple": "False",
        "return_format": "geojson",
        "request_id": "100"
    }

    try:
        res = requests.get(url, params=params, timeout=10)
        res.raise_for_status()
        return res.json()
    except requests.RequestException as e:
        print("❌ Proxy request failed:", e)
        return jsonify({"error": str(e)}), 500


@app.route("/")
def home():
    return "✅ KYTC RouteInfo proxy is running. Use /routeinfo with xcoord & ycoord."


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
