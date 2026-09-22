"""Dynamic agents: prompt by language, tools by role, model by conversation length.

Wrap style middleware gets the ModelRequest (system prompt, tools, model, state).
Node style gets state + runtime. Tools get tool runtime. Ask what you are changing
and the style picks itself.
"""

from dotenv import load_dotenv

load_dotenv()

import os
from dataclasses import dataclass
from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
from langchain.agents.middleware import dynamic_prompt, wrap_model_call
from langchain.tools import tool
from langchain.messages import HumanMessage
from langgraph.checkpoint.memory import InMemorySaver

key = os.getenv("DEEPSEEK_API_KEY")
small = ChatOpenAI(model="deepseek-chat", base_url="https://api.deepseek.com", api_key=key)
big = ChatOpenAI(model="deepseek-reasoner", base_url="https://api.deepseek.com", api_key=key)


@dataclass
class SellerContext:
    role: str = "external"
    language: str = "English"


@tool
def public_web_search(query: str) -> str:
    """Search the public web. Available to everyone."""
    return f"public results for {query}"


@tool
def internal_pricing_db(query: str) -> str:
    """Query the internal pricing database. Internal staff only."""
    return f"INTERNAL margin data for {query}: 42%"


@dynamic_prompt
def language_prompt(request) -> str:
    return (
        f"You are a seller assistant. Always answer in {request.runtime.context.language}. "
        "Keep answers under two sentences."
    )


@wrap_model_call
def role_tools(request, handler):
    """External users never see the internal tool. It is simply not in the list."""
    if request.runtime.context.role != "internal":
        request = request.override(
            tools=[t for t in request.tools if getattr(t, "name", "") != "internal_pricing_db"]
        )
    return handler(request)


@wrap_model_call
def model_switch(request, handler):
    """Cheap model by default, capable model once the conversation grows."""
    if len(request.state["messages"]) > 10:
        request = request.override(model=big)
    return handler(request)


def make_agent(middleware):
    return create_agent(
        model=small,
        tools=[public_web_search, internal_pricing_db],
        context_schema=SellerContext,
        checkpointer=InMemorySaver(),
        middleware=middleware,
    )


if __name__ == "__main__":
    a = make_agent([language_prompt, role_tools])
    for role, lang in [("external", "French"), ("internal", "Spanish")]:
        r = a.invoke(
            {"messages": [HumanMessage(content="What is our margin on soap?")]},
            context=SellerContext(role=role, language=lang),
            config={"configurable": {"thread_id": f"{role}-{lang}"}},
        )
        calls = [tc["name"] for m in r["messages"] if getattr(m, "tool_calls", None) for tc in m.tool_calls]
        print(f"{role}/{lang}: tools={calls or 'none'} | {str(r['messages'][-1].content)[:100]}")
