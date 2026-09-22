# 11 — Managing Long Conversations

The checkpointer keeps every message, so the list only grows. Every call resends
the whole history, so cost and latency grow with it, until the window overflows.

Measured growth, six turns, no middleware (input tokens per call):
20, 423, 911, 1658, 2230, 2907. Roughly doubles per turn.

## Fix 1: SummarizationMiddleware (out of the box)

Config: model that summarizes (can be cheap/different), `trigger=("tokens", N)`,
`keep=("messages", N)`. In this build the params are tuples, not kwargs.

Observed: fired at turn 3, state collapsed (4 messages -> 3: summary + recent),
conversation continued. Sharp edge: trigger too low (I used 400) means it
re-summarizes every turn, and the summarizer's verbose output becomes the new
bloat. Input still grew 739 -> 2322 after summaries started. Raise the trigger,
write a tight summary prompt.

## Fix 2: Trim via custom middleware

Four hooks: `before_agent` and `after_agent` run once per run (start/end);
`before_model` and `after_model` run before/after every model call.

Two gotchas found by failing:
1. Returning a filtered message list does NOT delete. `AgentState.messages` uses
   the `add_messages` reducer (merge by id). Deletion requires
   `RemoveMessage(id=...)` from `langgraph.graph.message`.
2. Deleting a ToolMessage alone breaks the request: the AIMessage above it still
   has `tool_calls` and OpenAI-compatible APIs reject with "An assistant message
   with 'tool_calls' must be followed by tool messages". Delete the exchange as
   a pair (ToolMessage + its tool-calling AIMessage).

## Proof method worth copying

Don't verify by reading your own code. A tool wrote 22.5C into a ToolMessage.
Control agent: answers 22.5C. Trimmed agent: "I don't know. I haven't actually
checked." That proves the deletion happened before the model saw state.

Code: `long_conversations.py`. Token counts are the bill; read `usage_metadata`.
