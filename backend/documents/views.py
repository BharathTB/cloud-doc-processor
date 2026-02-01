from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import Document
from .serializers import DocumentUploadSerializer

@api_view(['GET'])
def health(request):
    return Response({"status": "UP"})

@api_view(['POST'])
def upload_document(request):
    uploaded_file = request.FILES.get('file')

    if not uploaded_file:
        return Response(
            {"error": "No file provided"},
            status=status.HTTP_400_BAD_REQUEST
        )

    # Validation rules
    allowed_extensions = ['.pdf', '.png', '.jpg', '.jpeg']
    max_file_size = 5 * 1024 * 1024  # 5 MB

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

    document = Document.objects.create(
        file=uploaded_file,
        filename=uploaded_file.name,
        file_size=uploaded_file.size,
        status='UPLOADED'
    )

    serializer = DocumentUploadSerializer(document)
    return Response(serializer.data, status=status.HTTP_201_CREATED)

