import streamlit as st
from src.agents.findposts.agent import agentic, PostState
from src.memory.memory import MemoryManager
from langchain_core.messages import HumanMessage

st.set_page_config(
    page_title="FindposT", 
    page_icon="🧑‍💻", 
    initial_sidebar_state="collapsed", 
    layout="wide"
)

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

if "agent_graph" not in st.session_state:
    st.session_state.agent_graph = agentic()

if "memory_manager" not in st.session_state:
    import os
    # Ensure storage directory exists
    os.makedirs("storage", exist_ok=True)
    st.session_state.memory_manager = MemoryManager("storage/job_assistant.duckdb")

# Sidebar
sidebar = st.sidebar.title(":red[FindposT]")
with st.sidebar:
    st.markdown("#### :green[Search and apply for job in one place]")
    
# Add a debug section in sidebar for development
with st.sidebar:
    st.markdown("---")
    if st.button("🔧 Debug Database"):
        st.session_state.memory_manager.get_table_info()
        st.success("Check console for debug info")
    
    if st.button("🗑️ Clear Database"):
        st.session_state.memory_manager.clear_all_data()
        st.success("Database cleared!")
        
    # Add job search history
    st.markdown("#### Recent Job Searches")
    
    # Get and display recent job markdowns
    try:
        job_markdowns = st.session_state.memory_manager.get_all_job_markdowns()
        if job_markdowns:
            for i, md in enumerate(job_markdowns[:3]):  # Show last 3 searches
                with st.expander(f"Search {i+1}", expanded=False):
                    st.markdown(md[:200] + "..." if len(md) > 200 else md)
        else:
            st.info("No previous searches found")
    except Exception as e:
        st.error(f"Error loading search history: {str(e)}")

# Main layout
st.title("🧑‍💻 FindposT - AI Job Search Assistant")
st.markdown("Search for jobs and get personalized application tips!")

# Display previous chat messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Create two columns for chat and job posts
chat_col, post_col = st.columns([2, 1], gap="medium")

with chat_col:
    st.subheader("💬 Chat with Job Assistant")
    
    # Chat input
    user_input = st.chat_input("Type your job search query... (e.g., 'Find Python developer jobs in San Francisco')")

    if user_input:
        # Save user message
        st.session_state.messages.append({"role": "user", "content": user_input})
        
        # Display user message
        with st.chat_message("user"):
            st.markdown(user_input)

        # Prepare assistant message area
        with st.chat_message("assistant"):
            with st.spinner("🔍 Searching for jobs and analyzing opportunities..."):
                response_container = st.empty()
                
                def run_agent_stream():
                    try:
                        # Create initial state
                        initial_state = PostState(
                            messages=[HumanMessage(content=user_input)]
                        )
                        
                        # Run the agent
                        result = st.session_state.agent_graph.invoke(initial_state)
                        
                        # Extract the final assistant message
                        assistant_messages = []
                        for msg in result["messages"]:
                            if hasattr(msg, 'content') and msg.content:
                                msg_type = type(msg).__name__
                                if msg_type not in ['HumanMessage', 'ToolMessage']:
                                    assistant_messages.append(msg)
                        
                        if assistant_messages:
                            final_response = assistant_messages[-1].content
                            # Clean up the response if it contains tool calls info
                            if "tool_calls" in str(final_response).lower():
                                final_response = "I've searched for job opportunities based on your query. Check the job posts panel for detailed results!"
                            return final_response
                        else:
                            return "I found some job opportunities! Check the job posts panel for details."
                            
                    except Exception as e:
                        error_msg = str(e)
                        st.error(f"Error running agent: {error_msg}")
                        
                        # Provide more specific error handling
                        if "response" in error_msg:
                            return "I'm processing your job search request. There might be an issue with the response generation, but I'm still working on finding opportunities for you."
                        elif "tool" in error_msg.lower():
                            return "I'm having trouble accessing the job search tools. Please try again or rephrase your query."
                        else:
                            return f"Sorry, I encountered an error while searching for jobs: {error_msg}"

                def stream_generator():
                    response = run_agent_stream()
                    # Simulate streaming by yielding chunks
                    words = response.split()
                    for i, word in enumerate(words):
                        if i == 0:
                            yield word
                        else:
                            yield " " + word

                # Stream the response
                full_response = response_container.write_stream(stream_generator())

        # Save assistant response
        st.session_state.messages.append({"role": "assistant", "content": full_response})

with post_col:
    st.subheader("📋 Job Opportunities")
    
    # Try to get the latest job posts from memory
    try:
        job_markdowns = st.session_state.memory_manager.get_all_job_markdowns()
        
        if job_markdowns:
            latest_jobs = job_markdowns[0]  # Get the most recent job search results
            
            # Display the job posts
            with st.container():
                st.markdown(latest_jobs)
                
            # Add download button for job data
            st.download_button(
                label="📥 Download Job List",
                data=latest_jobs,
                file_name="job_opportunities.md",
                mime="text/markdown"
            )
            
        else:
            st.info("🔍 No job posts found yet. Start a conversation to search for jobs!")
            
    except Exception as e:
        st.error(f"Error loading job posts: {str(e)}")

# Add some helpful examples at the bottom
with st.expander("💡 Example Queries", expanded=False):
    st.markdown("""
    **Try these example queries:**
    - "Find Python developer jobs in New York"
    - "Search for remote data scientist positions"
    - "Look for frontend developer jobs at startups"
    - "Find entry-level software engineer positions"
    - "Search for AI/ML engineer jobs with good benefits"
    """)

# Add a clear chat button
if st.session_state.messages:
    if st.button("🗑️ Clear Chat History"):
        st.session_state.messages = []
        st.rerun()

# Footer
st.markdown("---")
st.markdown("Built with ❤️ using LangGraph and Streamlit")