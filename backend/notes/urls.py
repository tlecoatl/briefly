from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CollectionViewSet, NoteViewSet

router = DefaultRouter()
router.register(r'collections', CollectionViewSet, basename='collection')
router.register(r'notes', NoteViewSet, basename='note')

urlpatterns = [
    path('', include(router.urls)),
]