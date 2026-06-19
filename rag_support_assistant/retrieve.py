import numpy as np
from rank_bm25 import BM25Okapi
from sentence_transformers import CrossEncoder

RERANK_MODEL = "cross-encoder/ms-marco-MiniLM-L-6-v2"  # cheap precision boost on top-20
RRF_K = 60  # RRF constant; avoids tuning BM25 vs cosine score scales


def build_bm25(chunks):
    tokenized = [c["text"].lower().split() for c in chunks]
    return BM25Okapi(tokenized)


def reciprocal_rank_fusion(rank_lists, k=RRF_K):
    scores = {}
    for ranked_ids in rank_lists:
        for rank, chunk_id in enumerate(ranked_ids):
            scores[chunk_id] = scores.get(chunk_id, 0.0) + 1.0 / (k + rank + 1)
    return sorted(scores.keys(), key=lambda cid: scores[cid], reverse=True)


def dense_search(query, embedder, faiss_index, chunks, top_k):
    query_vec = embedder.encode([query], normalize_embeddings=True).astype("float32")
    _, indices = faiss_index.search(query_vec, top_k)
    return [chunks[i]["id"] for i in indices[0]]


def bm25_search(query, bm25_index, chunks, top_k):
    scores = bm25_index.get_scores(query.lower().split())
    ranked = np.argsort(scores)[::-1][:top_k]
    return [chunks[i]["id"] for i in ranked]


def rerank(query, chunk_ids, chunks, cross_encoder, top_k):
    id_to_chunk = {c["id"]: c for c in chunks}
    pairs = [(query, id_to_chunk[cid]["text"]) for cid in chunk_ids if cid in id_to_chunk]
    ids = [cid for cid in chunk_ids if cid in id_to_chunk]
    if not pairs:
        return []

    scores = cross_encoder.predict(pairs)
    ranked = sorted(zip(ids, scores), key=lambda x: x[1], reverse=True)
    return [cid for cid, _ in ranked[:top_k]]


def retrieve(query, mode, embedder, faiss_index, bm25_index, chunks, cross_encoder=None, top_k=5):
    if mode == "dense_only":
        ranked_ids = dense_search(query, embedder, faiss_index, chunks, top_k)
    elif mode == "hybrid_rerank":
        dense_ids = dense_search(query, embedder, faiss_index, chunks, 20)
        sparse_ids = bm25_search(query, bm25_index, chunks, 20)
        fused = reciprocal_rank_fusion([dense_ids, sparse_ids])
        ranked_ids = rerank(query, fused, chunks, cross_encoder, top_k)
    else:
        raise ValueError(f"Unknown retrieval mode: {mode}")

    id_to_chunk = {c["id"]: c for c in chunks}
    return [id_to_chunk[cid] for cid in ranked_ids if cid in id_to_chunk]


def recall_at_k(retrieved_ids, gold_ids, k):
    top_k = set(retrieved_ids[:k])
    return any(gid in top_k for gid in gold_ids)
