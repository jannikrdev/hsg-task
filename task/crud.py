from task.models import User, ActiveUser, engine
from sqlmodel import Session

def create_user(email, password):
    new_user = User(email=email, password=password)
    with Session(engine) as session:
        if not session.get(User, new_user.email):
            session.add(new_user)
            session.commit()
        else:
            return None


def login_user(email, password):
    with Session(engine) as session:
        login_user = session.get(User, email)
        if not login_user:
            return None
        else:
            print(login_user)
            new_login = ActiveUser(user=login_user)
            session.add(new_login)
            session.commit()
            session.refresh(new_login)
            return new_login

