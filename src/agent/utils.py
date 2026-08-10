import math
import requests
from dotenv import load_dotenv
from langchain_core.tools import tool
from langchain_tavily import TavilySearch
from langchain_community.utilities import WikipediaAPIWrapper
from langchain_community.tools import WikipediaQueryRun
from src.agent.db import save_memory, search_memory
from src.agent.rag import retrieve_from_rag

load_dotenv()

WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")

# Used in tool to save something in memory
CURRENT_THREAD_ID = "default"

def set_current_thread_id(thread_id:str):
  global CURRENT_THREAD_ID
  CURRENT_THREAD_ID = thread_id

# web search tool
web_search = TavilySearch(
  max_results = 3,
  topic = "general",
  search_depth = "advanced"
)

# calculator tool
@tool
def calculator(exp:str)->str:
  try:
    return str(eval(exp,{"__builtins__": {}},{}))
  except Exception as e:
    return f"Error: {e}"

# wikipedia tool
api_wrapper = WikipediaAPIWrapper(
  top_k_results=3,
  doc_content_chars_max=4000
)

wikipedia = WikipediaQueryRun(
  api_wrapper=api_wrapper
)


# tool to remember something
@tool
def update_memory(memory:str)->str:
  return save_memory(
    thread_id=CURRENT_THREAD_ID,
    memory=memory
  )


# recall from memory
@tool
def recall_memory(query:str)->str:
  return search_memory(
    CURRENT_THREAD_ID,
    query=query
  )


# rag tool
@tool
def search_uploaded_documents(query:str)->str:
  return retrieve_from_rag(
    query=query,
    thread_id=CURRENT_THREAD_ID,
    k=4
  )

@tool
def weather_tool(location:str):
  try:
    url = "https://api.weatherapi.com/v1/current.json"

    params = {
      "key":WEATHER_API_KEY,
      "q":location,
      "aqi":"no"
    }

    response = requests.get(
      url,
      params=params,
      timeout=10
    )

    response.raise_for_status()
    return response.json()
  
  except requests.RequestException as e:
    return {"Error": str(e)}

tools = [
  web_search,
  calculator,
  wikipedia,
  update_memory,
  recall_memory,
  search_uploaded_documents,
  weather_tool
]