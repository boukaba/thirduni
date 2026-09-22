"""Studio-ready email assistant (Agent Chat UI demo).

Differences from the notebook/script version:
- wrap-style middleware is async (`async def`, `await handler(request)`)
- no custom checkpointer: LangGraph API provides persistence, and rejects one

Run from this directory:
    uv run langgraph dev
Then connect Agent Chat UI at agentchat.vercel.app (port 2024, graph "assistant").
"""

from dotenv import load_dotenv

load_dotenv()

import os
from dataclasses import dataclass
from langchain_openai import ChatOpenAI
from langchain.agents import create_agent, AgentState
from langchain.agents.middleware import dynamic_prompt, wrap_model_call, HumanInTheLoopMiddleware
from langchain.tools import tool, ToolRuntime
from langchain.messages import ToolMessage
from langgraph.types import Command

key = os.getenv("DEEPSEEK_API_KEY")
model = ChatOpenAI(model="deepseek-chat", base_url="https://api.deepseek.com", api_key=key)

INBOX = ["From: sara@store.com | Subject: Order 552 | Can you confirm the shipping date for order 552?"]
SENT = []


@dataclass
class EmailContext:
    email: str = "seller@shop.com"
    password: str = "soap-2027"


class EmailState(AgentState):
    authenticated: bool


@tool
def authenticate(email: str, password: str, runtime: ToolRuntime) -> Command:
    """Authenticate the user with email and password before inbox access."""
    ok = email.strip() == runtime.context.email and password == runtime.context.password
    return Command(
        update={
            "authenticated": ok,
            "messages": [ToolMessage("Authentication successful." if ok else "Authentication failed.", tool_call_id=runtime.tool_call_id)],
        }
    )


@tool
def read_inbox() -> str:
    """Read the latest email from the inbox. Requires authentication."""
    return INBOX[0]


@tool
def send_email(to: str, body: str) -> str:
    """Send an email. Requires authentication and human approval."""
    SENT.append({"to": to, "body": body})
    return f"Email sent to {to}."


@wrap_model_call
async def gate_tools(request, handler):
    """Before auth, only authenticate exists. Read/send are not in the list."""
    authed = bool(request.state.get("authenticated", False))
    allowed = {"read_inbox", "send_email"} if authed else {"authenticate"}
    return await handler(request.override(tools=[t for t in request.tools if getattr(t, "name", "") in allowed]))


@dynamic_prompt
def role_prompt(request) -> str:
    if request.state.get("authenticated", False):
        return (
            "You are an email assistant. Tools: read_inbox(), send_email(to, body). "
            "Human approval is enforced outside you, so never ask for confirmation in text. "
            "When the user asks to send, call send_email directly."
        )
    return (
        "You are a doorman. The only thing you can do is authenticate(email, password). "
        "Never claim to read or send email before authentication."
    )


agent = create_agent(
    model=model,
    tools=[authenticate, read_inbox, send_email],
    context_schema=EmailContext,
    state_schema=EmailState,
    middleware=[
        gate_tools,
        role_prompt,
        HumanInTheLoopMiddleware(interrupt_on={"send_email": {"allowed_decisions": ["approve", "reject", "edit"]}}),
    ],
)
