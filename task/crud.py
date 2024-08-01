import chromadb
import random
import string
from task.models import User, ActiveUser, engine
from sqlmodel import Session, select
from chromadb.config import Settings

chroma_client = chromadb.Client(Settings(anonymized_telemetry=False))

def create_user(email, password):
    new_user = User(email=email, password=password)
    with Session(engine) as session:
        if not session.get(User, new_user.email):
            session.add(new_user)
            session.commit()
            session.refresh(new_user)
            return new_user
        else:
            return None


def login_user(email, password):
    with Session(engine) as session:
        login_user = session.exec(select(User).where(User.email == email and User.password == password)).first()
        if not login_user:
            return None
        else:
            new_login = ActiveUser(email=login_user.email, user=login_user)
            session.add(new_login)
            session.commit()
            session.refresh(new_login)
            return new_login


def get_current_user(token):
    with Session(engine) as session:
        current_user = session.exec(select(ActiveUser).where(ActiveUser.token == token)).one().user
        if not current_user:
            return None
        else:
            return current_user


def create_document(collection_name, document):
    collection = chroma_client.get_or_create_collection(name=collection_name)
    collection.add(documents=[document], ids=[''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(8))])


def read_document(collection_name, search_string):
    collection = chroma_client.get_or_create_collection(collection_name)
    result = collection.query(
        query_texts=[search_string],
        n_results=1
    )
    return result
