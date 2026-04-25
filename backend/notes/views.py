from rest_framework import viewsets, permissions, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Collection, Note
from .serializers import CollectionSerializer, NoteSerializer, NoteListSerializer
from .tasks import summarize_note, summarize_collection

class IsOwner(permissions.BasePermission):
    """Only allow owners of an object to access it."""
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user


class CollectionViewSet(viewsets.ModelViewSet):
    serializer_class = CollectionSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def get_queryset(self):
        return Collection.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    @action(detail=True, methods=['post'], url_path='summarize')
    def summarize(self, request, pk=None):
        collection = self.get_object()
        summarize_collection.delay(collection.id)
        return Response({'status': 'summarization started'})


class NoteViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated, IsOwner]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['collection', 'summary_status']
    search_fields = ['title', 'content']
    ordering_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']

    def get_queryset(self):
        return Note.objects.filter(owner=self.request.user)

    def get_serializer_class(self):
        if self.action == 'list':
            return NoteListSerializer
        return NoteSerializer

    def perform_create(self, serializer):
        note = serializer.save(owner=self.request.user)
        summarize_note.delay(note.id)