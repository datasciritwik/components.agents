import streamlit as st 
from src.utils.config import _set_env
st.set_page_config(page_title="Setting", page_icon="⚙️", initial_sidebar_state="expanded", layout="wide")


st.html("<style>[data-testid='stHeaderActionElements'] {display: none;}</style>")

options = ['⚙️ Settings', '🧑‍💻 FindposT']
OPTIONS = st.sidebar.radio(label="select options", label_visibility="collapsed", options=options)

if OPTIONS == options[0]:

    st.markdown("""
### 🔧 Configuration

Please provide the following:
1. **Model Name** – Choose or enter the LLM you wish to use (e.g., `gpt-4`, `llama`, etc.)
2. **Groq API Key** – Required to authenticate and interact with Groq models
3. **Tavily API Key** – Required for web search functionality using Tavily
""")

    # Input fields
    model_name = st.text_input("🔤 Model Name", placeholder="e.g., gpt-4")
    groq_api_key = st.text_input("🔑 Groq API Key", type="password", placeholder="Enter your Groq API Key", help="Currently only added Groq; for using other models, please adjust the code accordingly.")
    tavily_api_key = st.text_input("🌐 Tavily API Key", type="password", placeholder="Enter your Tavily API Key")

    # Save Button
    if st.button("💾 Save Configuration"):
        if model_name and groq_api_key and tavily_api_key:
            # Save to session state
            st.session_state["model_name"] = model_name
            st.session_state["groq_api_key"] = groq_api_key
            st.session_state["tavily_api_key"] = tavily_api_key

            # Set as environment variables
            _set_env("MODEL_NAME", model_name)
            _set_env("GROQ_API_KEY", groq_api_key)
            _set_env("TAVILY_API_KEY", tavily_api_key)

            st.success("✅ Configuration saved and environment variables set.")
        else:
            st.warning("⚠️ Please fill in all fields before saving.")

elif OPTIONS == options[1]:
    st.switch_page("pages/job.py")

