from flask import Flask, request, jsonify
import requests
from flask_cors import CORS

app = Flask(__name__)
CORS(app, origins=["https://terid.github.io"])


@app.route("/routeinfo")
def routeinfo():
    try:
        x = float(request.args.get("xcoord", ""))
        y = float(request.args.get("ycoord", ""))
    except ValueError:
        return jsonify({"error": "Invalid coordinates: xcoord and ycoord must be numeric"}), 400

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
        return jsonify({"error": str(e)}), 502


@app.route("/")
def home():
    return "✅ KYTC RouteInfo proxy is running. Use /routeinfo with xcoord & ycoord."


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
