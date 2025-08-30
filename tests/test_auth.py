def test_auth_success(client):
    payload = {
        "name": "Mailovemisa",
        "email": "mailovemsia@example.com",
        "password": "123"
    }
    response = client.post('/api/v1/auth/register', json=payload)
    data = response.get_json()
    assert response.status_code == 201
    assert data['message'] == 'User registered successfully'
    assert 'user_id' in data

def test_login_success(client, registered_user):
    payload = {
        "email": "mailovemisa@example.com",
        "password": "123",
    }
    response = client.post('/api/v1/auth/login', json=payload)
    data = response.get_json()
    assert response.status_code == 200
    assert 'access_token' in data
    assert 'refresh_token' in data