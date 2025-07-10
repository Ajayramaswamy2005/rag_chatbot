from fastapi import APIRouter, File, UploadFile, HTTPException
from app.services.vector_store import add_document, create_collection
from app.services.session_manager import set_last_collection
from app.utils.file_extractor import extract_text_from_file
import uuid

router = APIRouter()

@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    try:
        content = await file.read()
        text = extract_text_from_file(file.filename, content)

        if not text.strip():
            raise HTTPException(status_code=400, detail="Document is empty or unreadable.")

        collection_name = f"doc_{uuid.uuid4().hex[:6]}"
        create_collection(collection_name)

        doc_id = add_document(text, {"filename": file.filename}, collection_name)
        set_last_collection(collection_name)

        return {
            "status": "success",
            "filename": file.filename,
            "collection": collection_name
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
