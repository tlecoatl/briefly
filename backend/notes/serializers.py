from rest_framework import serializers
from .models import Collection, Note


class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ['id', 'name', 'description', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']


class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = [
            'id',
            'collection',
            'title',
            'content',
            'summary',
            'summary_status',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['summary', 'summary_status', 'created_at', 'updated_at']


class NoteListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for list views — omits content to keep responses small."""
    class Meta:
        model = Note
        fields = ['id', 'collection', 'title', 'summary_status', 'created_at']
        read_only_fields = ['summary_status', 'created_at']