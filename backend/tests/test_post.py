import pytest

from datetime import datetime

from ..models.post import Post
from ..models.image import Image

@pytest.fixture
def post():
    return Post(
        'Twitter',
        'My first scheduled tweet',
        datetime.strptime('2020-11-01 17:0:00', '%Y-%m-%d %H:%M:%S')
    )

def test_app_to_dict(post):
    expected_value = 'Twitter'
    post_dict = post.to_dict()
    assert post_dict['app'] == expected_value

def test_text_to_dict(post):
    expected_value = 'My first scheduled tweet'
    post_dict = post.to_dict()
    assert post_dict['text'] == expected_value

def test_dt_scheduled_to_dict(post):
    expected_value = datetime.strptime('2020-11-01 17:0:00', '%Y-%m-%d %H:%M:%S')
    post_dict = post.to_dict()
    assert post_dict['dt_scheduled'] == expected_value

def test_push_image(post):
    image = Image(filename='image_test.jpg', location=None, people=None)
    image.create()
    post.push_image(image)
    assert image.id in [post_image.id for post_image in post.images]