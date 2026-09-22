# Setup (do once, ~20 min)

## Rules from "Important, read this before you start"

- Classes go in order. Do not skip Setup.
- LangChain asks: no screenshots of class material outside the platform.
  Posting that you are learning is fine; the lessons stay inside.
- The intro has a Mark complete button at the bottom; pressing it is the
  confirmation.

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
- `.env` is git-ignored. Keys never in chat, notebooks, screenshots, or git.
