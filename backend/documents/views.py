import socket

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from django.shortcuts import get_object_or_404

from .models import Document
from .serializers import DocumentUploadSerializer
from documents.services.processor import process_document


@api_view(['GET'])
def health(request):
    """
    Health check endpoint used by Kubernetes readiness & liveness probes.
    """
    return Response({
        "status": "UP",
        "pod": socket.gethostname()
    })


@api_view(['POST'])
def upload_document(request):
    """
    Uploads a document and stores metadata.
    Does NOT trigger processing.
    """

    uploaded_file = request.FILES.get('file')

    # Validate file presence
    if not uploaded_file:
        return Response(
            {"error": "No file provided"},
            status=status.HTTP_400_BAD_REQUEST
        )

    # Validation rules
    allowed_extensions = ['.pdf', '.png', '.jpg', '.jpeg']
    max_file_size = 5 * 1024 * 1024  # 5MB

    file_extension = uploaded_file.name.lower().split('.')[-1]
    file_extension = f".{file_extension}"

    if file_extension not in allowed_extensions:
        return Response(
            {"error": "Unsupported file type"},
            status=status.HTTP_400_BAD_REQUEST
        )

    if uploaded_file.size > max_file_size:
        return Response(
            {"error": "File size exceeds 5MB limit"},
            status=status.HTTP_400_BAD_REQUEST
        )

    # Create document record
    document = Document.objects.create(
        file=uploaded_file,
        filename=uploaded_file.name,
        file_size=uploaded_file.size,
        status='UPLOADED'
    )

    serializer = DocumentUploadSerializer(document)

    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['POST'])
def process_document_view(request, document_id):
    """
    Triggers background processing for a document.
    """

    document = get_object_or_404(Document, id=document_id)

    # Prevent duplicate processing
    if document.status in ['PROCESSING', 'PROCESSED']:
        return Response(
            {
                "id": document.id,
                "status": document.status
            },
            status=status.HTTP_200_OK
        )

    # Update status before processing
    document.status = 'PROCESSING'
    document.save()

    # Trigger async processing
    process_document(document.id)

    # Refresh from DB after processing
    document.refresh_from_db()

    return Response(
        {
            "id": document.id,
            "status": document.status
        },
        status=status.HTTP_200_OK
    )


@api_view(['GET'])
def document_status_view(request, document_id):
    """
    Returns current document status.
    """

    document = get_object_or_404(Document, id=document_id)

    return Response(
        {
            "id": document.id,
            "status": document.status
        },
        status=status.HTTP_200_OK
    )
