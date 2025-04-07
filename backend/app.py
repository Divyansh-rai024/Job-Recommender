from flask import Flask, request, jsonify
from flask_cors import CORS
from models.embedder import get_model
import json

app = Flask(__name__)
CORS(app)

# Load SHL assessment data
with open("shl_data.json", "r") as f:
    data = json.load(f)

# Load Sentence Transformer model
model = get_model()

# Route for homepage
@app.route("/", methods=["GET"])
def home():
    return "✅ SHL Assessment Recommendation Engine is running! Use /recommend with POST requests."

# Recommendation endpoint
@app.route("/recommend", methods=["POST"])
def recommend():
    req_data = request.get_json()
    job_desc = req_data.get("job_description")

    if not job_desc:
        return jsonify({"error": "Missing 'job_description' in request"}), 400

    descriptions = [item["description"] for item in data]
    embeddings = model.encode(descriptions)
    query_embedding = model.encode([job_desc])[0]

    # Calculate cosine similarities
    from sklearn.metrics.pairwise import cosine_similarity
    scores = cosine_similarity([query_embedding], embeddings)[0]
    top_indices = scores.argsort()[-3:][::-1]  # Top 3 matches

    recommendations = [
        {
            "name": data[i]["name"],
            "url": data[i]["url"]
        } for i in top_indices
    ]
    return jsonify(recommendations)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
