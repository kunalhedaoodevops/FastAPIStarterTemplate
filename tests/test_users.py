from .conftest import get_token

def test_admin_can_create_user(client):
    token = get_token(client, 'admin@example.com', 'adminpass')
    r = client.post('/users/', json={'email':'new@example.com','full_name':'New','password':'newpass','role':'user'}, headers={'Authorization':f'Bearer {token}'})
    assert r.status_code == 200
    data = r.json()
    assert data['email'] == 'new@example.com'

def test_non_admin_cannot_create_user(client):
    token = get_token(client, 'user@example.com', 'userpass')
    r = client.post('/users/', json={'email':'x@example.com','full_name':'X','password':'xpass'}, headers={'Authorization':f'Bearer {token}'})
    assert r.status_code == 403

def test_read_users_list(client):
    token = get_token(client, 'admin@example.com', 'adminpass')
    r = client.get('/users/', headers={'Authorization':f'Bearer {token}'})
    assert r.status_code == 200
    assert isinstance(r.json(), list)

def test_get_me(client):
    token = get_token(client, 'user@example.com', 'userpass')
    r = client.get('/users/me', headers={'Authorization':f'Bearer {token}'})
    assert r.status_code == 200
    assert r.json()['email'] == 'user@example.com'