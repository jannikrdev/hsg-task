from datetime import datetime
import os
from typing import Optional
from sqlmodel import Relationship, SQLModel, Field, create_engine, table, text
import random
import string

class User(SQLModel, table=True):
    email: str = Field(max_length=255, primary_key=True)
    password: str = Field(max_length=255)
    collection: str = Field(max_length=16, default=''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(16)))

    login: list["ActiveUser"] = Relationship(back_populates="user", passive_deletes="all")

class ActiveUser(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    login_time: datetime = Field(default=datetime.now(), nullable=False)
    token: str = Field(max_length=64, default=''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(64)))
    email: str | None = Field(default=None, foreign_key="user.email", ondelete="CASCADE")
    user: User = Relationship(back_populates="login")


engine = create_engine("sqlite:///db.sqlite3")

def create_db_and_tables():
    if os.path.isfile("db.sqlite3"):
        os.remove("db.sqlite3")

    SQLModel.metadata.create_all(engine)
    with engine.connect() as connection:
        connection.execute(text("PRAGMA foreign_keys=ON"))
