"""Seller team: supervisor + researcher + writer.

Supervisor delegates via tools (sub-agent = tool).
Run from the upstream clone so Tavily key loads from its .env:
  cd lca-lc-foundations && uv run python ../thirduni/week3/seller_team.py
Or copy beside a .env and run with plain load_dotenv.
"""

from dotenv import load_dotenv

load_dotenv()

from langchain.chat_models import init_chat_model
from langchain.agents import create_agent
from langchain.tools import tool
from langchain_tavily import TavilySearch

model = init_chat_model(model="gemini-3-flash-preview", model_provider="google_genai")
search = TavilySearch(max_results=2)

researcher = create_agent(
    model=model,
    tools=[search],
    system_prompt="Research trending SEO keywords. Reply with 5 keywords only.",
)
writer = create_agent(
    model=model,
    system_prompt="Write a 2-sentence product description from given keywords. No tools.",
)


@tool
def keyword_expert(product: str) -> str:
    """Research trending SEO keywords for a product. Input: product name."""
    r = researcher.invoke({"messages": [{"role": "human", "content": f"Keywords for: {product}. 5 only."}]})
    return str(r["messages"][-1].content)


@tool
def listing_writer(keywords: str) -> str:
    """Write the final listing from SEO keywords. Input: keywords."""
    r = writer.invoke({"messages": [{"role": "human", "content": f"Listing from: {keywords}"}]})
    return str(r["messages"][-1].content)


boss = create_agent(
    model=model,
    tools=[keyword_expert, listing_writer],
    system_prompt="Coordinate. First keyword_expert, then listing_writer with those keywords. Reply final listing.",
)

if __name__ == "__main__":
    r = boss.invoke({"messages": [{"role": "human", "content": "New product: handmade olive oil soap"}]})
    for m in r["messages"]:
        print(
            type(m).__name__,
            "| tools:",
            getattr(m, "tool_calls", None),
            "| text:",
            str(m.content)[:300].replace(chr(10), " "),
        )
