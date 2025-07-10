from PyPDF2 import PdfReader
import docx
import io

def extract_text_from_file(filename: str, content: bytes) -> str:
    if filename.endswith(".pdf"):
        reader = PdfReader(io.BytesIO(content))
        return "\n".join(page.extract_text() for page in reader.pages if page.extract_text())
    
    elif filename.endswith(".docx"):
        doc = docx.Document(io.BytesIO(content))
        return "\n".join(para.text for para in doc.paragraphs if para.text.strip())
    
    elif filename.endswith(".txt"):
        return content.decode("utf-8")
    
    else:
        raise ValueError("Unsupported file type. Use PDF, DOCX, or TXT.")
