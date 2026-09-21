# 05 — Personal Chef → Seller Swap

Chef brief: leftovers in → web recipes out → follow-ups (memory).
Same 4 pieces every time: search tool, system prompt, model+tool+checkpointer, thread_id.

Proved (new key):
- Chef `kitchen-1`, chicken+rice: 2 searches unprompted, fried rice 15 min vs
  casserole 45-50. Follow-up "which faster?" remembered.
- Seller `seller-1`, olive oil soap: SEO keywords
  (Artisan, Cold Process, Vegan, Sensitive Skin) → title + description →
  mobile-short follow-up remembered.

Studio UI (tracing + chat), 3 steps:
1. `.py` with agent (see `seller_agent.py`).
2. `langgraph.json` → `"./seller_agent.py:agent"`, env → `.env`.
3. `uv run langgraph dev` in that dir. Wrong path is the usual failure.

Got wrong: listing too long for mobile, keywords generic pre-search.
Fix next: structured output (title ≤60 chars, desc ≤2 sentences) for clean frontend render.
