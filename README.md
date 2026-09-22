# Thirduni — Week 3: Building Agents with LangChain

Systems + product track. Week 2 used other people's agents (Claude Code, Cursor, Codex).
Week 3 builds your own: model → tools → memory → multimodal → shipped project.

Upstream course: `langchain-ai/lca-lc-foundations` (LangChain Academy, with Thirduni).
This repo holds **my working code + notes**. No keys, no screenshots of course material.

## What I proved

- Setup local with `uv`, Python 3.12.11, 212 packages, `env_utils.py` passes.
- Free tier only: Gemini + Tavily. `OPENAI_API_KEY` stays empty.
- Model swap: notebooks target `gpt-5-nano`, I run `gemini-3-flash-preview` via
  `init_chat_model(..., model_provider='google_genai')`. Note: `gemini-2.0-flash`
  and `gemini-2.5-flash` are retired (404) — use `gemini-3-flash-preview`.
- MCP: `seller_mcp` (stdio, 1 tool) + public `mcp-server-time` via `uvx`
  (no key). One prompt → agent called both. Server reusable by any MCP app.
- Tools = what separates chat from agent: function + `@tool` + name/description
  the model reads. Vague description is a bug.
- Loop visible: `Human → AI [] + tool_calls → ToolMessage → Final`.
  Confident-wrong without search (`London Breed`), correct with Tavily
  (`Daniel Lurie, sworn Jan 8 2025`).
- Memory = saved state: `InMemorySaver` + `thread_id`. No checkpointer = forgets.
  New thread = new user. Verified with seller-1 vs seller-2.
- Multimodal = Base64 text channel. Asked corner detail (moon top-right),
  then proved injection (factual ask overridden by smuggled "cat poem").
  Every new input is a new way in — gate frontend uploads.
- Chef → Seller: same 4 pieces (search tool, system prompt, model+tool+checkpointer,
  thread_id). Chef did 2 searches unprompted. Seller drafts SEO listing + mobile
  follow-up with memory.
- Context vs State: context (tier, language) immutable with defaults, visible only
  via tool runtime; state (preferred category) mutable via `Command`, no defaults.
  Sort rule: can it change?

## Repo layout

```
.env.example            # blanks only — copy to .env and fill locally
week3/
  seller_agent.py       # e-commerce listing agent (Studio-ready)
  setup.md              # setup steps + quota + model swap
  01-foundations.md     # response object, temp, system prompt
  02-tools.md           # tool loop, Tavily fix
  03-memory.md          # checkpointer + thread_id
  04-multimodal.md      # image Q + injection + frontend guard
  05-chef-to-seller.md  # chef build + domain swap + Studio
  06-mcp.md             # seller_mcp server + time server via uvx
  07-context-state.md   # context vs state, tier vs taste
  seller_mcp.py         # MCP server: listing_title tool (stdio)
  lounge-posts.md       # community posts as published
```

Upstream clone lives at `lca-lc-foundations/` locally but is git-ignored here
(it has its own git + `.venv` + `.env`).

## Run it

1. `git clone https://github.com/boukaba/thirduni.git && cd thirduni`
2. `cp .env.example .env` — fill `GOOGLE_API_KEY` (aistudio.google.com/apikey,
   free) and `TAVILY_API_KEY` (app.tavily.com, free). Leave OpenAI empty.
3. `uv sync` (or `pip install -r requirements.txt` — see upstream)
4. `uv run python week3/seller_agent.py` — or wire to LangGraph Studio:
   `langgraph.json` → `"./seller_agent.py:agent"`, then `uv run langgraph dev`.

Keys stay in `.env`. Never in chat, notebooks, screenshots, or git.

## Product direction

Course task says keep it small like the chef (30 min, one annoyance).
Thirduni demo needs polished frontend. My lane:

For independent e-commerce sellers: photo of product in → trending SEO keywords
via search → title + 2-sentence listing out. Removes 30 min of writing.
Same shape powers tender compliance (PDF in → missing-docs checklist out).

Week 3 Module 2 in progress: MCP + context/state done, next multi-agent.
