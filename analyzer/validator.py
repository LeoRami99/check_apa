from docx import Document

def count_lines(text):
    words = len(text.split())
    return max(1, round(words / 10))  # Asume aprox. 10 palabras por línea visual


def count_words(text):
    return len(text.split())

def validate_structure(path, expected_paragraphs, min_lines, max_lines, min_words, max_words):
    doc = Document(path)
    paragraphs = [p.text.strip() for p in doc.paragraphs if p.text.strip()]

    total_words = sum(count_words(p) for p in paragraphs)
    structure = {
        "total_words": total_words,
        "word_limit": f"{min_words}-{max_words}",
        "word_result": min_words <= total_words <= max_words,

        "total_paragraphs": len(paragraphs),
        "paragraph_result": len(paragraphs) == expected_paragraphs,

        "line_per_paragraphs": [],
    }

    for i, p in enumerate(paragraphs):
        lines = count_lines(p)
        valid = min_lines <= lines <= max_lines
        structure["line_per_paragraphs"].append({
            "paragraph": i+1,
            "lines": lines,
            "valid": valid
        })

    return structure
