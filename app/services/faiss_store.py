import faiss
import numpy as np
from pathlib import Path
from app.config import settings


INDEX_PATH = Path(settings.faiss_index_path)
INDEX_PATH.parent.mkdir(parents=True, exist_ok=True)
DIM = 384




def load_index():
if INDEX_PATH.exists():
index = faiss.read_index(str(INDEX_PATH))
else:
index = faiss.IndexFlatIP(DIM)
return index




def save_index(index):
faiss.write_index(index, str(INDEX_PATH))




def add_vectors(vectors: np.ndarray):
"""Add vectors to the index and return the indices of newly added vectors.
Note: IndexFlatIP doesn't provide persistent ids; we'll use insertion order mapping in SQLite (embedding_index).
"""
index = load_index()
before = index.ntotal
index.add(vectors)
save_index(index)
return list(range(before, before + vectors.shape[0]))




def search_vector(query_vec: np.ndarray, k: int = 8):
index = load_index()
if index.ntotal == 0:
return [], []
D, I = index.search(query_vec, k)
return D.tolist(), I.tolist()