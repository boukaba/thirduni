# 10 — What Is Middleware?

Middleware = functions inserted inside the model/tool loop. Out of the box you
choose model, prompt, tools at the start, then watch. Middleware is your code
running mid-loop, changing what happens next.

Two canonical examples from the lesson, both boundaries not brains:
- Payroll assistant must not give legal advice → classifier runs AFTER the answer.
- Support agent issues refunds → human approval BEFORE that tool only.

## My two doors (seller agent)

1. Before: publishing. Drafting, rewriting, keyword research all safe alone.
   Publish touches the world and can't be undone. Human approval goes before
   that specific tool. Everything else stays automatic.
2. After: regulated claims. "Organic", "vegan", "hypoallergenic" are claims a
   seller can be held to, not just SEO words. Classifier after the answer flags
   unsupported terms. Not blocked, checked.

## Why it lands now

Week 3 was building the loop; middleware intervenes in the loop, so it needed
the loop to exist first. Rest of the module = specific middleware per failure:
long conversations, unsupervised actions, different users.

## Ready locally

`from langchain.agents.middleware import before_model, after_model, wrap_model_call`
imports clean in the course venv. Build lessons can start immediately.
