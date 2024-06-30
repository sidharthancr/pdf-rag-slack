import fitz  # PyMuPDF
import re

"""
Extracts and preprocesses text from a PDF file.

Parameters:
- pdf_path (str): The file path of the PDF from which to extract text.

Returns:
- str: The extracted and preprocessed text.
"""
def extract_text_from_pdf(pdf_path):
    try:
        # Use context manager to ensure the PDF file is properly closed after processing
        with fitz.open(pdf_path) as doc:
            text = ""
            for page in doc:
                text += page.get_text()
            # Preprocess text: replace multiple whitespace characters with a single space
            text = re.sub(r'\s+', ' ', text)
        return text
    except Exception as e:
        raise Exception(f"Error extracting text from PDF: {e}")