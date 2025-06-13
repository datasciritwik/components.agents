from dotenv import load_dotenv
import os
load_dotenv()

class Config:
    # Reads from system environment
    nvidia_api = os.getenv("NVIDIA_API_KEY")
    groq_api = os.getenv("GROQ_API_KEY")
    openai_api = os.getenv("OPENAI_API_KEY", "")
    google_api = os.getenv("GOOGLE_API_KEY", "")
    xai_api = os.getenv("XAI_API_KEY", "")

    @classmethod
    def load_envs(cls):
        os.environ["NVIDIA_API_KEY"] = cls.nvidia_api or ""
        os.environ["GROQ_API_KEY"] = cls.groq_api or ""
        os.environ["OPENAI_API_KEY"] = cls.openai_api or ""
        os.environ["GOOGLE_API_KEY"] = cls.google_api
        os.environ["XAI_API_KEY"] = cls.xai_api
  
  
   
# # Load keys into os.environ explicitly if needed
# Config.load_envs()

# # Use keys directly
# print(Config.nvidia_api)
