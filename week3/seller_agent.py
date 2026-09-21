from dotenv import load_dotenv

load_dotenv()

from langchain.chat_models import init_chat_model
from langchain_tavily import TavilySearch
from langgraph.checkpoint.memory import InMemorySaver
from langchain.agents import create_agent

model = init_chat_model(model="gemini-3-flash-preview", model_provider="google_genai")
search = TavilySearch(max_results=3)

system_prompt = """You draft e-commerce listings for independent sellers.
Always search trending SEO keywords first, then return title + 2-sentence description.
Remember the product across follow-ups. No extra story."""

agent = create_agent(
    model=model,
    tools=[search],
    system_prompt=system_prompt,
    checkpointer=InMemorySaver(),
)
