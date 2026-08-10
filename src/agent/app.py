import warnings
from core import get_agent
from langchain_core.messages import HumanMessage

warnings.filterwarnings("ignore")

agent = get_agent("gemini-3.6-flash")
config = {
    "configurable": {
        "thread_id": "test_thread_id"
    }
}

prompt = "Generate a blog on Machine Learning"
final_blog = ""

for message_chunk, metadata in agent.stream(
    {"messages": [HumanMessage(content=prompt)]},
    config=config,
    stream_mode="messages",
):
    content = message_chunk.content

    # Gemini may return content as a string
    if isinstance(content, str):
        chunk_text = content

    # Or as a list of content blocks
    elif isinstance(content, list):
        chunk_text = ""

        for block in content:
            if isinstance(block, dict) and block.get("type") == "text":
                chunk_text += block.get("text", "")

    else:
        chunk_text = ""

    if chunk_text:
        # Show the response as it is generated
        print(chunk_text, end="", flush=True)

        # Keep a copy of the complete response
        final_blog += chunk_text


# Complete response is now available here
print("\n\n" + "=" * 60)
print("BLOG GENERATION COMPLETE")
print("=" * 60)