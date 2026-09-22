# 08 — Multi-Agent (supervisor + sub-agents)

One agent doing everything fills the finite window and drops quality.
Fix: supervisor delegates to specialists. In LangChain a sub-agent is just
a tool — wrap each specialist in a `@tool` function, hand them to the boss.
Tool calling the whole way down; name/description quality matters as much here.

Proved:
- Wiring (toy): boss → `square_agent(9)` → 81 → `root_agent(81)` → 9.
- Real split: boss → `keyword_expert` → 5 keywords
  (Organic, Artisan, Sensitive Skin, Vegan, Castile) → `listing_writer` →
  finished listing for "handmade olive oil soap".
- Boss printout carries only final outputs. Researcher searches and writer
  drafts are invisible without tracing — top layer says all fine.
  Tracing stops being optional once the system has layers.

Seller split design:
- Researcher: holds Tavily tool, "5 keywords only".
- Writer: no tools, "2-sentence description from keywords".
- Boss rule: keywords first, then writer, reply final listing only.

Code: `seller_team.py`. Run needs `TAVILY_API_KEY` + `GOOGLE_API_KEY` in `.env`.
