import pytest

from main.models import Book
from django.urls import reverse


# tests for library
@pytest.mark.django_db
def test_library_get(api_client):
    url = reverse('book')
    response = api_client.get(url)
    assert response.status_code == 200
    assert response.data[0].get('name') == 'book-1'
    assert len(response.data[1].get('authors')) == 2


@pytest.mark.django_db
@pytest.mark.parametrize(
    'name, year, status_code', [
        ('book-1', 1020, 201),
        (None, 1000,  400),
        ('book-1', None, 201),
        (None, None, 400)

    ],
)
def test_book_post(name, year, status_code, api_client, insert_library, insert_author):

    url = reverse('book')
    data = {
        'name': name,
        'year': year,
        'library': insert_library.data[0].get('id'),
        'authors': [insert_author.data[0].get('id'), insert_author.data[1].get('id')]
    }
    response = api_client.post(url, data=data, format='json')
    assert response.status_code == status_code


@pytest.mark.django_db
@pytest.mark.parametrize(
    'name, year,  status_code', [
        (['book-1', 'book-2'], [1000, 1020], 201),
        (['book-1', 'book-2'], [None, None],  201),
        ([None, None], [1000, 1020], 400),

    ],
)
def test_book_post_multiple(name, year, status_code, api_client, insert_library, insert_author):

    url = reverse('book')
    data = [{
            'name': name[0],
            'year': year[0],
            'library': insert_library.data[0].get('id'),
            'authors': [insert_author.data[0].get('id'), insert_author.data[1].get('id')]
    },
        {
            'name': name[1],
            'year': year[1],
            'library': insert_library.data[0].get('id'),
            'authors': [insert_author.data[0].get('id'), insert_author.data[1].get('id')]
        }
    ]
    response = api_client.post(url, data=data, format='json')
    assert response.status_code == status_code


@pytest.mark.django_db
def test_book_id_get(api_client):
    url = reverse('book_pk', kwargs={'pk':  api_client.get(reverse('book')).data[0].get('id')})
    response = api_client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
@pytest.mark.parametrize(
        'name, year, status_code', [
            ('book-20', 1020, 200),
            (None, 1000, 400),
            ('book-20', None, 200),
            (None, None, 400)

    ],
)
def test_book_id_put(name, year, status_code, api_client, insert_library, insert_author, insert_book):

    response = insert_book
    url = reverse('book_pk', kwargs={'pk':  response.data[0].get('id')})
    data = {
        'name': name,
        'year': year,
        'library': insert_library.data[1].get('id'),
        'authors': [insert_author.data[1].get('id')]
    }
    response = api_client.put(url, data=data, format='json')
    assert response.status_code == status_code
    if status_code == 200:
        assert response.data.get('name') == name
        assert len(response.data.get('authors')) == 1


@pytest.mark.django_db
@pytest.mark.parametrize(
    'partial_data, status_code', [
        ({'name': 'book'}, 200),
        ({'year': 2000}, 200),

    ],
)
def test_book_id_patch(partial_data, status_code, api_client, insert_book):

    response = insert_book
    url = reverse('book_pk', kwargs={'pk': response.data[0].get('id')})
    data = partial_data
    response = api_client.patch(url, data=data, format='json')
    assert response.status_code == status_code


@pytest.mark.django_db
@pytest.mark.parametrize(
    'name, year, status_code', [
        (['book-1', 'book-2'], [1000, 2000], 200),
        (['book-1', 'book-2'], [None, None], 200),
        (['book-1', None], [1000, 2000], 400),
        ([None, 'book-2'], [1000, 2000], 400),


    ],
)
def test_book_put_multiple(name, year, status_code, api_client, insert_library, insert_author, insert_book):

    response = insert_book

    url = reverse('book_list')
    data = [{
            'id': response.data[0].get('id'),
            'name': name[0],
            'year': year[0],
            'library': insert_library.data[0].get('id'),
            'authors': [insert_author.data[0].get('id')]
    },
        {
            'id': response.data[0].get('id'),
            'name': name[1],
            'year': year[1],
            'library': insert_library.data[1].get('id'),
            'authors': [insert_author.data[0].get('id'), insert_author.data[1].get('id')]
        }
    ]
    response = api_client.put(url, data=data, format='json')
    assert response.status_code == status_code


@pytest.mark.django_db
@pytest.mark.parametrize(
    'name, year, status_code', [
        (['book-1', 'book-2'], [1000, 2000], 200),

    ],
)
def test_book_pathc_multiple(name, year, status_code, api_client, insert_library, insert_author, insert_book):

    response = insert_book

    url = reverse('book_list')
    data = [{
            'id': response.data[0].get('id'),
            'library': insert_library.data[1].get('id'),
            'authors': [insert_author.data[1].get('id')]
    },
        {
            'id': response.data[0].get('id'),
            'name': name[1],
            'authors': [insert_author.data[0].get('id')]
        }
    ]
    response = api_client.patch(url, data=data, format='json')
    assert response.status_code == status_code