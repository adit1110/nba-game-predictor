import sys
import os
sys.path.append(os.path.abspath("../scripts"))

from predict import predict_matchup
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # allow frontend on localhost:5173

@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()
    home = data.get("home_team")
    away = data.get("away_team")
    
    if not home or not away:
        return jsonify({"error": "Missing team data"}), 400

    result = predict_matchup(home, away)
    if result is None:
        return jsonify({"error": "Invalid team abbreviation"}), 400

    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True)
