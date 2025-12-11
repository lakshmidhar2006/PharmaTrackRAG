from sentence_transformers import SentenceTransformer
import numpy as np
from app.config import settings


_model = None


def get_model():
global _model
if _model is None:
_model = SentenceTransformer(settings.embed_model)
return _model




def embed_texts(texts):
model = get_model()
embs = model.encode(texts, convert_to_numpy=True)
# normalize to unit length (for IP index after L2 normalization equivalence)
norms = np.linalg.norm(embs, axis=1, keepdims=True)
norms[norms == 0] = 1.0
embs = embs / norms
return embs.astype("float32")