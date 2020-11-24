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
    response = client.post(
        '/user', 
        data=json.dumps(data_ok_user['body']),
        headers=data_ok_user['headers']
    )
    
    assert response.status_code == 201

    response_json = response.get_json()
    assert isinstance(response_json['auth_token'], str)
    assert len(response_json['auth_token'])

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
    

def test_create_user_previously_created_should_return_user_already_exists_error(client, data_ok_user):
    response = client.post(
        '/user',
        data=json.dumps(data_ok_user['body']),
        headers=data_ok_user['headers']
    )

    assert response.status_code == 403
    assert response.get_json()['message'] == 'User already exists'

@pytest.mark.parametrize(
    'email, password, expected_status_code',
    [
        ('rachel_green@friends.com', 'wewereNOTonabreak', 200),
        ('rachel_green@friends.com', 'wewereonabreak', 401),
        ('rachel@friends.com', 'wewereonabreak', 401),
        ('rachel@friends.com', 'wewereNOTonabreak', 401),
    ]
)
def test_user_login(client, email, password, expected_status_code):
    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }
    body = {
        'email': email,
        'password': password
    }

    response = client.post(
        '/user/login',
        data=json.dumps(body),
        headers=headers
    )

    assert response.status_code == expected_status_code
