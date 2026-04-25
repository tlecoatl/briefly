import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from notes.models import Note


@pytest.fixture
def user():
    return User.objects.create_user(
        username='testuser',
        password='testpass123'
    )


@pytest.fixture
def client(user):
    api_client = APIClient()
    api_client.force_authenticate(user=user)
    return api_client


@pytest.mark.django_db
def test_create_note(client):
    response = client.post('/api/notes/', {
        'title': 'Test Note',
        'content': 'This is test content.'
    }, format='json')

    assert response.status_code == 201
    assert response.data['title'] == 'Test Note'
    assert response.data['summary_status'] == 'pending'

@pytest.mark.django_db
def test_retrieve_note(client, user):
    note = Note.objects.create(
        owner=user,
        title='My Note',
        content='Some content.'
    )

    response = client.get(f'/api/notes/{note.id}/')

    assert response.status_code == 200
    assert response.data['title'] == 'My Note'


@pytest.mark.django_db
def test_cannot_access_other_users_note(user):
    other_user = User.objects.create_user(
        username='otheruser',
        password='otherpass123'
    )
    note = Note.objects.create(
        owner=other_user,
        title='Private Note',
        content='Secret content.'
    )

    other_client = APIClient()
    other_client.force_authenticate(user=user)

    response = other_client.get(f'/api/notes/{note.id}/')

    assert response.status_code == 404


@pytest.mark.django_db
def test_unauthenticated_user_cannot_access_notes():
    unauthenticated_client = APIClient()

    response = unauthenticated_client.get('/api/notes/')

    assert response.status_code == 401


@pytest.mark.django_db
def test_delete_note(client, user):
    note = Note.objects.create(
        owner=user,
        title='Note to delete',
        content='Will be deleted.'
    )

    response = client.delete(f'/api/notes/{note.id}/')

    assert response.status_code == 204
    assert Note.objects.filter(id=note.id).count() == 0