import httpx
from bs4 import BeautifulSoup
from app.scraper.parser import parse_sections
from datetime import datetime

def static_scrape(url: str):
    res = httpx.get(url, timeout=15)
    soup = BeautifulSoup(res.text, "lxml")

    meta = {
        "title": soup.title.text if soup.title else "",
        "description": "",
        "language": soup.html.get("lang") if soup.html else "",
        "canonical": None
    }

    sections = parse_sections(soup, url)

    return {
        "result": {
            "url": url,
            "scrapedAt": datetime.utcnow().isoformat(),
            "meta": meta,
            "sections": sections,
            "interactions": {
                "clicks": [],
                "scrolls": 0,
                "pages": [url]
            },
            "errors": []
        }
    }
