import os
from fastapi import FastAPI, File, HTTPException, UploadFile
from typing import Optional, Annotated

from fastapi.responses import FileResponse, HTMLResponse
from pydantic import BaseModel
from sqlalchemy.exc import NoResultFound
import task.crud as crud


class User(BaseModel):
    username: str
    password: str


app = FastAPI()

@app.post("/api/documents/")
async def upload_document(document: UploadFile | None = None, token: str | None = None):
    """Creates a Document in the vector database. If a token is provided, it is user-based, otherwise,
    user "SUDO" is being used for general purpose.
    See the /docs for how to use it.
    """
    collection = "SUDO" if token is None else crud.get_current_user(token).collection
    if not document:
        return HTTPException(404, "File not provided")
    
    accepted = ["text/plain", "text/markdown"]
    if not document.content_type in accepted:
        return HTTPException(422, "Cannot process this type of file")

    content = str(document.file.read())
    res = crud.create_document(collection, content, document.filename)

    with open(f"files/{res}.{document.filename.split('.')[-1]}", "w") as out_file:
        out_file.write(content)
    
    return {"created with id:": res}


@app.get("/api/documents/")
async def get_documents(token: str | None = None):
    """Lists all the documents which were uploaded. See the /docs for details."""
    collection = "SUDO" if token is None else crud.get_current_user(token).collection
    res = crud.get_documents(collection)
    return {"results": [i["filename"] for i in res["metadatas"]],
            "contents": res["documents"]}
    

@app.get("/api/documents/query")
async def get_document(text: str, token: str | None = None):
    """Searches through the uploaded documents, if token is provided, on a user-basis. See /docs for details.
    If a document was found, it returns the whole file!"""
    collection = "SUDO" if token is None else crud.get_current_user(token).collection
    res = crud.read_document(collection, text)
    try:
        file = f"files/{res['ids'][0][0]}.{res['metadatas'][0][0]['filename'].split('.')[-1]}"
    except IndexError:
        raise HTTPException(404, "Nothing found. Have you uploaded any documents yet?")
    return FileResponse(file)


@app.delete("/api/documents/")
async def delete_document(ids: str, token: str | None = None):
    """Deletes a document based on ID. See /docs for details."""
    collection = "SUDO" if token is None else crud.get_current_user(token).collection
    extension = crud.delete_document(collection, ids)
    os.remove(f"files/{ids}.{extension}")
    return {"deleted": ids}


##### USER MANAGEMENT #####
@app.put("/api/users/")
async def user_login(user: User):
    """Logs in an existing user. User must be created first via the /api/users/ endpoint. See /docs for details."""
    token = crud.login_user(user.username, user.password).token
    return {"Successful login. Your token:": token}


@app.post("/api/users/")
async def user_create(user: User):
    """Creates a new user. Currently, username can be anything, it does not need to be an email."""
    crud.create_user(user.username, user.password)
    return {"created": user.username}

