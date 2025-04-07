from sentence_transformers import SentenceTransformer
import numpy as np

def get_model():
    return SentenceTransformer("all-MiniLM-L6-v2")

def embed_text(model, text):
    embedding = model.encode([text])[0]
    return np.array(embedding)
