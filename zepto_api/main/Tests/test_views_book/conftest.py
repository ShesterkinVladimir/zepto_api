import pytest
from main.models import Book
from django.urls import reverse


@pytest.fixture
def api_client():
    from rest_framework.test import APIClient
    return APIClient()


@pytest.fixture(autouse=True)
def insert_book(api_client):
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
    library = api_client.post(url, data=data, format='json')

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
    authors = api_client.post(url, data=data, format='json')

    url = reverse('book')
    data = [{
        'name': 'book-1',
        'year': 2001,
        'library': library.data[0].get('id'),
        'authors': [authors.data[0].get('id'), authors.data[1].get('id')]
    },
        {
        'name': 'book-2',
        'year': 2002,
        'library': library.data[1].get('id'),
        'authors': [authors.data[0].get('id'), authors.data[1].get('id')]
        }
    ]
    return api_client.post(url, data=data, format='json')


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
