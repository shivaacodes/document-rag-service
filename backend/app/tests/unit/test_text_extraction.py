from app.services.text_extraction import extract_text_from_pdf, extract_text_from_txt
from unittest.mock import patch, MagicMock

def test_extract_text_from_txt():
    content = b"Hello World"
    text = extract_text_from_txt(content)
    assert text == "Hello World"

def test_extract_text_from_pdf(sample_pdf_bytes):
    # We mock pdfminer.high_level.extract_text to avoid writing to disk or needing complex PDF parsing in tests
    with patch("app.services.text_extraction.extract_text") as mock_extract:
        mock_extract.return_value = "Hello World"
        
        text = extract_text_from_pdf(sample_pdf_bytes)
        
        assert text == "Hello World"
        mock_extract.assert_called_once()
