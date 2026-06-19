import os

INSUFFICIENT_CONTEXT = "INSUFFICIENT_CONTEXT"


def complete(prompt):
    provider = os.environ.get("LLM_PROVIDER", "gemini")

    if provider == "gemini":
        return _complete_gemini(prompt)
    if provider == "groq":
        return _complete_groq(prompt)
    if provider == "ollama":
        return _complete_ollama(prompt)

    raise ValueError(f"Unknown LLM provider: {provider}")


def _complete_gemini(prompt):
    import google.generativeai as genai

    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY not set")  # TODO: free key at https://aistudio.google.com/apikey

    # gemini-2.5-flash: AI Studio free tier, no billing required
    model_name = os.environ.get("GEMINI_MODEL", "gemini-2.5-flash")

    genai.configure(api_key=api_key)
    model = genai.GenerativeModel(model_name)
    response = model.generate_content(prompt)
    return response.text


def _complete_groq(prompt):
    from groq import Groq

    client = Groq(api_key=os.environ["GROQ_API_KEY"])
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
    )
    return response.choices[0].message.content


def _complete_ollama(prompt):
    import requests

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={"model": "llama3", "prompt": prompt, "stream": False},
    )
    response.raise_for_status()
    return response.json()["response"]
