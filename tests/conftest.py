from fastapi.testclient import TestClient
from app.main import app
import pytest
from app.database import get_db,Base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine


SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:supriya@localhost:5432/fastapi_test'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

testing_SessionLocal = sessionmaker(autocommit=False,autoflush=False,bind=engine)


@pytest.fixture()
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = testing_SessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture()
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    
@pytest.fixture()
def test_user(client):
    user_data ={
        "email":"emily@gmail.com",
        "password":"emily1234"
    }
    res = client.post("/users/",json=user_data)
    assert res.status_code == 201
    new_user = res.json()
    new_user['password'] = user_data['password']
    return new_user
