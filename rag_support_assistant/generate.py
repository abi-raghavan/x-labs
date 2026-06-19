from llm import INSUFFICIENT_CONTEXT, complete


def _build_context_block(contexts):
    blocks = []
    for i, ctx in enumerate(contexts, start=1):
        header = ctx.get("heading") or ctx["source"]
        blocks.append(f"[{i}] Source: {ctx['source']} | Section: {header}\n{ctx['text']}")
    return "\n\n".join(blocks)


def _build_prompt(question, contexts):
    context_text = _build_context_block(contexts)
    return f"""Answer the question using ONLY the context below.

Rules:
- Cite sources using [1], [2], etc. matching the context block numbers.
- If the context does not contain enough information, respond with exactly: {INSUFFICIENT_CONTEXT}
- Do not use outside knowledge.

Context:
{context_text}

Question: {question}

Answer:"""


def _parse_citations(answer, contexts):
    citations = []
    for i, ctx in enumerate(contexts, start=1):
        if f"[{i}]" in answer:
            citations.append({
                "source": ctx["source"],
                "heading": ctx.get("heading", ""),
                "excerpt": ctx["text"][:200],
            })
    return citations


def generate_answer(question, contexts):
    if not contexts:
        return {
            "answer": "I don't have enough information in the documentation to answer that.",
            "citations": [],
            "refused": True,
        }

    prompt = _build_prompt(question, contexts)
    raw = complete(prompt).strip()

    if INSUFFICIENT_CONTEXT in raw:
        return {
            "answer": "I don't have enough information in the documentation to answer that.",
            "citations": [],
            "refused": True,
        }

    return {
        "answer": raw,
        "citations": _parse_citations(raw, contexts),
        "refused": False,
    }


def judge_groundedness(question, answer, contexts):
    context_text = _build_context_block(contexts)
    prompt = f"""Given the context and answer below, list each factual claim in the answer.
For each claim, output one line: CLAIM | SUPPORTED or UNSUPPORTED

Context:
{context_text}

Question: {question}

Answer: {answer}

Claims:"""

    raw = complete(prompt).strip()
    lines = [l.strip() for l in raw.splitlines() if "|" in l]
    if not lines:
        return 1.0, 0

    supported = sum(1 for l in lines if l.upper().endswith("| SUPPORTED"))
    unsupported = sum(1 for l in lines if "UNSUPPORTED" in l.upper())
    total = len(lines)
    groundedness = supported / total if total else 1.0
    return groundedness, unsupported
