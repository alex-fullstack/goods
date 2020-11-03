import pytest


@pytest.fixture
def photo():
    return open('tests/fixtures/photo-test.png', 'rb')


@pytest.fixture
def photo_save_path():
    return 'media/advertisements/photo-test.png'
