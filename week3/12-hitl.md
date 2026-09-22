# 12 — Human in the Loop

Gate sensitive tools; leave the rest automatic. Prebuilt middleware:
`HumanInTheLoopMiddleware(interrupt_on={"publish_listing": {"allowed_decisions": ["approve", "edit", "reject"]}})`

Default per tool is auto-approve. Gating is opt-in. Forgetting to name a tool is
a silent decision to let it run unsupervised.

## What an interrupt looks like

Response carries `__interrupt__`; last message is the empty-content AI with the
tool call (same signature as the Tools class, stopped one step earlier). The
payload prints exactly what it wants to do:
`{'name': 'publish_listing', 'args': {'listing': 'Artisan handmade olive oil soap, natural and handmade. (draft id 7)'}, 'description': 'Tool execution requires approval...'}`

## Three decisions (resume with same thread_id)

- Approve: `Command(resume={"decisions": [{"type": "approve"}]})` → carries on.
- Reject: add `"message": "reason"` → agent rewrote the listing and interrupted
  again with the improved text, then approved. Honest cost: another full model
  run and another interruption per rejection.
- Edit: `{"type": "edit", "edited_action": {"name": ..., "args": {...}}}` → runs
  the corrected args, no second ask. Most useful for near-miss corrections.

## Findings

- Drafting (`draft_listing`) ran with no interrupt, publish stopped. Opt-in works.
- Before I forced the flow with a system prompt, the model sometimes refused to
  publish a thin draft on its own judgment. Nice behavior, not a control.
  Prompts are suggestions; middleware is enforcement.
- Tool boundary gates beat prompt-level "please ask first" for the same reason.

## My gate list (anything that spends money, messages a human, or is irreversible)

- `publish_listing` — live storefront. Gate. (done)
- `delete_listing` — irreversible. Gate.
- `send_offer_to_buyer` — messages a human. Gate.
- Price changes, refunds, ad spend. Gate.
- Drafting, keyword research, image prep. Automatic.

Code: `hitl.py`.
