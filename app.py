from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/', methods = ["GET"])
def home():
    return jsonify({"message": "Hello from EC2 Flask API!"})

@app.route('/status', methods = ["GET"])
def status():
    return jsonify({"status": "API is running"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=2708)
