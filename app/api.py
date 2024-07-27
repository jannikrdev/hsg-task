from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Document(BaseModel):
    pass

class User(BaseModel):
    pass


@app.get("/api/documents/")
async def list_documents():
    pass


@app.put("/api/documents/")
async def upload_document():
    pass


@app.delete("/api/documents/")
async def delete_document():
    pass

