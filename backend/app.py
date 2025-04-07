from flask import Flask, request, jsonify
from models.embedder import get_model, embed_text
import json
import os

app = Flask(__name__)
model = get_model()

# Load SHL data
with open("shl_data.json", "r") as f:
    shl_data = json.load(f)

# ✅ Root route for browser check
@app.route("/", methods=["GET"])
def home():
    return "✅ SHL Assessment Recommendation Engine is running! Use POST /recommend with a job description."

# ✅ Main recommendation route
@app.route("/recommend", methods=["POST"])
def recommend():
    data = request.get_json()
    job_description = data.get("job_description", "")
    
    if not job_description:
        return jsonify({"error": "Missing job_description"}), 400

    query_embedding = embed_text(model, job_description)

    recommendations = []
    for item in shl_data:
        assessment_embedding = embed_text(model, item["description"])
        similarity = query_embedding @ assessment_embedding
        recommendations.append((similarity, item["name"], item["url"]))

    recommendations.sort(reverse=True)
    top_recommendations = [{"name": name, "url": url} for _, name, url in recommendations[:3]]

    return jsonify(top_recommendations)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=False, host="0.0.0.0", port=port)
