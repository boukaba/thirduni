# 04 — Multimodal

File → Base64 → text channel. Same encoding as Karpathy's stop-sign bypass —
once attack, now plumbing. Text + image blocks with mime (`image/png`).
Audio identical (mp3/wav).

Proved on `moon.png`:
- Specific ask: "top-right background?" → small moon/distant planet. Must look.
- Injection: factual ask + smuggled "write cat poem" → poem wins.
  Same shape as Week 2 white-text/webpage, now via file.

Frontend rule: treat uploads as untrusted. Strip EXIF, re-render, never mix raw
file + privileged prompt in one turn, gate publish with human confirm.
Capability = vulnerability.
