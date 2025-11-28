# isolates I/O and parsing from API logic; easy to extend to DOCX, HTML later

from pdfminer.high_level import extract_text
import tempfile

def extract_text_from_pdf(file_bytes: bytes) -> str:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(file_bytes)
        tmp_path = tmp.name
    
    text = extract_text(tmp_path)
    print(f"DEBUG: Extracted {len(text)} chars from PDF")
    return text


def extract_text_from_txt(file_bytes: bytes) -> str:
     return file_bytes.decode("utf-8", errors="ignore")

