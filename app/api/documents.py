from fastapi import APIRouter, UploadFile, File, HTTPException
import uuid, os

router = APIRouter()

UPLOAD_DIR = "storage/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/documents/upload")
async def upload_document(file: UploadFile = File(...), metadata: str = None):
    doc_id = str(uuid.uuid4())
    path = os.path.join(UPLOAD_DIR, f"{doc_id}_{file.filename}")
    with open(path, "wb") as f:
        f.write(await file.read())
    # persist metadata to SQLite later
    return {"document_id": doc_id, "filename": file.filename, "path": path}
