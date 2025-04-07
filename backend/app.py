from flask import Flask, request, jsonify
from models.embedder import get_model
from utils.processor import load_assessments, get_descriptions, recommend
import os

app = Flask(__name__)

# Load model and data on startup
model = get_model()
data_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'shl_data.json')
assessments = load_assessments(data_path)
descriptions = get_descriptions(assessments)
data_embeddings = model.encode(descriptions)

@app.route("/recommend", methods=["POST"])
def recommend_assessments():
    data = request.json
    query = data.get("query", "")
    query_embedding = model.encode([query])[0]
    results = recommend(query_embedding, data_embeddings, assessments)
    return jsonify(results)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
