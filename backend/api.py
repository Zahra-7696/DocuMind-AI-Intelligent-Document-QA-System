from fastapi import FastAPI, UploadFile, File, Form
from pathlib import Path
import shutil

from backend.rag_pipeline import retriever_qa
from prometheus_client import Counter, generate_latest
from fastapi.responses import Response

app = FastAPI(title="DocuMind AI API")

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)


@app.get("/")
def root():
    return {"message": "DocuMind AI API is running"}


REQUEST_COUNT = Counter("app_requests_total", "Total requests")

@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type="text/plain")
@app.post("/ask")
async def ask(
    file: UploadFile = File(...),
    query: str = Form(...)
):
    file_path = UPLOAD_DIR / file.filename

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    answer = retriever_qa(str(file_path), query)
    return {"answer": answer}