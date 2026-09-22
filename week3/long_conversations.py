"""Long conversations: summarization + a trim hook, with proof.

Two fixes for an ever-growing message list:
  1. SummarizationMiddleware — compresses old turns into a summary.
  2. A custom before_agent hook — deletes what you choose (here: tool exchanges).

Run needs DEEPSEEK_API_KEY in .env.
"""

from dotenv import load_dotenv

load_dotenv()

import os
from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
from langchain.agents.middleware import SummarizationMiddleware, before_agent
from langchain.tools import tool
from langchain.messages import ToolMessage, HumanMessage
from langgraph.graph.message import RemoveMessage
from langgraph.checkpoint.memory import InMemorySaver

model = ChatOpenAI(model="deepseek-chat", base_url="https://api.deepseek.com", api_key=os.getenv("DEEPSEEK_API_KEY"))


@tool
def device_temperature() -> str:
    """Read the device temperature."""
    return "Device temperature is 22.5C"


@before_agent
def strip_tool_exchanges(state, runtime):
    """Delete tool exchanges before the agent sees state.

    Gotcha 1: messages use the add_messages reducer, a filtered list does NOT
    delete. Deletion needs RemoveMessage(id=...).
    Gotcha 2: deleting a ToolMessage alone leaves the AIMessage above it with
    dangling tool_calls; OpenAI-compatible APIs reject that. Remove both.
    """
    return {
        "messages": [
            RemoveMessage(id=m.id)
            for m in state["messages"]
            if isinstance(m, ToolMessage) or (getattr(m, "tool_calls", None))
        ]
    }


def summarizer_agent():
    return create_agent(
        model=model,
        checkpointer=InMemorySaver(),
        middleware=[
            SummarizationMiddleware(
                model=model,
                trigger=("tokens", 2000),  # too low re-summarizes every turn
                keep=("messages", 1),
            )
        ],
    )


def trimming_agent():
    return create_agent(
        model=model,
        tools=[device_temperature],
        checkpointer=InMemorySaver(),
        middleware=[strip_tool_exchanges],
    )


if __name__ == "__main__":
    # Proof: without the hook the agent remembers the tool result,
    # with it the tool exchange is gone before the model sees state.
    for label, mw, tid in [("CONTROL", [], "ctrl"), ("TRIM", [strip_tool_exchanges], "trim")]:
        a = create_agent(model=model, tools=[device_temperature], checkpointer=InMemorySaver(), middleware=mw)
        cfg = {"configurable": {"thread_id": tid}}
        a.invoke({"messages": [HumanMessage(content="Check the device temperature, then reply only OK.")]}, config=cfg)
        r = a.invoke({"messages": [HumanMessage(content="What was the device temperature? If you do not know, say so.")]}, config=cfg)
        print(f"{label}: {str(r['messages'][-1].content)[:160]}")
