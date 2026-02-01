from rest_framework import serializers
from .models import Document

class DocumentUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ['id', 'file', 'filename', 'file_size', 'status', 'uploaded_at']
        read_only_fields = ['id', 'status', 'uploaded_at']
