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
- Multi-agent: supervisor + specialists as tools. Wiring proved on math,
  real split proved on seller (keywords → listing). Boss printout hides
  internals — tracing required once layered.
- Middleware: functions inside the loop. Seller doors mapped: human approval
  before publish, regulated-claims classifier after the answer. Decorators
  (`before_model`, `after_model`, `wrap_model_call`) verified present.
- Long conversations: input tokens 20 → 2907 over six turns. Summarization via
  `SummarizationMiddleware` (tuple trigger/keep); trim via `before_agent` hook.
  Two gotchas: deletion needs `RemoveMessage`, and tool exchanges must go as a
  pair (dangling `tool_calls` break OpenAI-compatible APIs).
- HITL: gated `publish_listing` only. Approve, reject-with-note (agent rewrote
  and re-interrupted), edit (ran corrected args, no second ask). Default is
  auto-approve, so gating is opt-in.
- Dynamic agents: `@dynamic_prompt` by language, `@wrap_model_call` tools by
  role (external never sees internal tool), model switch with tokens side by
  side (12 vs 400 output, 373 reasoning). DeepSeek reports the same
  `model_name` for both models now; reasoning tokens are the tell.
- Email assistant capstone: auth-before-inbox via dynamic tool filtering, HITL
  on send. Attack log: skip-auth injection, unauth send, password leak, wrong
  password all held. Forced `tool_choice` injection still hit the interrupt and
  nothing sent. Model judgment is a bonus; the tool-boundary gate is the control.
- Agent Chat UI: capstone put behind a real chat front end. Studio boot gotchas:
  wrap-style middleware must be async in a `.py` file, and no custom checkpointer
  (platform owns persistence). Verified auth + interrupt + approve through the API.
  Shown to an outsider: typed own creds first, clicked through the approval panel
  without noticing the pause, kept expecting the dummy inbox to change.

## Repo layout

```
.env.example            # blanks only — copy to .env and fill locally
week3/
  seller_agent.py       # e-commerce listing agent (Studio-ready)
  setup.md              # setup steps + free-tier keys + model swap
  01-foundations.md     # response object, temp, system prompt
  02-tools.md           # tool loop, Tavily fix
  03-memory.md          # checkpointer + thread_id
  04-multimodal.md      # image Q + injection + frontend guard
  05-chef-to-seller.md  # chef build + domain swap + Studio
  06-mcp.md             # seller_mcp server + time server via uvx
  07-context-state.md   # context vs state, tier vs taste
  08-multi-agent.md       # supervisor + researcher/writer team
  09-wedding.md             # Module 2 project: coordinator + 3 specialists
  10-middleware.md          # middleware intro + my two doors
  11-long-conversations.md  # token growth, summarization, trim proof
  12-hitl.md                # gate one tool: approve, reject, edit
  13-dynamic-agents.md      # prompt/tools/model switched at runtime
  14-email-assistant.md     # capstone + attack log
  15-agent-chat-ui.md       # Studio + Agent Chat UI, async gotcha
  studio/
    agent.py                # Studio-ready email assistant (async middleware)
    langgraph.json          # graph: assistant
  seller_mcp.py         # MCP server: listing_title tool (stdio)
  seller_team.py        # multi-agent: boss + keyword researcher + writer
  wedding_team.py       # Module 2 project: coordinator + flights/venue/music
  long_conversations.py # summarization + trim hook, with 22.5C proof
  hitl.py               # gated publish: approve, reject, edit
  dynamic_agent.py      # prompt by language, tools by role, model by length
  email_assistant.py    # capstone: auth gate + HITL + forced-injection attack rig
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

Week 3 Module 2 done: MCP + context/state + multi-agent + wedding team
(easyJet ~$33, Primard 80-guest, 5 rock tracks; runs on DeepSeek `deepseek-chat`).
Module 3 done: middleware, long conversations, HITL, dynamic agents, email
assistant attacked (forced injection still hit the approval gate), and a real
chat UI on top (Studio + Agent Chat UI).