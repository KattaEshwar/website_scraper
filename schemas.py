from pydantic import BaseModel, HttpUrl
from typing import List, Optional, Dict, Any


# ---------- Core Content Models ----------

class Link(BaseModel):
    text: str
    href: HttpUrl


class Image(BaseModel):
    src: HttpUrl
    alt: Optional[str] = ""


class ErrorItem(BaseModel):
    message: str
    phase: str


# ---------- Section Content ----------

class SectionContent(BaseModel):
    headings: List[str]
    text: str
    links: List[Link]
    images: List[Image]
    lists: List[List[str]]
    tables: List[Any]


# ---------- Section ----------

class Section(BaseModel):
    id: str
    type: str
    label: str
    sourceUrl: HttpUrl
    content: SectionContent
    rawHtml: str
    truncated: bool


# ---------- Interactions ----------

class Interactions(BaseModel):
    clicks: List[str]
    scrolls: int
    pages: List[HttpUrl]


# ---------- Meta ----------

class Meta(BaseModel):
    title: str
    description: str
    language: str
    canonical: Optional[HttpUrl]


# ---------- Result ----------

class ScrapeResult(BaseModel):
    url: HttpUrl
    scrapedAt: str
    meta: Meta
    sections: List[Section]
    interactions: Interactions
    errors: List[ErrorItem]


# ---------- API Response ----------

class ScrapeResponse(BaseModel):
    result: ScrapeResult
