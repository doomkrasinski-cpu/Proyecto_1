from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)

# MUY IMPORTANTE: permitir origen "null"
CORS(app, resources={r"/*": {"origins": ["*", "null"]}})

estado = {"led": "off"}
API_KEY = "123ABC"

@app.route("/")
def home():
    return "API ESP32 lista!"

@app.route("/status", methods=["GET"])
def get_status():
    key = request.args.get("key")
    if key != API_KEY:
        return jsonify({"error": "unauthorized"}), 403
    return jsonify(estado)

@app.route("/set", methods=["POST"])
def set_state():
    data = request.json
    if not data:
        return jsonify({"error": "no json"}), 400

    key = data.get("key")
    if key != API_KEY:
        return jsonify({"error": "unauthorized"}), 403

    if "led" in data:
        estado["led"] = data["led"]

    return jsonify({"ok": True, "estado": estado})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
