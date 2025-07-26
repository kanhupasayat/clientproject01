from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # URL for the Django admin site
    path('admin/', admin.site.urls),

    # Include the URLs from your 'api' app under the 'api/' prefix
    # All URLs from api/urls.py will now start with /api/
    # e.g., /api/files/
    path('api/', include('api.urls')),

    # URLs for user authentication (login, logout, password reset) from dj-rest-auth
    path('auth/', include('dj_rest_auth.urls')),

    # If you want to enable user registration, you can uncomment the line below
    # path('auth/registration/', include('dj_rest_auth.registration.urls')),
]

# This is a helper function to serve media files (like user uploads)
# during development (when DEBUG=True). This is not for production.
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
