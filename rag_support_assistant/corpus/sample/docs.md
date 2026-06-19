# Product Documentation

## Getting Started

Install with pip install streamlit, then run streamlit run app.py. The app opens at localhost:8501.

## Deployment

Push to GitHub and connect the repo at share.streamlit.io. Pin dependencies in requirements.txt.

## Secrets

Store API keys in .streamlit/secrets.toml locally or in Streamlit Cloud Settings > Secrets. Never commit keys to git.

## Caching

Use @st.cache_data for DataFrames and arrays. Use @st.cache_resource for models and DB connections.

## Session State

Use st.session_state to keep values between reruns. Initialize keys before first use.

## Layout

Use st.columns, st.sidebar, and st.set_page_config(layout="wide") for dashboard layouts.

## File Uploads

Use st.file_uploader and read CSV with pd.read_csv(uploaded_file).

## Charts

Render Plotly charts with st.plotly_chart(fig, use_container_width=True).

## Authentication

Streamlit has no built-in auth. Use st.login, a custom login form, or SSO behind a reverse proxy.

## Performance

Cache expensive work with @st.cache_data and @st.cache_resource. Avoid reloading large files on every rerun.
