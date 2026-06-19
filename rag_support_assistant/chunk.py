import re
from pathlib import Path

CHUNK_SIZE = 400
CHUNK_OVERLAP = 80  # overlap keeps context at chunk boundaries


def _split_paragraphs(text):
    parts = re.split(r"\n\n+", text.strip())
    return [p.strip() for p in parts if p.strip()]


def _make_chunk_id(source, index):
    stem = Path(source).stem
    return f"{stem}_{index:03d}"


def chunk_markdown(text, source, heading=""):
    paragraphs = _split_paragraphs(text)
    chunks = []
    current = ""
    chunk_index = 0

    for para in paragraphs:
        if len(current) + len(para) + 2 <= CHUNK_SIZE:
            current = f"{current}\n\n{para}".strip() if current else para
            continue

        if current:
            chunks.append({
                "id": _make_chunk_id(source, chunk_index),
                "text": current,
                "source": source,
                "heading": heading,
            })
            chunk_index += 1
            tail = current[-CHUNK_OVERLAP:] if len(current) > CHUNK_OVERLAP else current
            current = f"{tail}\n\n{para}".strip()
        else:
            current = para

        while len(current) > CHUNK_SIZE:
            chunks.append({
                "id": _make_chunk_id(source, chunk_index),
                "text": current[:CHUNK_SIZE],
                "source": source,
                "heading": heading,
            })
            chunk_index += 1
            current = current[CHUNK_SIZE - CHUNK_OVERLAP:]

    if current:
        chunks.append({
            "id": _make_chunk_id(source, chunk_index),
            "text": current,
            "source": source,
            "heading": heading,
        })

    return chunks


def load_and_chunk_corpus(corpus_dir):
    corpus_path = Path(corpus_dir)
    all_chunks = []

    for md_file in sorted(corpus_path.glob("*.md")):
        content = md_file.read_text(encoding="utf-8")
        heading = ""
        body_parts = []

        for line in content.splitlines():
            if line.startswith("# "):
                heading = line[2:].strip()
            else:
                body_parts.append(line)

        body = "\n".join(body_parts)
        file_chunks = chunk_markdown(body, md_file.name, heading)
        all_chunks.extend(file_chunks)

    return all_chunks
