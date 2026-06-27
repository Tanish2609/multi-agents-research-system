from langchain.tools import tool
from langchain_mistralai import ChatMistralAI
import requests
from bs4 import BeautifulSoup
from tavily import TavilyClient
import os
from rich import print
from dotenv import load_dotenv

load_dotenv()

tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))


@tool
def web_search(query : str) -> str:
    """Searches the web for recent and reliable and information on a topic. 
    Returns titles , URLs and snippet"""

    results = tavily.search(
        query = query , 
        max_results= 5,
        search_depth="basic")
    
    out = []

    for r in results['results']:
        out.append(
            f"Title : {r['title']}\nURL :{r['url']}\nContent :{r['content'][:300]}\n"
        )
    return "\n--------------------------\n".join(out)


@tool
def scrape_url(url : str) -> str:
    """Scrape and return clean text content from a given url for deeper reading."""
    try:
        resp = requests.get(url , timeout = 8 , headers={"User Agent" : "Mozilla/5.0"})
        soup = BeautifulSoup(resp.text , "html.parser")
        for tag in soup(["script" , 'style' , 'nav' , 'footer']):
            tag.decompose()
        return soup.get_text(separator = " " , strip = True)[:3000]
    except Exception as e:
        return f"Could not scrape url : {str(e)}"
    