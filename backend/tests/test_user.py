import json, pytest, time

auth_token_ok_user = None

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

@pytest.fixture
def valid_login(client):
    time.sleep(1)
    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }
    body = {
        'email': 'rachel_green@friends.com', 
        'password': 'wewereNOTonabreak'
    }

    return client.post(
        '/user/login',
        data=json.dumps(body),
        headers=headers
    )

def test_create_user_should_return_status_code_201(client, data_ok_user):
    response = client.post(
        '/user', 
        data=json.dumps(data_ok_user['body']),
        headers=data_ok_user['headers']
    )
    
    assert response.status_code == 201

    response_json = response.get_json()
    assert response_json['message'] == 'User created successfully'

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
        ('rachel_green@friends.com', 'wewereNOTonabreak', 201),
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

    auth_token = response.get_json().get('auth_token')

    assert response.status_code == expected_status_code

    if response.status_code == 201:
        assert isinstance(auth_token, str)

        client.post(
            '/user/logout',
            headers=dict(
                Authorization='Bearer ' + auth_token
            )
        )

def test_get_user_status(client, valid_login):
    login = valid_login
    auth_token = login.get_json().get('auth_token')
    name = 'Rachel Green'
    email = 'rachel_green@friends.com'
    
    response = client.get(
        '/user/status',
        headers=dict(
            Authorization='Bearer ' + auth_token
        )
    )

    assert response.status_code == 200
    assert response.get_json().get('email') == email
    assert response.get_json().get('name') == name

    client.post(
        '/user/logout',
        headers=dict(
            Authorization=auth_token
        )
    )    

def test_user_logout_successfully(client, valid_login):
    login = valid_login

    auth_token = login.get_json().get('auth_token')

    logout_response = client.post(
        '/user/logout',
        headers=dict(
            Authorization='Bearer ' + auth_token
        )
    )

    assert logout_response.status_code == 201

def test_user_logout_fails_with_invalid_authorization_format(client, valid_login):
    """Test for authorization without Bearer prefix, but using valid token.
        A 401 error is expected.
    """
    login = valid_login

    auth_token = login.get_json().get('auth_token')

    logout_response = client.post(
        '/user/logout',
        headers=dict(
            Authorization=auth_token
        )
    )

    assert logout_response.status_code == 401

def test_user_logout_with_invalid_token(client):
    logout_response = client.post(
        '/user/logout',
        headers=dict(
            Authorization='Bearer invalidtestauthtoken'
        )
    )

    assert logout_response.status_code == 401
