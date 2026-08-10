# KAI_agent

KAI Agent is a Python-based chatbot project that uses LangGraph and LangChain to build an AI assistant with tool support, long-term memory, and document retrieval.

## Overview

This repository implements a conversational AI agent that:
- Uses Google Generative AI models via `langchain-google-genai`.
- Supports tool-enabled workflows such as web search, Wikipedia lookup, calculation, memory storage, document retrieval, and weather lookup.
- Stores conversation metadata and chat history in a local SQLite database.
- Supports RAG (retrieval-augmented generation) by ingesting uploaded documents and querying relevant content.
- Includes a configurable system prompt to guide the assistant behavior.

## Key Features

- Model selection via environment variable `LLM_MODEL`
- Persistent conversation state in `data/chatbot_memory.db`
- Memory save and recall using long-term memory records
- Document upload ingestion for enhanced QA
- Web search and Wikipedia tools
- Weather API integration
- Streaming responses in the demo script

## Repository Structure

- `requirements.txt` - Python dependencies
- `README.md` - Project documentation
- `src/agent/app.py` - Example entrypoint that sends a prompt to the agent
- `src/agent/core.py` - Agent construction and caching logic
- `src/agent/db.py` - SQLAlchemy database models and helper functions
- `src/agent/rag.py` - Document ingestion and search helpers
- `src/agent/utils.py` - Agent builder, tool binding, and LangGraph workflow setup
- `src/agent/state.py` - Placeholder state module (currently empty)
- `src/agent/__init__.py` - Package initializer
- `prompts/system_prompt.py` - System prompt definition for the assistant
- `chroma_db/` - Persisted Chroma vector store directory
- `data/` - Data storage for checkpoints and other runtime files
- `uploads/` - Upload folder for documents to ingest
- `templates/index.html` - placeholder template file

## Installation

1. Create and activate a Python virtual environment.

   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

2. Install dependencies.

   ```powershell
   pip install -r requirements.txt
   ```

## Environment Configuration

Create a `.env` file or set environment variables in your shell.

Recommended variables:

- `LLM_MODEL` - Default model for chat inference (`gemini-3.6-flash` by default)
- `EMBEDDING_MODEL` - Embedding model for RAG (`gemini-embedding-001` by default)
- `WEATHER_API_KEY` - API key for the weather tool
- Google GenAI credentials as required by `langchain-google-genai`

Example `.env` file:

```env
LLM_MODEL=gemini-3.6-flash
EMBEDDING_MODEL=gemini-embedding-001
WEATHER_API_KEY=your_weather_api_key_here
# Add Google API credentials / key as required by your Google GenAI setup
```

## Usage

Run the example agent script from the repository root:

```powershell
python .\src\agent\app.py
```

The script sends a sample prompt (`5+4*3-1`) to the configured model and streams the response.

### Extending the Agent

- Modify `prompts/system_prompt.py` to change the assistant behavior and tone.
- Add or update tools in `src/agent/utils.py` and `src/agent/rag.py`.
- Manage conversation state and memory via `src/agent/db.py`.

## Document Retrieval (RAG)

Supported upload formats:
- PDF (`.pdf`)
- Word (`.docx`)
- Text (`.txt`)
- Markdown (`.md`)
- Python script (`.py`)
- CSV (`.csv`)

Documents are processed into chunks, embedded with the configured embedding model, and stored in `chroma_db`.

## Tools Included

- `TavilySearch` web search
- `calculator` arithmetic evaluation
- `WikipediaQueryRun` Wikipedia lookup
- `update_memory` save notes to long-term memory
- `recall_memory` retrieve stored memory
- `search_uploaded_documents` search ingested files
- `weather_tool` current weather lookup

## Notes

- The project uses local SQLite databases under `data/` and `chroma_db/`.
- `src/agent/state.py` is currently empty and can be extended for custom state management.
- `templates/index.html` is a placeholder and does not yet contain a UI implementation.

## License

This repository includes a `LICENSE` file at the project root.
