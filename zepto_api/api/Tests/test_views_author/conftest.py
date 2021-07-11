import pytest
from api.models import Author
from django.urls import reverse


@pytest.fixture
def api_client():
    from rest_framework.test import APIClient
    return APIClient()


@pytest.fixture(autouse=True)
def insert_author(api_client):
    url = reverse('author')
    data = [{
        'name': 'Murakami',
        'birth_date': '2021-12-12'
    },
        {
        'name': 'Pelevin',
        'birth_date': '1999-09-10'
        }
    ]
    return api_client.post(url, data=data, format='json')
