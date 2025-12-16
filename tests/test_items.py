from .conftest import get_token

def test_create_item(client):
    token = get_token(client, 'user@example.com', 'userpass')
    r = client.post('/items/', json={'title':'Item1','description':'desc','price':9.99}, headers={'Authorization':f'Bearer {token}'})
    assert r.status_code == 200
    assert r.json()['title'] == 'Item1'

def test_list_items_pagination_and_filter(client):
    token = get_token(client, 'user@example.com', 'userpass')
    # create multiple items
    for i in range(1,16):
        client.post('/items/', json={'title':f'Item{i}','description':'x','price':i}, headers={'Authorization':f'Bearer {token}'})
    r = client.get('/items/?page=2&size=5', headers={'Authorization':f'Bearer {token}'})
    assert r.status_code == 200
    assert len(r.json()) == 5
    r2 = client.get('/items/?search=Item1', headers={'Authorization':f'Bearer {token}'})
    assert r2.status_code == 200
    assert any('Item1' in it['title'] for it in r2.json())

def test_update_delete_item_permissions(client):
    token_user = get_token(client, 'user@example.com', 'userpass')
    token_admin = get_token(client, 'admin@example.com', 'adminpass')
    # create by user
    r = client.post('/items/', json={'title':'Owned','description':'x','price':1}, headers={'Authorization':f'Bearer {token_user}'})
    item = r.json()
    # another user (admin) can edit
    r2 = client.patch(f"/items/{item['id']}", json={'price':2}, headers={'Authorization':f'Bearer {token_admin}'})
    assert r2.status_code == 200
    # delete by owner
    r3 = client.delete(f"/items/{item['id']}", headers={'Authorization':f'Bearer {token_user}'})
    assert r3.status_code == 204