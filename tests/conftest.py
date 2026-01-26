import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.databases.db import SessionLocal, engine
from app.utils import security

from app.models import base, users

@pytest.fixture(scope='session')
def client():
    base.Base.metadata.drop_all(bind=engine)
    base.Base.metadata.create_all(bind=engine)
    # create an admin user
    db = SessionLocal()
    admin = users.User(email='admin@example.com', full_name='Admin', hashed_password=security.get_password_hash('adminpass'), role='admin')
    user = users.User(email='user@example.com', full_name='User', hashed_password=security.get_password_hash('userpass'), role='user')
    db.add(admin)
    db.add(user)
    db.commit()
    db.refresh(admin)
    db.refresh(user)
    db.close()
    with TestClient(app) as c:
        yield c

def get_token(client, username, password):
    r = client.post('/auth/token', data={'username': username, 'password': password})
    assert r.status_code == 200
    return r.json()['access_token']
