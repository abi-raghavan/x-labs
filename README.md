# x-labs

Applied ML and GenAI labs: experimentation, predictive optimization, and retrieval-augmented generation. Each project is self-contained, with its own README, tests, and Streamlit app.

| Project | Problem | Approach | Stack | Demo |
|---------|---------|----------|-------|------|
| [experimentation_lab](experimentation_lab/) | Ship/no-ship calls on A/B tests without statistical guardrails | Deterministic SHA-256 assignment, two-proportion z-test and Welch t-test, SRM and sample-size checks before lift is reported | Streamlit, SciPy, SQLite, Plotly | [Live](https://x-lab-argon.streamlit.app/) |
| [ride_incentive_recommender](ride_incentive_recommender/) | Over-discounting riders who would book anyway | Logistic regression on rider features, then score four incentive options against a no-incentive baseline | Streamlit, scikit-learn, Pandas | [Live](https://ride-signal-argon.streamlit.app/) |
| [rag_support_assistant](rag_support_assistant/) | Repetitive support questions with answers scattered across docs | Hybrid dense + BM25 retrieval fused with RRF, cross-encoder rerank, cited generation with an insufficient-context refusal path | sentence-transformers, FAISS, Gemini, Streamlit | Not deployed |

All three run on synthetic or sample data. The metrics in each project README describe the implemented evaluation workflow, not production outcomes.

## Run locally

```bash
cd <project_name>
pip install -r requirements.txt
streamlit run app.py
```

`rag_support_assistant` needs `GEMINI_API_KEY` and an ingest step first. See its [README](rag_support_assistant/README.md).

## Test

```bash
cd <project_name>
pytest tests/ -v
```

---

Author: [Abi Raghavan](https://github.com/abi-raghavan)
