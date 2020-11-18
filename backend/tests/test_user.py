import json, pytest

@pytest.fixture
def data_ok_user():
    mimetype = 'application/json'

    return {
        'headers': {
            'Content-Type': mimetype,
            'Accept': mimetype
        },
        'body': {
            'name': 'Rachel Green',
            'email': 'rachel_green@friends.com',
            'password': 'wewereNOTonabreak'
        }
    }

@pytest.fixture
def data_user_invalid_email():
    mimetype = 'application/json'

    return {
        'headers': {
            'Content-Type': mimetype,
            'Accept': mimetype
        },
        'body': {
            'name': 'Rachel Green',
            'email': 'rachel_green@friends@com',
            'password': 'wewereNOTonabreak'
        }
    }

@pytest.fixture
def data_user_invalid_password():
    mimetype = 'application/json'

    return {
        'headers': {
            'Content-Type': mimetype,
            'Accept': mimetype
        },
        'body': {
            'name': 'Rachel Green',
            'email': 'rachel_green@friends.com',
            'password': 12345
        }
    }

@pytest.fixture
def data_user_password_too_short():
    mimetype = 'application/json'

    return {
        'headers': {
            'Content-Type': mimetype,
            'Accept': mimetype
        },
        'body': {
            'name': 'Rachel Green',
            'email': 'rachel_green@friends.com',
            'password': 'wewe'
        }
    }

def test_create_user_should_return_status_code_201(client, data_ok_user):
    assert client.post(
        '/user', 
        data=json.dumps(data_ok_user['body']),
        headers=data_ok_user['headers']
    ).status_code == 201

def test_create_user_should_return_403_status_code_when_email_is_invalid(client, data_user_invalid_email):
    assert client.post(
        '/user',
        data=json.dumps(data_user_invalid_email['body']),
        headers=data_user_invalid_email['headers']
    ).status_code == 403

def test_create_user_should_return_an_error_message_when_email_is_invalid(client, data_user_invalid_email):
    assert client.post(
        '/user',
        data=json.dumps(data_user_invalid_email['body']),
        headers=data_user_invalid_email['headers']
    ).get_json()['message'] == 'Unrecognized e-mail format'

def test_create_user_should_return_403_status_code_when_password_is_invalid(client, data_user_invalid_password):
    assert client.post(
        '/user',
        data=json.dumps(data_user_invalid_password['body']),
        headers=data_user_invalid_password['headers']
    ).status_code == 403

def test_create_user_should_return_an_error_message_when_password_is_invalid(client, data_user_invalid_password): 
    print(client.post(
        '/user',
        data=json.dumps(data_user_invalid_password['body']),
        headers=data_user_invalid_password['headers']
    ).get_json())
    assert client.post(
        '/user',
        data=json.dumps(data_user_invalid_password['body']),
        headers=data_user_invalid_password['headers']
    ).get_json()['message'] == 'Invalid password type'

def test_create_user_should_return_403_status_code_when_password_is_too_short(client, data_user_password_too_short):
    assert client.post(
        '/user',
        data=json.dumps(data_user_password_too_short['body']),
        headers=data_user_password_too_short['headers']
    ).status_code == 403

def test_create_user_should_return_an_error_message_when_password_is_too_short(client, data_user_password_too_short):
    assert client.post(
        '/user',
        data=json.dumps(data_user_password_too_short['body']),
        headers=data_user_password_too_short['headers']
    ).get_json()['message'] == 'Password is too short'


def test_create_user_should_not_return_its_auth_token_when_there_is_an_error(client, data_user_password_too_short):
    response = client.post(
        '/user',
        data=json.dumps(data_user_password_too_short['body']),
        headers=data_user_password_too_short['headers']
    ).get_json()
    
    assert response.get('auth_token') is None

def test_create_user_should_return_its_auth_token(client, data_ok_user):
    response = client.post(
        '/user',
        data=json.dumps(data_ok_user['body']),
        headers=data_ok_user['headers']
    ).get_json()
    
    assert isinstance(response['auth_token'], str) and len(response['auth_token'])
