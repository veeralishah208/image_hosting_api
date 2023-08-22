from django.urls import path
from .views import ImageUploadAPI, ImageListAPI

urlpatterns = [
    # Upload image
    path('upload-image/', ImageUploadAPI.as_view(), name="upload-image"),
    path('image-list/', ImageListAPI.as_view(), name="image-list"),

]
