from django.urls import path
from .views import health, upload_document

urlpatterns = [
    path('health/', health),
    path('documents/upload/', upload_document),
]
