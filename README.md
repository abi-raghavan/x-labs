# x-labs

Applied ML/AI portfolio: experimentation, predictive optimization, and production RAG.

| Project | Problem | Approach | Impact Metric | Stack | Live Demo |
|---------|---------|----------|---------------|-------|-----------|
| [experimentation_lab](experimentation_lab/) | Ship/no-ship calls on A/B tests without statistical guardrails | Deterministic assignment, z/t-tests, SRM and sample-size checks | Lift + p-value on primary metric (conversion or revenue) | Streamlit, SQLite, SciPy, Plotly | [Demo](https://x-lab-argon.streamlit.app/) |
| [ride_incentive_recommender](ride_incentive_recommender/) | Over-discounting riders when picking incentives | Logistic regression on rider features; score four incentive scenarios | Expected conversion rate vs no-incentive baseline | Streamlit, scikit-learn | [Demo](https://ride-signal-argon.streamlit.app/) |
| [rag_support_assistant](rag_support_assistant/) | Repetitive support questions with answers buried in docs | Hybrid BM25 + dense retrieval, cross-encoder re-rank, grounded generation with citations | recall@5, groundedness, hallucination rate (see project README) | sentence-transformers, FAISS, Gemini | TODO |

**About:** Senior AI/ML Engineer. Production ML, forecasting, and GenAI/RAG.

## Run locally

```bash
cd <project_name>
pip install -r requirements.txt
streamlit run app.py
```

For `rag_support_assistant`, set `GEMINI_API_KEY` first. See that project's README.

## Test

```bash
cd <project_name>
pytest tests/ -v
```
