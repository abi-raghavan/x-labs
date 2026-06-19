import json
import pickle
from pathlib import Path

import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

EMBED_MODEL = "all-MiniLM-L6-v2"  # fast CPU baseline for short technical text


def get_embedder():
    return SentenceTransformer(EMBED_MODEL)


def encode_texts(embedder, texts):
    vectors = embedder.encode(texts, normalize_embeddings=True)
    return np.array(vectors, dtype="float32")


def build_faiss_index(vectors):
    dim = vectors.shape[1]
    index = faiss.IndexFlatIP(dim)  # cosine via normalized vectors + inner product
    index.add(vectors)
    return index


def save_artifacts(chunks, vectors, bm25_index, artifacts_dir):
    artifacts_path = Path(artifacts_dir)
    artifacts_path.mkdir(parents=True, exist_ok=True)

    faiss_index = build_faiss_index(vectors)
    faiss.write_index(faiss_index, str(artifacts_path / "faiss.index"))

    with open(artifacts_path / "chunks.json", "w", encoding="utf-8") as f:
        json.dump(chunks, f, indent=2)

    with open(artifacts_path / "bm25.pkl", "wb") as f:
        pickle.dump(bm25_index, f)


def load_chunks(artifacts_dir):
    path = Path(artifacts_dir) / "chunks.json"
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def load_faiss_index(artifacts_dir):
    path = Path(artifacts_dir) / "faiss.index"
    return faiss.read_index(str(path))


def load_bm25(artifacts_dir):
    path = Path(artifacts_dir) / "bm25.pkl"
    with open(path, "rb") as f:
        return pickle.load(f)
