# pytest good practices: https://realpython.com/pytest-python-testing/

import pytest
import sys

from datetime import datetime

from backend.models.twitter_post import TwitterPost
#from backend.models.post_strategy import PostStrategy
from backend.models.image import Image

@pytest.fixture
def twitter_post():
    return TwitterPost(
        'My first scheduled tweet',
        datetime.strptime('2020-11-01 17:0:00', '%Y-%m-%d %H:%M:%S')
    )

def test_app_to_dict(twitter_post):
    expected_value = 'Twitter'
    post_dict = post.to_dict()
    assert post_dict['app'] == expected_value

def test_text_to_dict(twitter_post):
    expected_value = 'My first scheduled tweet'
    post_dict = post.to_dict()
    assert post_dict['text'] == expected_value

def test_dt_scheduled_to_dict(twitter_post):
    expected_value = datetime.strptime('2020-11-01 17:0:00', '%Y-%m-%d %H:%M:%S')
    post_dict = post.to_dict()
    assert post_dict['dt_scheduled'] == expected_value

def test_user(twitter_post):
    expected_value = 1
    assert expected_value == twitter_post.user

def test_get_inputs(twitter_post):
    expected_value = [
        {
            'input': 'name',
            'title': 'Name'
        },
        {
            'input': 'text',
            'name': 'Tweet'
        },
        {
            'input': 'dt_scheduled',
            'name': 'Date to post'
        }
    ]
    inputs = twitter_post.get_inputs()
    assert expected_value.sort() == inputs.sort()
