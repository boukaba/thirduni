# 06 — MCP (Model Context Protocol)

USB for agents. Before: fresh tangle of API calls per app. After: server exposes
tools/resources/prompts, client plugs in. Host = your agent.

Words: server exposes, client talks, host holds client.
Transport matters: `stdio` vs `streamable_http` — wrong one = failed connect.

Proved in one run:
- Mine: `seller_mcp` over stdio, 1 tool `listing_title(product)`.
- Public: `mcp-server-time` via `uvx` — `get_current_time`, `convert_time`, no key.
- Prompt "title for olive oil soap + current UTC" → agent called both:
  `Artisan Olive Oil Soap - Natural Handmade Bar` + `08:18 UTC Tue Sep 22 2026`.

Notes:
- Built with `FastMCP` + `@mcp.tool()` decorator (familiar after Tools class).
- Client via `langchain_mcp_adapters.client.MultiServerMCPClient`.
- Server reusable: any MCP app (chatbot, IDE) can use `seller_mcp`, not just my agent.
- MCP class is the one lesson needing local machine (`uvx` to start server).

Frontend use: my listing tool + their time/delivery estimate. No new keys.
