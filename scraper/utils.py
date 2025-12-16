from urllib.parse import urljoin, urlparse
import re


def is_valid_http_url(url: str) -> bool:
    """
    Validate that the URL uses http or https scheme.
    """
    try:
        parsed = urlparse(url)
        return parsed.scheme in ("http", "https")
    except Exception:
        return False


def make_absolute_url(base_url: str, link: str) -> str:
    """
    Convert relative URLs to absolute URLs.
    """
    if not link:
        return ""
    return urljoin(base_url, link)


def clean_text(text: str) -> str:
    """
    Normalize whitespace and remove junk characters.
    """
    if not text:
        return ""
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def truncate_html(html: str, max_length: int = 1000) -> tuple[str, bool]:
    """
    Truncate raw HTML safely and indicate truncation status.
    """
    if not html:
        return "", False

    if len(html) <= max_length:
        return html, False

    return html[:max_length], True


def guess_section_type(tag_name: str) -> str:
    """
    Guess section type based on HTML tag.
    """
    mapping = {
        "header": "hero",
        "nav": "nav",
        "footer": "footer",
        "section": "section",
        "main": "section"
    }
    return mapping.get(tag_name, "unknown")


def derive_label_from_text(text: str, word_limit: int = 7) -> str:
    """
    Generate a fallback label using first N words.
    """
    if not text:
        return "Section"

    words = text.split()
    return " ".join(words[:word_limit])
