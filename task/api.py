from fastapi import FastAPI, File, HTTPException, UploadFile
from typing import Optional, Annotated

from fastapi.responses import FileResponse, HTMLResponse
import task.crud as crud

app = FastAPI()


@app.post("/api/documents/")
async def upload_document(document: UploadFile | None = None, token: str | None = None):
    collection = "SUDO" if token is None else crud.get_current_user(token).collection
    if not document:
        return HTTPException(404, "File not provided")
    
    accepted = ["text/plain", "text/markdown"]
    if not document.content_type in accepted:
        return HTTPException(422, "Cannot process this type of file")

    res = crud.create_document(collection, str(document.file.read()), document.filename)

    with open(f"files/{res}.{document.filename.split('.')[-1]}", "wb") as out_file:
        content = await document.read()
        out_file.write(content)
    
    return {"created with id:": res}

@app.get("/api/documents/")
async def get_documents(token: str | None = None):
    collection = "SUDO" if token is None else crud.get_current_user(token).collection
    res = crud.get_documents(collection)
    return {"results": [i["filename"] for i in res["metadatas"]],
            "contents": res["documents"]}
    
@app.get("/api/documents/{text}")
async def get_document(text: str, token: str | None = None):
    collection = "SUDO" if token is None else crud.get_current_user(token).collection
    res = crud.read_document(collection, text)
    file = f"files/{res['ids'][0][0]}.{res['metadatas'][0][0]['filename'].split('.')[-1]}"
    print(file)
    return FileResponse(f"files/{res['ids'][0][0]}.{res['metadatas'][0][0]['filename'].split('.')[-1]}")

