from setuptools import setup, find_packages
import setuptools.command.install
import subprocess

class CustomInstallCommand(setuptools.command.install.install):
    def run(self):
        subprocess.check_call([self._python_executable(), '-m', 'playwright', 'install'])
        super().run()
    def _python_executable(self):
        import sys
        return sys.executable

setup(
    name="components-agents",
    version="0.1.0",
    description="Add your description here",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="",
    python_requires=">=3.12",
    packages=find_packages(),
    install_requires=[
        "arxiv>=2.2.0",
        "crawl4ai>=0.6.3",
        "duckdb>=1.3.0",
        "langchain-community>=0.3.25",
        "langchain-google-genai>=2.1.5",
        "langchain-nvidia-ai-endpoints>=0.3.10",
        "langchain-openai>=0.3.22",
        "langchain-tavily>=0.2.4",
        "langchain-xai>=0.2.4",
        "langchain[google-genai,groq,openai]>=0.3.25",
        "langgraph>=0.4.8",
        "notebook>=7.4.3",
        "pymongo>=4.13.1",
        "pymupdf>=1.26.1",
        "python-dotenv>=1.1.0",
        "rich>=14.0.0",
        "streamlit>=1.45.1",
        "streamlit-extras>=0.7.1",
        "textual>=3.4.0",
        "textual-dev>=1.7.0",
        "playwright"
    ],
    include_package_data=True,
    zip_safe=False,
    cmdclass={
        'install': CustomInstallCommand,
    },
)
