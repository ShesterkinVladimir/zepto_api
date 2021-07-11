import pytest

from api.models import Library
from django.urls import reverse


# tests for library
@pytest.mark.django_db
def test_library_get(api_client):
    url = reverse('library')
    response = api_client.get(url)
    assert response.status_code == 200
    assert response.data[0].get('address') == 'Sovetskaya'
    assert response.data[1].get('book_capacity') == 10000


@pytest.mark.django_db
@pytest.mark.parametrize(
    'address, book_capacity, name, status_code', [
        ('Sovetskaya', 1000, 'Nekrasova', 201),
        (None, 1000, 'Nekrasova', 400),
        ('Sovetskaya', None, 'Nekrasova', 400),
        ('Sovetskaya', 1000, None, 400),
        (None, None, None, 400)

    ],
)
def test_library_post(address, book_capacity, name, status_code, api_client):

    url = reverse('library')
    data = {
        'address': address,
        'book_capacity': book_capacity,
        'name': name
    }
    response = api_client.post(url, data=data, format='json')
    assert response.status_code == status_code


@pytest.mark.django_db
@pytest.mark.parametrize(
    'address, book_capacity, name, status_code', [
        (['Sovetskaya', 'street 1'], [1000, 5000], ['Nekrasova', 'Pushkina'], 201),
        (['Sovetskaya', 'street 1'], [None, 5000], ['Nekrasova', 'Pushkina'], 400),
        (['Sovetskaya', None], [1000, None], ['Nekrasova', None], 400),

    ],
)
def test_library_post_multiple(address, book_capacity, name, status_code, api_client):

    url = reverse('library')
    data = [{
            'address': address[0],
            'book_capacity': book_capacity[0],
            'name': name[0]
    },
        {
            'address': address[1],
            'book_capacity': book_capacity[1],
            'name': name[1]
        }
    ]
    response = api_client.post(url, data=data, format='json')
    assert response.status_code == status_code


@pytest.mark.django_db
def test_library_id_get(api_client):
    url = reverse('library_pk', kwargs={'pk':  api_client.get(reverse('library')).data[0].get('id')})
    response = api_client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
@pytest.mark.parametrize(
    'address, book_capacity, name, status_code', [
        ('Sovetskaya-1', 20000, 'Nekrasova-3', 200),
        ('Sovetskaya', 1000, 'Nekrasova', 200),
        (None, 1000, 'Nekrasova', 400),
        ('Sovetskaya-10', None, 'Nekrasova', 400)

    ],
)
def test_library_id_put(address, book_capacity, name, status_code, api_client, insert_library):

    response = insert_library
    url = reverse('library_pk', kwargs={'pk':  response.data[0].get('id')})
    data = {
        'address': address,
        'book_capacity': book_capacity,
        'name': name
    }
    response = api_client.put(url, data=data, format='json')
    assert response.status_code == status_code
    if status_code == 200:
        assert response.data.get('address') == address
    else:
        assert api_client.get(reverse('library')).data[0].get('address') == "Sovetskaya"



@pytest.mark.django_db
@pytest.mark.parametrize(
    'partial_data, status_code', [
        ({'address': 'Sovetskaya-1'}, 200),
        ({'book_capacity': 2000}, 200),
        ({'name': 'Nekrasova-1'}, 200)

    ],
)
def test_library_id_patch(partial_data, status_code, api_client, insert_library):

    response = insert_library
    url = reverse('library_pk', kwargs={'pk': response.data[0].get('id')})
    data = partial_data
    response = api_client.patch(url, data=data, format='json')
    assert response.status_code == status_code


@pytest.mark.django_db
@pytest.mark.parametrize(
    'address, book_capacity, name, status_code', [
        (['Sovetskaya', 'street 1'], [1000, 5000], ['Nekrasova', 'Pushkina'], 200),
        (['Sovetskaya', 'street 1'], [None, 5000], ['Nekrasova', 'Pushkina'], 400),
        (['Sovetskaya', None], [1000, None], ['Nekrasova', None], 400),

    ],
)
def test_library_put_multiple(address, book_capacity, name, status_code, api_client, insert_library):

    response = insert_library

    url = reverse('library_list')
    data = [{
        'id': response.data[0].get('id'),
        'address': address[0],
        'book_capacity': book_capacity[0],
        'name': name[0]
    },
        {
            'id': response.data[1].get('id'),
            'address': address[1],
            'book_capacity': book_capacity[1],
            'name': name[1]
        }
    ]
    response = api_client.put(url, data=data, format='json')
    assert response.status_code == status_code


@pytest.mark.django_db
@pytest.mark.parametrize(
    'address, book_capacity, name, status_code', [
        (['Sovetskaya', 'street 1'], [1000, 5000], ['Nekrasova', 'Pushkina'], 200),
        (['Sovetskaya', 'street 1'], [None, 5000], ['Nekrasova', 'Pushkina'], 200),
        (['Sovetskaya', None], [1000, None], ['Nekrasova', None], 400),

    ],
)
def test_library_patch_multiple(address, book_capacity, name, status_code, api_client,  insert_library):

    response = insert_library

    url = reverse('library_list')
    data = [{
        'id': response.data[0].get('id'),
        'name': name[0]
    },
        {
        'id': response.data[1].get('id'),
        'address': address[1]
        }
    ]
    response = api_client.patch(url, data=data, format='json')
    assert response.status_code == status_code
