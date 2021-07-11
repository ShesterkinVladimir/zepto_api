import pytest
from api.models import Library
from django.urls import reverse


@pytest.fixture
def api_client():
    from rest_framework.test import APIClient
    return APIClient()


@pytest.fixture(autouse=True)
def insert_library(api_client):
    url = reverse('library')
    data = [{
        'address': 'Sovetskaya',
        'book_capacity': 1000,
        'name': 'Nekrasova'
    },
        {
            'address': 'Sovetskaya-1',
            'book_capacity': 10000,
            'name': 'Nekrasova-1'
        }
    ]
    return api_client.post(url, data=data, format='json')
