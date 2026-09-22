# 07 — Context and State

Two ways to carry what isn't in the conversation. Difference is the lesson.

Context: fixed facts, set at start. Schema (dataclass) with defaults, passed to
`create_agent(..., context_schema=...)` and at invoke via `context=...`.
Surprise: agent CANNOT see it — it goes to tool runtime, not the model.
Why: context window is finite precious RAM; framework holds facts out of reach
so agent fetches only the piece it needs via tool call.

State: things learned, mutable. Already used it (message history via checkpointer).
Add fields via `state_schema` (extends `AgentState`), no defaults.
Agent updates itself through a tool returning `Command(update={...})`.
Reading works like context — through tool runtime, same window reason.

Proved on seller domain:
- Fail: `SellerContext(tier, language)`, no tool → "I do not have access..."
  (Bonus bug: omitting `context=` at invoke → `NoneType` — must pass every run.)
- Fix: `get_tier(runtime)` → `standard` default, `pro` on
  `context=SellerContext(seller_tier='pro')`.
- State: told "natural soaps" → state `{'preferred_category': 'natural soaps'}` →
  ask retrieves "You prefer natural soaps."

Sort rule — can it change?
- Context: user_id, tier, staff-vs-customer, language default. Set by you at start.
- State: preferred category, current product. Set by you or agent, any time.

Canonical imports: `from langchain.tools import tool, ToolRuntime`,
`from langgraph.types import Command`, `from langchain.agents import AgentState`.
