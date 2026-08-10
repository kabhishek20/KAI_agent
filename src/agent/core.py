"""LangGraph agent construction and model selection helpers."""

import os
import sqlite3
import sys
from pathlib import Path

# Ensure the repository root is on sys.path 
# when running this file directly from a nested folder
ROOT_DIR = Path(__file__).resolve().parents[2]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from dotenv import load_dotenv
import certifi

from langchain_google_genai import ChatGoogleGenerativeAI


def _ensure_directory(path: str | Path) -> None:
    """Create a directory in a way that remains compatible with older Python versions."""
    directory = Path(path)
    try:
        directory.mkdir(exist_ok=True)
    except TypeError:
        if not directory.exists():
            directory.mkdir()
from langchain_core.messages import SystemMessage
from langgraph.graph import StateGraph, START, MessagesState
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.checkpoint.sqlite import SqliteSaver

from prompts.system_prompt import SYSTEM_PROMPT
from src.agent.utils import tools

load_dotenv()

# prevent path related error for windows
os.environ["SSL_CERT_FILE"] = certifi.where()
os.environ["REQUEST_CA_BUNDLE"] = certifi.where()

# create data folder to store checkpoints
# if it doesn't exist
_ensure_directory("data")


# Keeping default LLM Model
DEFAULT_MODEL = os.getenv("LLM_MODEL", "gemini-3.6-flash")

# List of all LLM Models
ALLOWED_MODELS = {
    "gemini-3.6-flash",
    "gemini-3.5-flash",
    "gemini-3.5-flash-lite",
    "gemini-2.5-flash",
    "gemini-2.5-pro",
}


def normalize_model_name(model_name: str):
    """Return a supported model name, falling back to the default model when needed."""
    if not model_name:
        return DEFAULT_MODEL

    model_name = model_name.strip()
    if model_name in ALLOWED_MODELS:
        return model_name
    return DEFAULT_MODEL


def build_agent(model_name: str):
    """Build and compile a LangGraph agent configured with the requested model."""
    selected_model = normalize_model_name(model_name)

    # Initializing llm
    llm = ChatGoogleGenerativeAI(
        model=selected_model,
        temperature=0.1,
        streaming=True,
    )

    # Binding tools to llm
    llm_with_tools = llm.bind_tools(tools)

    def chatbot_node(state: MessagesState):
        """Generate a chat response using the configured system prompt and the current message state."""
        messages = [SystemMessage(content=SYSTEM_PROMPT)] + state["messages"]
        response = llm_with_tools.invoke(messages)
        return {"messages": [response]}

    # tool node
    tool_node = ToolNode(tools)

    # Building graph
    workflow = StateGraph(MessagesState)

    workflow.add_node("chatbot", chatbot_node)
    workflow.add_node("tools", tool_node)

    workflow.add_edge(START, "chatbot")
    workflow.add_conditional_edges("chatbot", tools_condition)
    workflow.add_edge("tools", "chatbot")

    # Adding memory
    conn = sqlite3.connect(
        "data/checkpoints.sqlite",
        check_same_thread=False,
    )

    checkpointer = SqliteSaver(conn)
    return workflow.compile(checkpointer=checkpointer)


# storing the langgraph agent in cache
# so everytime we dont have to build it
_AGENT_CACHE = {}


def get_agent(model_name: str | None = None):
    """Return a cached agent instance, creating it on first use for the selected model."""
    selected_model = normalize_model_name(model_name)

    if selected_model not in _AGENT_CACHE:
        _AGENT_CACHE[selected_model] = build_agent(selected_model)

    return _AGENT_CACHE[selected_model]