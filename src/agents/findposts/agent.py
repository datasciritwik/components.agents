from langgraph.graph import StateGraph, END
from typing import Annotated, Sequence, TypedDict
from langchain_core.messages import HumanMessage, SystemMessage, BaseMessage, ToolMessage
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode
from langchain_groq import ChatGroq
from src.tools.alltools import webcrawl, websearch
from src.memory.memory import MemoryManager
from src.utils.config import _get_env

# Define the agent's state
class PostState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]


# Tool setup
tools = [webcrawl, websearch]
llm = ChatGroq(model="MODEL NAME", streaming=True, api_key="API KEY")
model = llm.bind_tools(tools)

# Memory Manager (DuckDB backed)
memory = MemoryManager("storage/job_assistant.duckdb")

# Core agent logic (ReAct-style)
def job_agent(state: PostState) -> PostState:
    history = memory.get_recent_messages()
    system_prompt = SystemMessage(
        content=(
            "You are an AI agent that helps users find job opportunities. "
            "Follow this 3-step reasoning:\n"
            "1. Search job postings based on user query.\n"
            "2. Crawl job details.\n"
            "3. Provide application steps and tips."
        )
    )
    
    current_user_message = state["messages"][-1]
    all_messages = [system_prompt] + history + [current_user_message]
    
    # Generate response from the model
    response = model.invoke(all_messages)
    
    # Collect tips/suggestions from the response
    tips = response.content.strip() if response.content else "No specific tips generated."

    # Find recent job data from ToolMessages
    job_data = []
    for msg in reversed(state["messages"]):
        if isinstance(msg, ToolMessage):
            try:
                # Try to parse as JSON first, then eval as fallback
                import json
                try:
                    job = json.loads(msg.content)
                except json.JSONDecodeError:
                    job = eval(msg.content)  # Use with caution
                
                if isinstance(job, dict):
                    job_data.append(job)
            except Exception as e:
                print(f"Error parsing tool message: {e}")
                continue

    # Store structured job data + tips in Markdown
    if job_data and tips:
        memory.store_job_markdown(job_data=job_data, tips=tips)

    # Store messages in memory
    memory.append_message(current_user_message)
    memory.append_message(response)

    return {"messages": state["messages"] + [response]}


# Check if tools should continue or end
def should_continue(state: PostState) -> str:
    last_message = state["messages"][-1]
    
    # If the last message has tool calls, continue to tools
    if hasattr(last_message, 'tool_calls') and last_message.tool_calls:
        return "tools"
    
    # Check for end condition in tool messages
    for msg in reversed(state["messages"]):
        if isinstance(msg, ToolMessage) and "end" in msg.content.lower():
            memory.summarize_to_long_term()
            return "end"
    
    # Otherwise, end the conversation
    return "end"


# Build the graph
def agentic():
    graph = StateGraph(PostState)
    graph.add_node("agent", job_agent)
    graph.add_node("tools", ToolNode(tools))

    graph.set_entry_point("agent")
    
    # Add conditional edges from agent
    graph.add_conditional_edges(
        "agent",
        should_continue,
        {
            "tools": "tools",
            "end": END,
        }
    )
    
    # Tools always go back to agent
    graph.add_edge("tools", "agent")
    
    return graph.compile()

