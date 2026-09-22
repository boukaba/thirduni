"""HITL: gate only publish_listing, leave drafting automatic.

One middleware arg gates one tool. Approve, reject-with-note, and edit all
demonstrated. Resume needs the same thread_id and a Command(resume=...).

Run needs DEEPSEEK_API_KEY in .env.
"""

from dotenv import load_dotenv

load_dotenv()

import os
from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
from langchain.agents.middleware import HumanInTheLoopMiddleware
from langchain.tools import tool
from langchain.messages import HumanMessage
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.types import Command

model = ChatOpenAI(model="deepseek-chat", base_url="https://api.deepseek.com", api_key=os.getenv("DEEPSEEK_API_KEY"))

published = []


@tool
def draft_listing(product: str) -> str:
    """Draft a product listing. Safe, runs automatically."""
    return f"DRAFT for {product}: Artisan {product}, natural and handmade. (draft id 7)"


@tool
def publish_listing(listing: str) -> str:
    """Publish a listing to the live storefront. Irreversible."""
    published.append(listing)
    return f"PUBLISHED to storefront: {listing}"


def make_agent():
    return create_agent(
        model=model,
        tools=[draft_listing, publish_listing],
        system_prompt=(
            "You are a listing assistant. Draft the listing, then immediately call "
            "publish_listing with it. Never ask questions. Never comment on draft quality."
        ),
        checkpointer=InMemorySaver(),
        middleware=[
            HumanInTheLoopMiddleware(
                interrupt_on={
                    # only publish is gated; draft has no entry, so it auto-approves
                    "publish_listing": {"allowed_decisions": ["approve", "edit", "reject"]}
                }
            )
        ],
    )


def start(agent, tid):
    cfg = {"configurable": {"thread_id": tid}}
    r = agent.invoke(
        {"messages": [HumanMessage(content="Draft a listing for handmade olive oil soap and publish it.")]},
        config=cfg,
    )
    return cfg, r


if __name__ == "__main__":
    # 1. approve
    a = make_agent()
    cfg, r = start(a, "hitl-approve")
    print("APPROVE wants:", str(r["__interrupt__"][0].value)[:200])
    r = a.invoke(Command(resume={"decisions": [{"type": "approve"}]}), config=cfg)
    print("APPROVE final:", str(r["messages"][-1].content)[:120])

    # 2. reject with a note, agent rewrites, interrupts again
    a = make_agent()
    cfg, r = start(a, "hitl-reject")
    r = a.invoke(
        Command(resume={"decisions": [{"type": "reject", "message": "Too generic, mention cold-process and sensitive skin."}]}),
        config=cfg,
    )
    print("REJECT interrupted again:", "__interrupt__" in r)
    r = a.invoke(Command(resume={"decisions": [{"type": "approve"}]}), config=cfg)
    print("REJECT final:", str(r["messages"][-1].content)[:140])

    # 3. edit args, runs without a second ask
    a = make_agent()
    cfg, r = start(a, "hitl-edit")
    r = a.invoke(
        Command(
            resume={
                "decisions": [
                    {
                        "type": "edit",
                        "edited_action": {
                            "name": "publish_listing",
                            "args": {"listing": "EDITED BY HUMAN: Artisan cold-process olive oil soap, unscented."},
                        },
                    }
                ]
            }
        ),
        config=cfg,
    )
    print("EDIT final:", str(r["messages"][-1].content)[:120])
    print("published store:", published)
