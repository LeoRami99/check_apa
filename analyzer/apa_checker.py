import re
from docx import Document

APA_PATTERN = r"\(([^)]+?,\s?\d{4})\)"

def check_apa_citations(path):
    doc = Document(path)
    citations = []
    for i, para in enumerate(doc.paragraphs):
        matches = re.findall(APA_PATTERN, para.text)
        for match in matches:
            parts = match.split(",")
            if len(parts) != 2:
                citations.append({
                    "paragraph": i + 1,
                    "citation": match,
                    "valid": False,
                    "error": "Formato incorrecto, revise coma o año"
                })
            else:
                citations.append({
                    "paragraph": i + 1,
                    "citation": match,
                    "valid": True
                })
    return citations
