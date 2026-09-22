# 00 — Free Tools: "If you cannot pay" + "OpenCode"

The two opening lessons of Week 3, both about doing this without a bank card.

## If you cannot pay for the tools

Constraint set: no debit cards in Algeria, OpenAI has no free tier, Claude /
Cursor / Codex are paid, and the mentors will not be handing out credits. The
lesson's point is that the model is the one part of the stack you can swap.

Free options listed in the course (Setup lesson's table, same content):
- Gemini Flash, `aistudio.google.com/apikey` — free, no card, reliable tool calling.
- Tavily, `app.tavily.com` — free, 1,000 searches/month, no card. Search tool
  from the Tools class onward.
- gpt-oss on Groq, `console.groq.com/keys` — free, Apache-2.0, ~30 req/min.
- gpt-oss via Ollama — no account, no key, nothing leaves the machine. Needs a
  capable laptop, realistically 16GB RAM.
- University email + GitHub Student Pack — free tiers of Figma, Cursor and co.

One warning worth keeping: free tiers are usually paid for with your data.
Google states plainly that content improves their products. Fine for coursework,
wrong for anything private. Local gpt-oss is the version where the question
does not arise.

What we actually ran this week: Gemini free tier for most lessons, DeepSeek
(cheap, paid) for the heavy multi-agent runs, Tavily free for search, and Ollama
with `qwen3:8b` / `llama3` installed as the offline fallback. Keys live in
`.env`, never in chat or notebooks.

## OpenCode, an agent nobody can price you out of

Open-source, model-agnostic coding agent. No subscription. The Setup lesson
hands the repository setup to "OpenCode, from the last class, or Cursor" and
gives you the prompt box to paste in.

That box is written for a coding agent: clone the repo, install Python and
packages, create `.env` with blanks only, never ask for or write an API key,
report which lines to fill, run the verification script, and never print
`.env`. We did exactly that in this repo's setup (see `setup.md`): OpenCode
created the file, printed the two lines to fill, waited, then ran
`env_utils.py` after the keys were added.

The whole week ran with OpenCode as the pair: tools, memory, MCP, the wedding
team, the email capstone, and the RAG repro.
