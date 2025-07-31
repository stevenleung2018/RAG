import os
import tempfile
import fitz  # PyMuPDF
import pytest
from src.read_pdf import read_pdf

def create_sample_pdf(text, file_path):
    doc = fitz.open()
    page = doc.new_page()
    page.insert_text((72, 72), text)
    doc.save(file_path)
    doc.close()

def test_read_pdf_returns_text():
    sample_text = "Hello, PDF!"
    fd, path = tempfile.mkstemp(suffix=".pdf")
    os.close(fd)  # Close the file descriptor so PyMuPDF can write to it
    try:
        create_sample_pdf(sample_text, path)
        result = read_pdf(path)
        assert sample_text in result
    finally:
        os.remove(path)

def test_read_pdf_empty_pdf():
    # Create a PDF with a blank page
    fd, path = tempfile.mkstemp(suffix=".pdf")
    os.close(fd)
    try:
        doc = fitz.open()
        doc.new_page()  # Add a blank page
        doc.save(path)
        doc.close()
        result = read_pdf(path)
        assert result.strip() == ""
    finally:
        os.remove(path)

def test_read_pdf_invalid_path():
    with pytest.raises(Exception):
        read_pdf("nonexistent_file.pdf")