import pytest
from unittest.mock import patch, MagicMock
from django.contrib.auth.models import User
from notes.models import Note
from notes.tasks import summarize_note


@pytest.fixture
def user():
    return User.objects.create_user(
        username='testuser',
        password='testpass123'
    )


@pytest.fixture
def note(user):
    return Note.objects.create(
        owner=user,
        title='Test Note',
        content='This is the content to summarize.'
    )


@pytest.mark.django_db
def test_summarize_note_success(note):
    mock_response = MagicMock()
    mock_response.choices[0].message.content = 'This is a mock summary.'

    with patch('notes.tasks.Groq') as MockGroq:
        MockGroq.return_value.chat.completions.create.return_value = mock_response
        summarize_note(note.id)

    note.refresh_from_db()
    assert note.summary_status == 'completed'
    assert note.summary == 'This is a mock summary.'


@pytest.mark.django_db
def test_summarize_note_sets_processing_status(note):
    mock_response = MagicMock()
    mock_response.choices[0].message.content = 'Summary.'

    with patch('notes.tasks.Groq') as MockGroq:
        MockGroq.return_value.chat.completions.create.return_value = mock_response
        summarize_note(note.id)

    note.refresh_from_db()
    assert note.summary_status == 'completed'


@pytest.mark.django_db
def test_summarize_note_handles_api_failure(note):
    with patch('notes.tasks.Groq') as MockGroq:
        MockGroq.return_value.chat.completions.create.side_effect = Exception('API error')
        summarize_note(note.id)

    note.refresh_from_db()
    assert note.summary_status == 'failed'
    assert note.summary == ''


@pytest.mark.django_db
def test_summarize_note_nonexistent_note():
    result = summarize_note(99999)
    assert result is None