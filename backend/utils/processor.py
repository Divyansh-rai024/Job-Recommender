import json
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

def load_assessments(json_path):
    with open(json_path, "r") as file:
        return json.load(file)

def get_descriptions(assessments):
    return [a['description'] for a in assessments]

def recommend(query_embedding, data_embeddings, assessments, top_k=3):
    similarities = cosine_similarity([query_embedding], data_embeddings)[0]
    top_indices = similarities.argsort()[-top_k:][::-1]
    return [assessments[i] for i in top_indices]
