from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),

    # Login and Logout in API
    path('api-auth/', include('rest_framework.urls')),

    # Image
    path('api/image/', include('image_hosting.urls')),
]
