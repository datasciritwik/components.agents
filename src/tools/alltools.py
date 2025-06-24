from langchain_tavily import TavilySearch
from langchain_core.tools import tool
import asyncio
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig
from crawl4ai.markdown_generation_strategy import DefaultMarkdownGenerator

@tool
def websearch(query: str)-> str:
    """
    Performs a web search using the TavilySearch API and returns a formatted summary of the top results.
    Args:
        query (str): The search query string to look up on the web.
    Returns:
        str: A formatted string containing the title, URL, and snippet of each top result, or "No results found." if there are no results.
    """
    tavily_search = TavilySearch(max_results=10)
    results = tavily_search.invoke(query)
    
    if not results:
        return "No results found."
    
    formatted = "\n\n".join(
    f"Title: {r.get('title', '')}\nURL: {r.get('url', '')}\nSnippet: {r.get('content', '')}"
    for r in results['results']
    )
    print(formatted)
    return formatted

@tool
def webcrawl(url:str) -> str:
    """
    Crawl a web page and return its structured markdown content using crawl4ai.
    Args:
        url (str): The URL of the web page to crawl.
    Returns:
        str: The structured markdown content of the web page, or "No markdown found." if extraction fails.
    """
    md_generator = DefaultMarkdownGenerator(
        options={
            "ignore_links": False,
            "escape_html": False,
        }
    )

    config = CrawlerRunConfig(
        markdown_generator=md_generator
    )
    async def crawl():
        async with AsyncWebCrawler() as crawler:
            result = await crawler.arun(url=url, config=config)
            return result.markdown if hasattr(result, "markdown") else "No markdown found."
    
    return asyncio.run(crawl())

if __name__ == '__main__':
    # Run tests for the functions and print outputs

    # Test websearch
    search_query = "Python programming language"
    search_result = websearch(search_query)
    print("Websearch Result:\n", search_result)

    # Test webcrawl
    test_url = "https://www.python.org/"
    crawl_result = webcrawl(test_url)
    print("\nWebcrawl Result:\n", crawl_result)