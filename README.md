# Abi Raghavan | AI Engineering Portfolio

Senior AI Engineer and Data Scientist building production systems across GenAI, RAG, predictive modelling, experimentation, and data platforms.

[GitHub](https://github.com/abi-raghavan) | [LinkedIn](https://www.linkedin.com/in/abiraghavan) | [Email](mailto:abiraghavan@outlook.com)

## Featured projects

### [Agentic Stock Intelligence](https://github.com/abi-raghavan/agentic-stock-intelligence)

Evidence-first, multi-agent research platform for Indian and US equities.

- Orchestrates planning, market research, hybrid RAG, risk analysis, and report verification with LangGraph.
- Combines live prices, fundamentals, and news with BM25 retrieval and cited evidence.
- Handles rate-limited data sources with labelled snapshots and confidence caps instead of hiding stale inputs.
- Ships as a Next.js interface backed by FastAPI, with Docker and free-tier deployment support.

`Python` `LangGraph` `FastAPI` `Next.js` `BM25` `SQLite` `Docker`

### [AIRA](https://github.com/abi-raghavan/aira-core)

Privacy-first Android companion designed for predictable, offline assistance.

- Maps chosen spoken phrases to short, fixed responses using on-device speech processing.
- Keeps speech on the phone, does not save audio, and stores setup securely.
- Separates a safe demo build from the release build that can alert an approved carer.
- Uses deterministic phrase rules rather than an open-ended chatbot for safety and consistency.

`Kotlin` `Android` `On-device speech` `Encrypted storage` `Gradle`

## Applied ML and GenAI labs

### [Experimentation Lab](experimentation_lab/)

An end-to-end A/B testing workflow with deterministic assignment, conversion and revenue analysis, confidence intervals, sample ratio mismatch detection, and sample-size checks.

[Live demo](https://x-lab-argon.streamlit.app/) | `Streamlit` `SciPy` `SQLite` `Plotly`

### [Ride Incentive Recommender](ride_incentive_recommender/)

An explainable scoring application that estimates rider conversion and compares four incentive scenarios against a no-incentive baseline.

[Live demo](https://ride-signal-argon.streamlit.app/) | `scikit-learn` `Pandas` `Streamlit`

### [RAG Support Assistant](rag_support_assistant/)

A grounded support assistant using dense and BM25 retrieval, reciprocal rank fusion, cross-encoder reranking, citations, and an insufficient-context refusal path.

`Python` `FAISS` `sentence-transformers` `Gemini` `Streamlit`

The lab projects use synthetic or sample data. Their metrics describe the implemented evaluation workflows, not production business outcomes.

## Selected professional impact

- Improved a season-level forecasting model by 20-30% over baseline using nine years of data, replacing a 1-2 day manual review with daily automated alerts.
- Led development of a patient analytics platform deployed across more than five countries, using Elasticsearch for sub-second search.
- Migrated a legacy C++ pipeline to PySpark and Databricks, reducing full-project runtime from about one week to 1-4 hours.
- Built an enterprise natural-language analytics assistant covering more than 20 business KPIs with groundedness evaluation.

## Technical focus

- **GenAI:** RAG architecture, agentic workflows, evaluation, embeddings, semantic search, LangChain, LangGraph
- **Machine learning:** forecasting, risk models, ranking, anomaly detection, XGBoost, SHAP
- **Data engineering:** Python, PySpark, SQL, Databricks, Delta Lake, Elasticsearch
- **Production:** FastAPI, Flask, Docker, MLflow, CI/CD, Azure, AWS
- **Statistics:** A/B testing, experiment design, hypothesis testing, uplift modelling

## Run the labs

Each project has its own setup instructions. For the Streamlit applications:

```bash
cd <project_name>
pip install -r requirements.txt
streamlit run app.py
```

The RAG assistant also requires `GEMINI_API_KEY`. See its [project README](rag_support_assistant/README.md).

Run a project's tests with:

```bash
cd <project_name>
pytest tests/ -v
```
