import os
from pypdf import PdfReader
from docx import Document
import pytesseract
from pdf2image import convert_from_path
from PIL import Image
from modules.transcriber import transcribe_audio

def extract_text_from_file(file_path, file_type):
    """
    Extract text from a file based on its type.
    
    Args:
        file_path (str): Path to the file.
        file_type (str): Type of the file (pdf, docx, image, audio).
        
    Returns:
        str: Extracted text.
    """
    try:
        if file_type == 'pdf':
            return _extract_from_pdf(file_path)
        elif file_type == 'docx':
            return _extract_from_docx(file_path)
        elif file_type in ['jpg', 'jpeg', 'png']:
            return _extract_from_image(file_path)
        elif file_type in ['mp3', 'wav', 'm4a', 'ogg']:
            return transcribe_audio(file_path)
        else:
            return "Formato no soportado."
    except Exception as e:
        return f"Error al procesar el archivo: {e}"

def _extract_from_pdf(file_path):
    text = ""
    try:
        reader = PdfReader(file_path)
        for page in reader.pages:
            text += page.extract_text() + "\n"
        
        # If text is empty, try OCR (scanned PDF)
        if not text.strip():
            print("PDF seems to be scanned. Attempting OCR...")
            images = convert_from_path(file_path)
            for i, image in enumerate(images):
                text += pytesseract.image_to_string(image) + "\n"
                
    except Exception as e:
        print(f"Error reading PDF: {e}")
        raise e
    return text

def _extract_from_docx(file_path):
    doc = Document(file_path)
    text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
    return text

def _extract_from_image(file_path):
    image = Image.open(file_path)
    text = pytesseract.image_to_string(image)
    return text
