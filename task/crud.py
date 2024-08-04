import chromadb
import random
import string

from fastapi import HTTPException
from sqlalchemy.exc import NoResultFound
from task.models import User, ActiveUser, engine
from sqlmodel import Session, select
from chromadb.config import Settings

chroma_client = chromadb.PersistentClient(path="vectordb/",
                                          settings=Settings(anonymized_telemetry=False))

def create_user(email, password):
    """Creates a new User in the database. Does not login automatically."""
    new_user = User(email=email, password=password)
    with Session(engine) as session:
        if not session.get(User, new_user.email):
            session.add(new_user)
            session.commit()
            session.refresh(new_user)
            return new_user
        else:
            raise HTTPException(409, "User already exists")


def login_user(email, password):
    """If username and password are correct, returns a token to use infinitely."""
    with Session(engine) as session:
        try:
            login_user = session.exec(select(User).where(User.email == email).where(User.password == password)).one()
        except NoResultFound:
            raise HTTPException(404, "Wrong email or password")
    
        try:
            old_login = session.exec(select(ActiveUser).where(ActiveUser.email == email)).one()
            return old_login
        except NoResultFound:
            new_login = ActiveUser(email=login_user.email, user=login_user)
            session.add(new_login)
            session.commit()
            session.refresh(new_login)
            return new_login


def get_current_user(token):
    with Session(engine) as session:
        try:
            current_user = session.exec(select(ActiveUser).where(ActiveUser.token == token)).one().user
            if not current_user:
                raise HTTPException(403, "Token is wrong")
            else:
                return current_user
        except NoResultFound:
            raise HTTPException(409, "token invalid.")


def create_document(collection_name, document, title):
    collection = chroma_client.get_or_create_collection(name=collection_name)
    ids = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(8))
    collection.add(documents=[document], ids=[ids], metadatas={"filename": title})
    return ids


def delete_document(collection_name, ids):
    collection = chroma_client.get_or_create_collection(name=collection_name)
    try:
        extension = collection.get(ids=[ids])["metadatas"][0]["filename"].split('.')[-1]
        collection.delete(ids=[ids])
    except IndexError:
        raise HTTPException(404, "ID not found")
    return extension


def get_documents(collection_name):
    collection = chroma_client.get_or_create_collection(name=collection_name)
    res = collection.get()
    return res


def read_document(collection_name, search_string):
    collection = chroma_client.get_or_create_collection(collection_name)
    result = collection.query(
        query_texts=[search_string],
        n_results=1
    )
    return result

