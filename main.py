from src.agents.findposts.agent import agentic
from src.utils.config import _get_env, _set_env
if __name__ == '__main__':
    tavily_api_key = "API KEY"
    _set_env("TAVILY_API_KEY", tavily_api_key)
    
    _get_env("TAVILY_API_KEY")
    response = agentic()
    def print_stream(stream):
        for s in stream:
            message = s['messages'][-1]
            if isinstance(message, tuple):
                print(message)
            else:
                try:
                    message.pretty_print()
                except AttributeError:
                    print(message)
    inputs = {"messages": "Find Data Scientist jobs in Hyderabad, India"}
    print_stream(response.stream(inputs, stream_mode="values"))