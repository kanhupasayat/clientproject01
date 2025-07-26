from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UploadedFileViewSet

# DefaultRouter automatically creates the URL patterns for a ViewSet.
# It will handle list, create, retrieve, update, partial_update, and destroy actions.
router = DefaultRouter()

# Register the 'UploadedFileViewSet' with the router.
# The URL prefix will be 'files'. So the endpoint will be /api/files/
# 'basename' is important for generating URL names, especially when queryset is dynamic.
router.register(r'files', UploadedFileViewSet, basename='uploadedfile')

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('', include(router.urls)),
]
