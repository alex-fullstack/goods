import pytest


@pytest.fixture
def user_client():
    from rest_framework.test import APIClient

    client = APIClient()
    return client
