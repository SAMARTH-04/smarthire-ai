import json
import numpy as np
from sentence_transformers import SentenceTransformer

from app.models import resume
from app.models import job


model = SentenceTransformer("all-MiniLM-L6-v2")

def generate_embedding(text: str):
    embedding = model.encode(text)
    return embedding.tolist()

def cosine_similarity(vec1, vec2):
    v1 = np.array(json.loads(job.embedding))
    v2 = np.array(json.loads(resume.embedding))
    return float(np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2)))