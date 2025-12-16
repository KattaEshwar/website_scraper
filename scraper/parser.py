def parse_sections(soup, url):
    sections = []

    candidates = soup.find_all(["article", "main", "section", "header", "footer"])
    
    if not candidates:
        # Fallback 1: Look for common structural divs
        candidates = soup.find_all("div", id=lambda x: x and x.lower() in ["main", "content", "app", "root", "page", "container"])
    
    if not candidates and soup.body:
        # Fallback 2: Use the entire body
        candidates = [soup.body]

    for i, sec in enumerate(candidates):
        text = sec.get_text(" ", strip=True)

        if not text:
            continue

        sections.append({
            "id": f"section-{i}",
            "type": "section",
            "label": text[:50],
            "sourceUrl": url,
            "content": {
                "headings": [h.text for h in sec.find_all(["h1","h2","h3"])],
                "text": text,
                "links": [
                    {"text": a.text, "href": a.get("href")}
                    for a in sec.find_all("a", href=True)
                ],
                "images": [
                    {"src": img.get("src"), "alt": img.get("alt")}
                    for img in sec.find_all("img")
                ],
                "lists": [
                    [li.get_text(" ", strip=True) for li in lst.find_all("li")]
                    for lst in sec.find_all(["ul", "ol"])
                ],
                "tables": [
                    [
                        [cell.get_text(" ", strip=True) for cell in row.find_all(["th", "td"])]
                        for row in table.find_all("tr")
                    ]
                    for table in sec.find_all("table")
                ]
            },
            "rawHtml": str(sec)[:1000],
            "truncated": True
        })

    return sections
