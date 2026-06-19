from chunk import chunk_markdown


def test_chunk_markdown_short_text():
    # fixtures
    text = "First paragraph about Streamlit.\n\nSecond paragraph about widgets."
    expected = [
        {
            "id": "doc_000",
            "text": "First paragraph about Streamlit.\n\nSecond paragraph about widgets.",
            "source": "doc.md",
            "heading": "Intro",
        }
    ]

    # run
    result = chunk_markdown(text, "doc.md", "Intro")

    # assert
    assert result == expected


def test_chunk_markdown_splits_long_paragraph():
    # fixtures
    text = "A" * 500
    expected = [
        {
            "id": "long_000",
            "text": "A" * 400,
            "source": "long.md",
            "heading": "",
        },
        {
            "id": "long_001",
            "text": "A" * 180,
            "source": "long.md",
            "heading": "",
        },
    ]

    # run
    result = chunk_markdown(text, "long.md", "")

    # assert
    assert result == expected
