import json
import os
import time
from pathlib import Path

import llm  # loads .env
from embed import get_embedder, load_bm25, load_chunks, load_faiss_index
from generate import generate_answer, judge_groundedness
from retrieve import dense_search, recall_at_k, retrieve
from sentence_transformers import CrossEncoder

ARTIFACTS_DIR = Path(__file__).parent / "artifacts"
EVAL_PATH = Path(__file__).parent / "eval" / "eval_set.json"
RERANK_MODEL = "cross-encoder/ms-marco-MiniLM-L-6-v2"


def _load_stack():
    embedder = get_embedder()
    chunks = load_chunks(ARTIFACTS_DIR)
    faiss_index = load_faiss_index(ARTIFACTS_DIR)
    bm25_index = load_bm25(ARTIFACTS_DIR)
    cross_encoder = CrossEncoder(RERANK_MODEL)
    return embedder, chunks, faiss_index, bm25_index, cross_encoder


def _retrieval_ids(query, mode, embedder, faiss_index, bm25_index, chunks, cross_encoder, top_k=10):
    if mode == "dense_only":
        return dense_search(query, embedder, faiss_index, chunks, top_k)
    return [c["id"] for c in retrieve(
        query, "hybrid_rerank", embedder, faiss_index, bm25_index, chunks,
        cross_encoder=cross_encoder, top_k=top_k,
    )]


def evaluate_config(eval_rows, mode, embedder, chunks, faiss_index, bm25_index, cross_encoder, run_generation=False):
    recall_5 = []
    recall_10 = []
    groundedness_scores = []
    hallucination_flags = []

    for row in eval_rows:
        query = row["question"]
        gold_ids = row["gold_chunk_ids"]
        expect_refusal = row.get("expect_refusal", False)

        retrieved_ids = _retrieval_ids(
            query, mode, embedder, faiss_index, bm25_index, chunks, cross_encoder, top_k=10,
        )

        if gold_ids:
            recall_5.append(recall_at_k(retrieved_ids, gold_ids, 5))
            recall_10.append(recall_at_k(retrieved_ids, gold_ids, 10))

        if not run_generation:
            continue

        contexts = [c for c in chunks if c["id"] in retrieved_ids[:5]]
        gen = generate_answer(query, contexts)
        time.sleep(13)  # free tier: 5 req/min on gemini-2.5-flash

        if expect_refusal:
            hallucination_flags.append(0 if gen["refused"] else 1)
            continue

        if gen["refused"]:
            hallucination_flags.append(1)
            groundedness_scores.append(0.0)
            continue

        g_score, unsupported = judge_groundedness(query, gen["answer"], contexts)
        time.sleep(13)
        groundedness_scores.append(g_score)
        hallucination_flags.append(1 if unsupported > 0 else 0)

    out = {
        "recall@5": sum(recall_5) / len(recall_5) if recall_5 else None,
        "recall@10": sum(recall_10) / len(recall_10) if recall_10 else None,
    }
    if groundedness_scores:
        out["groundedness"] = sum(groundedness_scores) / len(groundedness_scores)
        out["hallucination_rate"] = sum(hallucination_flags) / len(hallucination_flags)
    else:
        out["groundedness"] = None
        out["hallucination_rate"] = None
    return out


def main():
    # TODO: set GEMINI_API_KEY before running generation metrics
    with open(EVAL_PATH, encoding="utf-8") as f:
        eval_rows = json.load(f)

    embedder, chunks, faiss_index, bm25_index, cross_encoder = _load_stack()
    run_gen = bool(os.environ.get("GEMINI_API_KEY"))

    results = {}
    for mode in ["dense_only", "hybrid_rerank"]:
        results[mode] = evaluate_config(
            eval_rows, mode, embedder, chunks, faiss_index, bm25_index, cross_encoder,
            run_generation=run_gen,
        )

    print("\n| Config | recall@5 | recall@10 | groundedness | hallucination_rate |")
    print("|--------|----------|-----------|--------------|-------------------|")
    for mode, m in results.items():
        r5 = f"{m['recall@5']:.2f}" if m["recall@5"] is not None else "N/A"
        r10 = f"{m['recall@10']:.2f}" if m["recall@10"] is not None else "N/A"
        g = f"{m['groundedness']:.2f}" if m["groundedness"] is not None else "N/A (set GEMINI_API_KEY)"
        h = f"{m['hallucination_rate']:.2f}" if m["hallucination_rate"] is not None else "N/A (set GEMINI_API_KEY)"
        print(f"| {mode} | {r5} | {r10} | {g} | {h} |")


if __name__ == "__main__":
    main()
