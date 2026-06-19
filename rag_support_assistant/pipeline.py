from pathlib import Path

from embed import get_embedder, load_bm25, load_chunks, load_faiss_index
from generate import generate_answer
from retrieve import retrieve
from sentence_transformers import CrossEncoder

ARTIFACTS_DIR = Path(__file__).parent / "artifacts"
RERANK_MODEL = "cross-encoder/ms-marco-MiniLM-L-6-v2"


def _load_retrieval_stack():
    embedder = get_embedder()
    chunks = load_chunks(ARTIFACTS_DIR)
    faiss_index = load_faiss_index(ARTIFACTS_DIR)
    bm25_index = load_bm25(ARTIFACTS_DIR)
    cross_encoder = CrossEncoder(RERANK_MODEL)
    return embedder, chunks, faiss_index, bm25_index, cross_encoder


def answer(question, retrieval_mode="hybrid_rerank"):
    embedder, chunks, faiss_index, bm25_index, cross_encoder = _load_retrieval_stack()

    contexts = retrieve(
        question,
        retrieval_mode,
        embedder,
        faiss_index,
        bm25_index,
        chunks,
        cross_encoder=cross_encoder,
        top_k=5,
    )

    result = generate_answer(question, contexts)
    result["contexts"] = contexts
    result["retrieval_mode"] = retrieval_mode
    return result
