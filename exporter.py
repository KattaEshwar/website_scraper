from fpdf import FPDF
import io

class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'Lyftr Scraper Report', 0, 1, 'C')

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

def generate_pdf(data: dict) -> bytes:
    pdf = PDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    result = data.get("result", {})
    url = result.get("url", "Unknown URL")
    
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(0, 10, f"Scrape Results for: {url}", 0, 1)
    pdf.ln(5)

    sections = result.get("sections", [])
    if not sections:
        pdf.set_font("Arial", size=12)
        pdf.cell(0, 10, "No sections found.", 0, 1)
    
    for section in sections:
        # Section Label
        pdf.set_font("Arial", 'B', 12)
        # Handle unicode characters that fpdf might struggle with
        label = section.get("label", "Section").encode('latin-1', 'replace').decode('latin-1')
        pdf.cell(0, 10, label, 0, 1)
        
        content = section.get("content", {})
        
        # Text
        text = content.get("text", "")
        if text:
            pdf.set_font("Arial", size=10)
            pdf.multi_cell(0, 5, text.encode('latin-1', 'replace').decode('latin-1'))
            pdf.ln(2)
        
        # Lists
        lists = content.get("lists", [])
        if lists:
            pdf.set_font("Arial", 'B', 10)
            pdf.cell(0, 5, "Lists:", 0, 1)
            pdf.set_font("Arial", size=10)
            for lst in lists:
                for item in lst:
                    pdf.cell(5) # Indent
                    pdf.cell(0, 5, f"- {item}".encode('latin-1', 'replace').decode('latin-1'), 0, 1)
                pdf.ln(1)
        
        # Tables
        tables = content.get("tables", [])
        if tables:
            pdf.set_font("Arial", 'B', 10)
            pdf.cell(0, 5, "Tables:", 0, 1)
            pdf.set_font("Arial", size=10)
            for table in tables:
                for row in table:
                    row_text = " | ".join(row)
                    pdf.cell(5)
                    pdf.multi_cell(0, 5, row_text.encode('latin-1', 'replace').decode('latin-1'))
                pdf.ln(1)
                
        pdf.ln(5)

    return pdf.output(dest='S').encode('latin-1')
