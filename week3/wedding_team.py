"""Wedding team v2: state shared by explicit passing.

Lesson from v1: sub-agents invoked inside wrapper tools do NOT inherit the
boss's state -- each has its own. So the boss reads its own state and passes
facts as tool arguments. State is how the BOSS tracks; arguments are how the
team communicates.
"""

from dotenv import load_dotenv

load_dotenv()  # expects TAVILY_API_KEY + DEEPSEEK_API_KEY in .env (see ../.env.example)

import os
import sqlite3
from langchain_openai import ChatOpenAI
from langchain.agents import create_agent, AgentState
from langchain.tools import tool, ToolRuntime
from langgraph.types import Command
from langchain.messages import ToolMessage
from langchain_tavily import TavilySearch

# Course database (clone https://github.com/langchain-ai/lca-lc-foundations next to this repo,
# or point CHINOOK_DB at your copy):
DB = os.getenv(
    "CHINOOK_DB",
    "../lca-lc-foundations/notebooks/module-2/resources/Chinook.db",
)
model = ChatOpenAI(model="deepseek-chat", base_url="https://api.deepseek.com", api_key=os.getenv("DEEPSEEK_API_KEY"))
web = TavilySearch(max_results=2)


class WeddingState(AgentState):
    origin: str
    destination: str
    dates: str
    guests: str
    genre: str


@tool
def set_details(origin: str, destination: str, dates: str, guests: str, genre: str, runtime: ToolRuntime) -> Command:
    """Save wedding details to shared state. Call first with all five."""
    return Command(
        update={
            "origin": origin, "destination": destination, "dates": dates,
            "guests": guests, "genre": genre,
            "messages": [ToolMessage("Details saved", tool_call_id=runtime.tool_call_id)],
        }
    )


@tool
def read_state(runtime: ToolRuntime) -> str:
    """Read shared wedding details (origin, destination, dates, guests, genre)."""
    s = runtime.state
    return f"origin={s.get('origin')}, destination={s.get('destination')}, dates={s.get('dates')}, guests={s.get('guests')}, genre={s.get('genre')}"


@tool
def flight_search(query: str) -> str:
    """Search live flights. Input: full route + dates."""
    return str(web.invoke(f"cheap flights {query}"))[:600]


@tool
def venue_search(query: str) -> str:
    """Search wedding venues. Input: city + guests."""
    return str(web.invoke(f"wedding venue {query}"))[:600]


@tool
def music_search(genre: str) -> str:
    """Query music DB for playlist tracks. Input: genre name."""
    con = sqlite3.connect(DB)
    rows = con.execute(
        "SELECT t.Name, ar.Name FROM Track t JOIN Album al ON al.AlbumId=t.AlbumId "
        "JOIN Artist ar ON ar.ArtistId=al.ArtistId JOIN Genre g ON g.GenreId=t.GenreId "
        "WHERE g.Name LIKE ? LIMIT 5",
        (f"%{genre}%",),
    ).fetchall()
    con.close()
    return str(rows) if rows else "No tracks for genre"


flight_agent = create_agent(model=model, tools=[flight_search],
    system_prompt="Search flights for the given route. Reply 2 options only. No questions.")
venue_agent = create_agent(model=model, tools=[venue_search],
    system_prompt="Search venues for the given city and guests. Reply 2 options only. No questions.")
music_agent = create_agent(model=model, tools=[music_search],
    system_prompt="Query music_search with the given genre. Reply 5 tracks only. No questions.")


@tool
def flight_expert(origin: str, destination: str, dates: str) -> str:
    """Get flight options. Inputs: origin city, destination city, dates."""
    r = flight_agent.invoke({"messages": [{"role": "human", "content": f"Flights from {origin} to {destination}, {dates}."}]})
    return str(r["messages"][-1].content)


@tool
def venue_expert(destination: str, guests: str) -> str:
    """Get venue options. Inputs: destination city, guest count."""
    r = venue_agent.invoke({"messages": [{"role": "human", "content": f"Venues in {destination} for {guests} guests."}]})
    return str(r["messages"][-1].content)


@tool
def music_expert(genre: str) -> str:
    """Get playlist. Input: music genre."""
    r = music_agent.invoke({"messages": [{"role": "human", "content": f"Playlist for genre {genre}."}]})
    return str(r["messages"][-1].content)


boss = create_agent(
    model=model,
    tools=[set_details, read_state, flight_expert, venue_expert, music_expert],
    state_schema=WeddingState,
    system_prompt="Coordinator. 1) set_details: London, Paris, Jun 12 2027, 80 guests, Rock. "
    "2) read_state, then call all three experts with those exact values. "
    "3) Compile flights+venue+playlist. Never ask questions.",
)

if __name__ == "__main__":
    r = boss.invoke({"messages": [{"role": "human", "content": "Plan our Paris wedding."}]})
    print(str(r["messages"][-1].content)[:1800])
