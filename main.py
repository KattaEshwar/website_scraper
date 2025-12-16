import sys
import asyncio
from fastapi import FastAPI, Request

if sys.platform.startswith("win"):
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.scraper.static import static_scrape
from app.scraper.js import js_scrape
from app.exporter import generate_pdf
from fastapi.responses import Response

from pathlib import Path

app = FastAPI()
BASE_DIR = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

@app.get("/healthz")
def health():
    return {"status": "ok"}

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/scrape")
async def scrape(payload: dict):
    url = payload.get("url")

    result = static_scrape(url)

    # heuristic: fallback if text is too small
    if not result["result"]["sections"] or len(result["result"]["sections"][0]["content"]["text"]) < 200:
        result = await js_scrape(url)

    return result

@app.post("/export/pdf")
def export_pdf(data: dict):
    pdf_bytes = generate_pdf(data)
    return Response(content=pdf_bytes, media_type="application/pdf", headers={"Content-Disposition": "attachment; filename=report.pdf"})

if __name__ == "__main__":
    import uvicorn
    # Using "main:app" string to enable reload support
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
