import os
from dotenv import load_dotenv

from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage
from langgraph.prebuilt import create_react_agent

from tools import ALL_TOOLS
from prompts import SYSTEM_PROMPT

load_dotenv()

MODEL_NAME = "openai/gpt-oss-120b"

# agent-built once per session 
_agent = None


def _get_agent():
    global _agent
    if _agent is not None:
        return _agent

    llm = ChatGroq(
        model=MODEL_NAME,
        api_key=os.getenv("GROQ_API_KEY"),
        temperature=0,
        max_tokens=1024,
    )

    # create_react_agent handles 
    # LLM → tool call → observe result → LLM → ... → final answer
    _agent = create_react_agent(
        model=llm,
        tools=ALL_TOOLS,
        state_modifier=SYSTEM_PROMPT,
    )

    print("[Agent] LangGraph ReAct agent initialised.")
    return _agent


def run_agent(user_input: str, chat_history: list) -> dict:
    """
    Run the LangGraph ReAct agent for one user turn.

    Returns:
        answer     : Final response text.
        tools_used : List of tool names that were called.
    """
    agent = _get_agent()

    # Build message list: history + current user message
    messages = [*chat_history, HumanMessage(content=user_input)]

    try:
        result = agent.invoke({"messages": messages})
    except Exception as e:
        return {
            "answer": f"Sorry, I encountered an error: {e}",
            "tools_used": [],
        }

    # The last message in result["messages"] is the final AI response
    final_message = result["messages"][-1]
    answer = final_message.content

    # Collect tool names from all ToolMessage entries in the result
    tools_used = []
    for msg in result["messages"]:
        # LangGraph marks tool call messages with a "name" attribute
        name = getattr(msg, "name", None)
        if name and name not in tools_used:
            tools_used.append(name)

    return {
        "answer": answer,
        "tools_used": tools_used,
    }