from flask import Flask, jsonify, request
from datetime import datetime
import uuid

app = Flask(__name__)


def add_cors(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, PATCH, DELETE, OPTIONS"
    return response

app.after_request(add_cors)


devices = [
    {"id": "dev-001", "name": "Den phong khach", "type": "light", "status": "on", "floor": 1, "unit": "A101", "created_at": "2024-01-15T08:00:00"},
    {"id": "dev-002", "name": "Dieu hoa phong ngu", "type": "air_conditioner", "status": "off", "floor": 2, "unit": "B205", "created_at": "2024-01-15T08:05:00"},
    {"id": "dev-003", "name": "Camera hanh lang", "type": "camera", "status": "on", "floor": 3, "unit": "common", "created_at": "2024-01-15T08:10:00"},
    {"id": "dev-004", "name": "Den hanh lang tang 2", "type": "light", "status": "off", "floor": 2, "unit": "common", "created_at": "2024-01-15T08:15:00"},
    {"id": "dev-005", "name": "Dieu hoa phong khach", "type": "air_conditioner", "status": "on", "floor": 3, "unit": "C301", "created_at": "2024-01-15T08:20:00"},
]


@app.route("/")
def home():
    return jsonify({"message": "Smart Apartment API", "version": "1.0.0"})


@app.route("/health")
def health():
    return jsonify({"status": "healthy", "timestamp": datetime.now().isoformat()})


@app.route("/devices", methods=["GET", "OPTIONS"])
def get_devices():
    if request.method == "OPTIONS":
        return jsonify({}), 200

    result = list(devices)
    device_type = request.args.get("type")
    floor = request.args.get("floor")
    status = request.args.get("status")

    if device_type:
        result = [d for d in result if d["type"] == device_type]
    if floor:
        result = [d for d in result if str(d["floor"]) == floor]
    if status:
        result = [d for d in result if d["status"] == status]

    return jsonify({"total": len(result), "devices": result}), 200


@app.route("/devices", methods=["POST"])
def add_device():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Missing request body"}), 400

    required = ["name", "type", "floor", "unit"]
    missing = [f for f in required if f not in data]
    if missing:
        return jsonify({"error": f"Missing fields: {missing}"}), 400

    device = {
        "id": f"dev-{str(uuid.uuid4())[:8]}",
        "name": data["name"],
        "type": data["type"],
        "status": data.get("status", "off"),
        "floor": data["floor"],
        "unit": data["unit"],
        "created_at": datetime.now().isoformat()
    }
    devices.append(device)
    return jsonify(device), 201


@app.route("/devices/<device_id>", methods=["PATCH", "OPTIONS"])
def update_device(device_id):
    if request.method == "OPTIONS":
        return jsonify({}), 200

    device = next((d for d in devices if d["id"] == device_id), None)
    if not device:
        return jsonify({"error": "Device not found"}), 404

    data = request.get_json()
    if not data:
        return jsonify({"error": "Missing request body"}), 400

    if "status" in data:
        if data["status"] not in ("on", "off"):
            return jsonify({"error": "status must be 'on' or 'off'"}), 400
        device["status"] = data["status"]

    if "name" in data:
        device["name"] = data["name"]

    return jsonify(device), 200


@app.route("/devices/<device_id>", methods=["DELETE", "OPTIONS"])
def delete_device(device_id):
    if request.method == "OPTIONS":
        return jsonify({}), 200

    global devices
    device = next((d for d in devices if d["id"] == device_id), None)
    if not device:
        return jsonify({"error": "Device not found"}), 404

    devices = [d for d in devices if d["id"] != device_id]
    return jsonify({"deleted": device_id}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
