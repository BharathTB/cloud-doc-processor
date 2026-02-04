from django.urls import path
from .views import (
    health,
    upload_document,
    process_document_view,
    document_status_view,
)

urlpatterns = [
    path('health/', health),
    path('documents/upload/', upload_document),
    path('documents/<int:document_id>/process/', process_document_view),
    path('documents/<int:document_id>/status/', document_status_view),
]
