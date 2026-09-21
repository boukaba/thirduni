# 02 — Tools

Tool = ordinary function + `@tool` decorator + name/description the model reads.
Vague description is a bug — agent ignores the tool. Good description needs no
hint in system prompt.

Loop (printed message by message):
`Human → AI content=[] + tool_calls → ToolMessage → Final`.
Empty content is the act.

Proved:
- `add(21,21)` → 42, loop visible.
- No-tools: "mayor is London Breed" — confident, wrong (training ends mid-2024).
- With Tavily: "Daniel Lurie, sworn Jan 8 2025, 46th mayor", tool call
  `tavily_search(query='current mayor of San Francisco sworn in date')`.
- Tool is for what model can't know: after training, live DB, right now.
- Tracing (LangSmith) optional here; print statements break down once tools multiply.
