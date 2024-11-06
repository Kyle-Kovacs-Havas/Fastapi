from typing import Annotated
from fastapi import FastAPI, Depends
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import  declarative_base
from app.main import app
from app import schemas
import pytest
from app.config import settings
from app.database import get_db, Base
from alembic import command

#SQLALCHEMY_DATABASE_URL = 'postgres://postgres:fever364@localhost@5432/fastapi_test'
#SQLALCHEMY_DATABASE_URL = 'postgresql://<username>:<password>@<ip-address/hostname>/<database_name>'
SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_session():
    with TestingSessionLocal() as session:
        yield session

SessionLocal = Annotated[Session, Depends(get_session)]


@pytest.fixture()
def session():
    #run our code before we return our test
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()    #Base.metadata.drop_all(bind=engine) could put it here if you want
    #run our code after the test finishes


@pytest.fixture()
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
