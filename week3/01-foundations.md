# 01 — Foundational Models

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
