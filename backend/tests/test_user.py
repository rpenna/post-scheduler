import json

def test_create_user_should_return_status_code_201(client):
    mimetype = 'application/json'

    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }

    data = {
        'name': 'Rachel Green',
        'email': 'rachel_green@friends.com',
        'password': 'wewereNOTonabreak'
    }

    assert client.post(
        '/user', 
        data=json.dumps(data),
        headers=headers
    ).status_code == 201
