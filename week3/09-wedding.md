# 09 — Wedding Planner Team (Module 2 project)

Coordinator + 3 specialists on shared state. Pattern: supervisor with sub-agents
as tools. Draw architecture first — hard part is deciding who knows what.

Architecture:
- `WeddingState(origin, destination, dates, guests, genre)` extends `AgentState`.
- Boss tools: `set_details` (`Command` update), `read_state`, plus
  `flight_expert(origin, destination, dates)`,
  `venue_expert(destination, guests)`, `music_expert(genre)`.
- Specialists: flight (Tavily), venue (Tavily), music (SQLite on course `Chinook.db`).
- Boss rule: set details → read state → call all three with exact values → compile.

Key design lesson (found by failing): sub-agents invoked inside wrapper tools do
NOT inherit the boss's state. State is how the boss tracks; arguments are how
the team talks. v1 (subs reading board themselves) returned empty everywhere.

Smaller lessons:
- Wrapper tools need defaults (`_: str = ""`) — boss calls them empty.
- SQLite schema is capitalized (`Track`, `Artist.Name`) — list schema, don't guess.
- Prompt rule added after watching stalls: "Never ask follow-up questions."
  Prompts accumulate, one observed failure at a time.
- First run caught a real gap: destination is not origin — flights need both.

Live result (DeepSeek `deepseek-chat` via OpenAI-compatible endpoint):
- Flights London→Paris Jun 12 2027: easyJet ~$33, Vueling alt.
- Venue: Domaine de Primard, 80-guest exclusivity + lodging.
- Playlist: 5 rock tracks (AC/DC, Accept) from DB.

Runs on DeepSeek because nested teams multiply model calls per run.
Model = swappable detail: same code ran on Gemini earlier via `init_chat_model`.

Code: `wedding_team.py`. Needs `TAVILY_API_KEY` + `DEEPSEEK_API_KEY` in `.env`.
Transplant mapped: same skeleton → product-launch team (researcher, writer,
pricing checker, same board).
