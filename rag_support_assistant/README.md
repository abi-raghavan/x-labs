# RAG Support Assistant

## Problem

Support teams answer the same product questions repeatedly. Answers live in scattered documentation. Wrong answers create more tickets than they close.

## Approach

Retrieval-augmented generation over a documentation corpus:

1. Chunk markdown docs (400 chars, 80 overlap)
2. Embed with sentence-transformers, store in FAISS + BM25 index
3. Hybrid retrieval: dense + BM25 fused with RRF, then cross-encoder re-rank
4. Generate answers with Gemini (AI Studio free tier), cite source blocks, refuse when context is insufficient

## Impact / Metric

Eval set of 10 in-scope + 2 out-of-scope questions. Run `python evaluate.py` to compare dense-only vs hybrid+re-rank.

**Retrieval (sample corpus, 10 questions):**

| Config | recall@5 | recall@10 |
|--------|----------|-----------|
| dense_only | 1.00 | 1.00 |
| hybrid_rerank | 1.00 | 1.00 |

Sample corpus is small (4 chunks), so both configs hit all gold docs. Add more docs and re-run `python evaluate.py` to see hybrid gains on keyword-heavy queries.

**Generation:** groundedness and hallucination_rate need `GEMINI_API_KEY`. Run `python evaluate.py` after setting the key.

## Tech Stack

Python, sentence-transformers, FAISS, rank-bm25, Google Gemini, Streamlit, pytest

## How to Run

```bash
pip install -r requirements.txt
export GEMINI_API_KEY=your_key   # TODO: get free key at https://aistudio.google.com/apikey
streamlit run app.py
pytest tests/ -v
python evaluate.py
```

To use a different corpus: add `.md` files under `corpus/sample/` (or pass `--corpus-dir`), then run `python ingest.py`.

## Live Demo

TODO

## Setup & Keys

Uses Google AI Studio free tier (`gemini-2.5-flash` by default). No credit card required.

1. Get a free API key at https://aistudio.google.com/apikey
2. Locally: `export GEMINI_API_KEY=your_key`
3. Streamlit Cloud: add to app secrets as `GEMINI_API_KEY = "your_key"`
4. Optional: `export GEMINI_MODEL=gemini-2.5-flash` to swap models on free tier
5. Re-run ingest if you change the corpus: `python ingest.py`
6. Re-run eval to refresh metrics: `python evaluate.py`

Swap LLM provider with `LLM_PROVIDER=gemini|groq|ollama` (Groq needs `GROQ_API_KEY`, Ollama needs local server).

## Design Decisions

- **Hybrid retrieval:** Dense misses exact keyword matches; BM25 misses paraphrases. RRF merges ranks without score tuning.
- **400-char chunks:** Short enough for precise retrieval, long enough to keep a section intact in a single doc file.
- **Cross-encoder re-rank:** Second pass on top-20 candidates; cheap accuracy gain over bi-encoder alone.
- **Refusal path:** Prompt returns `INSUFFICIENT_CONTEXT` when docs do not cover the question.
- **Provider wrapper (`llm.py`):** Swap Gemini/Groq/Ollama without touching retrieval or generation logic.
