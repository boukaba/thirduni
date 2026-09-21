# Setup (do once, ~20 min)

Upstream: https://github.com/langchain-ai/lca-lc-foundations

Local (what I ran):
```
git clone --depth 1 https://github.com/langchain-ai/lca-lc-foundations.git
cd lca-lc-foundations
cp example.env .env
uv sync            # Python 3.12.11, 212 packages
```

Free tier: `GOOGLE_API_KEY` at aistudio.google.com/apikey,
`TAVILY_API_KEY` at app.tavily.com. Leave `OPENAI_API_KEY` empty.

Verify:
```
uv run python env_utils.py   # warns OPENAI empty — expected
uv run jupyter lab           # lessons in notebooks/module-1,2,3
```

Lessons learned:
- `langchain-google-genai` already in upstream `pyproject.toml`.
- Notebooks target OpenAI; swap one line to Gemini:
  `init_chat_model(model='gemini-3-flash-preview', model_provider='google_genai')`
- `gemini-2.0-flash` / `2.5-flash` return 404 (retired). Use `gemini-3-flash-preview`.
- Free Gemini quota ~20 req/day/model. Hit `429 RESOURCE_EXHAUSTED`, rotated key.
  Fallback ready: local Ollama (`qwen3:8b`, `llama3`) — no key, private.
- `.env` is git-ignored. Keys never in chat, notebooks, screenshots, or git.
