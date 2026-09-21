# 03 — Short-Term Memory

Agents forget between runs. State holds messages but isn't saved.
Fix: checkpointer snapshot + `thread_id` to group runs.

Proved with shop product:
- No checkpointer: "I don't know what your shop sells."
- `InMemorySaver` + `thread_id=seller-1`: "Your shop sells handmade olive oil soap",
  4 messages in state.
- `thread_id=seller-2`: gone — that's user-session isolation for frontend.

Model + tools + memory = agent. Everything after is refinement.
Custom state fields (e.g. user_id) possible; default tracks messages.
