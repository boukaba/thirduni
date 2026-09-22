# 13 — Dynamic Agents

One agent, many users. Change prompt, tools, or model while running.

## The matrix (the useful part)

| Middleware | What you get | Use it to |
|---|---|---|
| wrap style | `ModelRequest` | change model, prompt, or tools mid-run |
| node style | state + runtime | change state (e.g. trim messages) |
| a tool | tool runtime | let the agent read/write state or context |

Ask what you are changing and the style picks itself.

## API

- `@dynamic_prompt` → callable takes `ModelRequest`, returns prompt string.
  Read context via `request.runtime.context.<field>`.
- `@wrap_model_call` → callable `(request, handler)`, return `handler(request)`.
  Change with `request.override(model=..., tools=[...])`.
- Node style stays `@before_agent` / `@after_model` etc. from lesson 11.

## Proved on the seller agent

1. Prompt by language: same agent answered in French and Spanish via
   `SellerContext(language=...)`.
2. Tools by role: external saw `['public_web_search']` only, said it had no
   access, zero tool calls. Internal saw both, called `internal_pricing_db`,
   returned the 42% margin. External is never told a tool exists.
3. Model switch, token counts side by side:
   - small (`deepseek-chat`): 7 input, 12 output tokens
   - switched (`deepseek-reasoner`) past threshold: 80 input, 400 output,
     of which 373 reasoning. Same class of question, ~30x output bill.

## Provider gotcha found while testing

DeepSeek now reports `deepseek-flash` as `model_name` for BOTH
`deepseek-chat` and `deepseek-reasoner`. Response metadata will not tell you
which model answered. The tell is `usage_metadata.output_token_details.reasoning`
(present only for the reasoning model). Do not audit routing on `model_name`
alone without checking your provider's behavior.

Code: `dynamic_agent.py`.
