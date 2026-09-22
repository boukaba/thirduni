# 01 — Foundational Models

## Module 1 intro (from the opening video)

- Shift from Week 2: there you used agents other people built (Claude Code,
  Cursor, Codex). This module you build one.
- Spectrum of agency: plain chatbot, then tool-using agent, then high-agency
  systems (SRE agents, deep research). Tool calling is what separates chat from
  agent, the same definition Anthropic gave in Week 2, arriving from the other side.
- Course path: model and system prompt -> tools -> short-term memory ->
  multimodal -> chef project.
- Task done: one-sentence build kept small, like the chef. Ours: for independent
  e-commerce sellers, an agent that takes a product and drafts a listing from
  trending SEO keywords, removing 30 minutes of writing per product.

Model = conductor. Answer is an object, not a string: `content` + metadata
(model name, finish reason, token usage). Tokens = bill — cheap model first.

Dials: temperature (randomness), max tokens, timeout, max retries.
Last two matter: calling someone else's service over the internet fails.

Model-agnostic: swap provider by name, key in `.env`. Don't marry a provider.

`create_agent(model, system_prompt)` returns message list — that shape is memory later.
Streaming cuts felt wait, not wait (Daniel's value equation).

Proved:
- `What's the capital of Algeria?` → Algiers, 9 in / 42 out / 51 total.
- Temp 0.0 vs 1.5 on tender-compliance line: strict vs broader.
- System prompt that won (tender, frontend-ready):
  "You are a strict Algerian tender compliance assistant. Only list missing
  documents as bullet points. No extra story. If compliant, say exactly: COMPLIANT."
  Before: paragraph. After: `* Tax certificate / * Technical datasheet` — renders directly.
