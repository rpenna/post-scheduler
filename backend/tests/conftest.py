import pytest

from src.application import create_app

@pytest.fixture
def app():
    return create_app('test')
