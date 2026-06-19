import os

import streamlit as st

from pipeline import answer

st.set_page_config(page_title="RAG Support Assistant", layout="wide")

if "GEMINI_API_KEY" not in os.environ and "GEMINI_API_KEY" in st.secrets:
    os.environ["GEMINI_API_KEY"] = st.secrets["GEMINI_API_KEY"]

st.title("RAG Support Assistant")
st.markdown("Answers grounded in product documentation with citations.")

retrieval_mode = st.sidebar.selectbox(
    "Retrieval mode",
    ["hybrid_rerank", "dense_only"],
    format_func=lambda m: "Hybrid + re-rank" if m == "hybrid_rerank" else "Dense only",
)

st.sidebar.markdown("---")
st.sidebar.markdown("Set `GEMINI_API_KEY` in env or Streamlit secrets.")

question = st.text_input("Ask a support question")

if st.button("Ask") and question:
    with st.spinner("Retrieving and generating..."):
        result = answer(question, retrieval_mode=retrieval_mode)

    if result["refused"]:
        st.warning(result["answer"])
    else:
        st.subheader("Answer")
        st.markdown(result["answer"])

    if result["citations"]:
        st.subheader("Citations")
        for cite in result["citations"]:
            st.markdown(f"**{cite['source']}** - {cite['heading']}")
            st.caption(cite["excerpt"])

    with st.expander("Retrieved context", expanded=False):
        for i, ctx in enumerate(result["contexts"], start=1):
            st.markdown(f"**[{i}] {ctx['source']}** - {ctx.get('heading', '')}")
            st.text(ctx["text"])
