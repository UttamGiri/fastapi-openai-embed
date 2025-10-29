from fastapi import FastAPI, UploadFile, Form
from fastapi.responses import JSONResponse
from app.services.embedding_service import EmbeddingService

app = FastAPI(title="FastAPI + OpenAI Embedding API")

service = EmbeddingService()  # Instantiate once

@app.post("/embed-file/")
async def embed_file(file: UploadFile):
    try:
        file_bytes = await file.read()
        file_path = service.create_embedding(file_bytes, file.filename)
        return {"status": "success", "embedding_file": file_path.split("/")[-1]}
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)

@app.post("/query/")
async def query_embedding(query: str = Form(...), embed_file: str = Form(...)):
    try:
        return service.query_embedding(query, embed_file)
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)
