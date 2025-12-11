import fitz # PyMuPDF
from typing import List




def extract_text_from_pdf(path: str) -> str:
"""Extract textual content from a PDF file. Returns a single string."""
doc = fitz.open(path)
pages = []
for page in doc:
pages.append(page.get_text("text"))
return "\n".join(pages)