import logging
from groq import Groq
from celery import shared_task
from .models import Note

logger = logging.getLogger(__name__)


@shared_task
def summarize_note(note_id):
    try:
        note = Note.objects.get(id=note_id)
    except Note.DoesNotExist:
        return

    note.summary_status = Note.SummaryStatus.PROCESSING
    note.save(update_fields=['summary_status'])

    try:
        client = Groq()
        message = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "user",
                    "content": f"Summarize the following note in 2-3 concise sentences:\n\n{note.content}"
                }
            ]
        )
        note.summary = message.choices[0].message.content
        note.summary_status = Note.SummaryStatus.COMPLETED
        note.save(update_fields=['summary', 'summary_status'])

    except Exception as e:
        logger.error(f"Groq API error for note {note_id}: {str(e)}")
        note.summary_status = Note.SummaryStatus.FAILED
        note.save(update_fields=['summary_status'])

@shared_task
def summarize_collection(collection_id):
    from .models import Collection

    try:
        collection = Collection.objects.get(id=collection_id)
    except Collection.DoesNotExist:
        return

    notes = collection.notes.all()
    if not notes:
        return

    combined = "\n\n".join(
        f"Note: {note.title}\n{note.content}" for note in notes
    )

    try:
        client = Groq()
        message = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "user",
                    "content": f"Summarize the following collection of notes in 3-5 concise sentences, capturing the key themes:\n\n{combined}"
                }
            ]
        )
        collection.description = message.choices[0].message.content
        collection.save(update_fields=['description'])

    except Exception as e:
        logger.error(f"Groq API error for collection {collection_id}: {str(e)}")