from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
from app.scraper.parser import parse_sections
from datetime import datetime
import asyncio

def _sync_scrape_logic(url: str):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url)
        try:
            page.wait_for_load_state("networkidle", timeout=10000)
        except:
            pass # Continue even if networkidle not reached

        # scroll 3 times
        for _ in range(3):
            page.mouse.wheel(0, 3000)
            page.wait_for_timeout(1500)

        html = page.content()
        browser.close()
        return html

async def js_scrape(url: str):
    loop = asyncio.get_running_loop()
    # Run sync playwright in a separate thread to avoid asyncio loop issues on Windows
    html = await loop.run_in_executor(None, _sync_scrape_logic, url)

    soup = BeautifulSoup(html, "lxml")
    sections = parse_sections(soup, url)

    return {
        "result": {
            "url": url,
            "scrapedAt": datetime.utcnow().isoformat(),
            "meta": {},
            "sections": sections,
            "interactions": {
                "clicks": ["auto-scroll"],
                "scrolls": 3,
                "pages": [url]
            },
            "errors": []
        }
    }
