# src/utils/web_search.py
import requests
from firecrawl import FirecrawlApp
from src.models.llm import get_llm
from src.config.settings import Settings
from datetime import datetime

class WebFallback:
    def __init__(self):
        self.serper_key = Settings.SERPER_API_KEY
        self.firecrawl = FirecrawlApp(api_key=Settings.FIRECRAWL_API_KEY) if Settings.FIRECRAWL_API_KEY else None
        self.llm = get_llm()

    def search_and_scrape(self, query: str) -> str:
        if not self.serper_key:
            return "Web search unavailable. Using static data only."

        # Serper search with financial focus
        payload = {"q": query + " site:finance.yahoo.com OR site:coingecko.com OR site:fred.stlouisfed.org", "num": 5}
        headers = {"X-API-KEY": self.serper_key, "Content-Type": "application/json"}
        response = requests.post("https://google.serper.dev/search", json=payload, headers=headers)
        if response.status_code != 200:
            return "Search error."

        results = response.json().get("organic", [])

        context = ""
        for item in results[:3]:
            url = item["link"]
            if self.firecrawl:
                try:
                    scraped = self.firecrawl.scrape_url(url, params={"onlyMainContent": True, "formats": ["markdown"]})
                    context += f"\n\nFrom {item['title']} ({url}):\n{scraped.get('markdown', '')[:3000]}"
                except Exception as e:
                    context += f"\n\nSnippet from {item['title']}: {item.get('snippet', '')}"

        # Generate response with LLM
        prompt = f"Use this current web context to answer factually. Include disclaimer: 'Data as of {datetime.now().strftime('%Y-%m-%d')}'. Context: {context}\n\nQuestion: {query}\nAnswer:"
        answer = self.llm.invoke(prompt).content

        # Add sources for transparency
        sources = [r["link"] for r in results]
        answer += f"\n\nSources: {', '.join(sources)}"

        return answer