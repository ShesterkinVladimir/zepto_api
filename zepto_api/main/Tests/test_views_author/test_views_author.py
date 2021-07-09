import pytest

from main.models import Author
from django.urls import reverse


@pytest.mark.django_db
def test_library_get(api_client):
    url = reverse('author')
    response = api_client.get(url)
    assert response.status_code == 200
    assert response.data[0]['name'] == 'Murakami'
    assert response.data[1]['birth_date'] == '1999-09-10'


@pytest.mark.django_db
@pytest.mark.parametrize(
    'name, birth_date, status_code', [
        ('Author-1', '2000-12-12', 201),
        (None, '2021-12-20', 400),
        ('Author-2', None, 400),

    ],
)
def test_author_post(name, birth_date, status_code, api_client):

    url = reverse('author')
    data = {
        'name': name,
        'birth_date': birth_date
    }
    response = api_client.post(url, data=data, format='json')
    assert response.status_code == status_code


@pytest.mark.django_db
@pytest.mark.parametrize(
    'name, birth_date, status_code', [
        (['Author-1', 'Author-2'], ['1010-01-12', '2000-12-12'], 201),
        (['Author-1', 'Author-2'], [None, '2000-12-12'], 400),
        (['Author-1', None], ['1010-01-12', None], 400),

    ],
)
def test_author_post_multiple(name, birth_date, status_code, api_client):

    url = reverse('author')
    data = [{
        'name': name[0],
        'birth_date': birth_date[0]
    },
        {
        'name': name[1],
        'birth_date': birth_date[1]
        }
    ]
    response = api_client.post(url, data=data, format='json')
    assert response.status_code == status_code


@pytest.mark.django_db
def test_author_id_get(api_client):
    url = reverse('author_pk', kwargs={'pk':  api_client.get(reverse('author')).data[0].get('id')})
    response = api_client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
@pytest.mark.parametrize(
    'name, birth_date, status_code', [
        ('Author-1', '2000-12-12', 200),
        (None, '2021-12-20', 400),
        ('Author-2', None, 400),

    ],
)
def test_author_id_put(name, birth_date, status_code, api_client, insert_author):

    response = insert_author
    url = reverse('author_pk', kwargs={'pk':  response.data[0].get('id')})
    data = {
        'name': name,
        'birth_date': birth_date
    }
    response = api_client.put(url, data=data, format='json')
    assert response.status_code == status_code
    if status_code == 200:
        assert response.data.get('name') == name
    else:
        assert api_client.get(reverse('author')).data[0].get('name') == "Murakami"


@pytest.mark.django_db
@pytest.mark.parametrize(
    'partial_data, status_code', [
        ({'name': 'Author-1'}, 200),
        ({'birth_date': '2000-12-12'}, 200),
        ({'name': 'Author-1', 'birth_date': '2000-12-12'}, 200)

    ],
)
def test_author_id_patch(partial_data, status_code, api_client, insert_author):

    response = insert_author
    url = reverse('author_pk', kwargs={'pk': response.data[0].get('id')})
    data = partial_data
    response = api_client.patch(url, data=data, format='json')
    assert response.status_code == status_code


@pytest.mark.django_db
@pytest.mark.parametrize(
    'name, birth_date, status_code', [
        (['Author-1', 'Author-2'], ['2000-12-12', '2012-12-12'], 200),
        (['SAuthor-1', 'Author-2'], [None, '2012-12-12'], 400),
        (['Author-1', None], ['2012-12-12', None], 400),

    ],
)
def test_author_put_multiple(name, birth_date, status_code, api_client, insert_author):

    response = insert_author

    url = reverse('author_list')
    data = [{
        'id': response.data[0].get('id'),
        'name': name[0],
        'birth_date': birth_date[0]
    },
        {
        'id': response.data[0].get('id'),
        'name': name[1],
        'birth_date': birth_date[1]
        }
    ]
    response = api_client.put(url, data=data, format='json')
    assert response.status_code == status_code


@pytest.mark.django_db
@pytest.mark.parametrize(
    'name, birth_date, status_code', [
        (['Author-1', 'Author-2'], ['2000-12-12', '2012-12-12'], 200),
        (['Author-1', 'Author-2'], ['2012-12-12', None], 400),
        ([None, 'Author-2'], ['2012-12-12', '2012-12-12'], 400),

    ],
)
def test_author_patch_multiple(name, birth_date, status_code, api_client,  insert_author):

    response = insert_author

    url = reverse('author_list')
    data = [{
        'id': response.data[0].get('id'),
        'name': name[0]
    },
        {
        'id': response.data[1].get('id'),
        'birth_date': birth_date[1]
        }
    ]
    response = api_client.patch(url, data=data, format='json')
    assert response.status_code == status_code

