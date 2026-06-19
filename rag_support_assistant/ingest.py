import argparse
from pathlib import Path

from chunk import load_and_chunk_corpus
from embed import encode_texts, get_embedder, save_artifacts
from retrieve import build_bm25

DEFAULT_CORPUS = Path(__file__).parent / "corpus" / "sample"
DEFAULT_ARTIFACTS = Path(__file__).parent / "artifacts"


def ingest(corpus_dir, artifacts_dir):
    chunks = load_and_chunk_corpus(corpus_dir)
    embedder = get_embedder()
    texts = [c["text"] for c in chunks]
    vectors = encode_texts(embedder, texts)
    bm25_index = build_bm25(chunks)
    save_artifacts(chunks, vectors, bm25_index, artifacts_dir)
    print(f"Ingested {len(chunks)} chunks from {corpus_dir} -> {artifacts_dir}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--corpus-dir", default=str(DEFAULT_CORPUS))
    parser.add_argument("--artifacts-dir", default=str(DEFAULT_ARTIFACTS))
    args = parser.parse_args()
    # TODO: point --corpus-dir at a larger doc set when swapping corpora
    ingest(args.corpus_dir, args.artifacts_dir)
