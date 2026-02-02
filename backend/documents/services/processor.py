import time
import logging
from documents.models import Document

logger = logging.getLogger(__name__)

def process_document(document_id):
    """
    Simulates background processing of a document.
    """

    try:
        document = Document.objects.get(id=document_id)
    except Document.DoesNotExist:
        logger.error(f"Document with id {document_id} not found")
        return

    logger.info(f"Starting processing for document {document.id}")

    document.status = 'PROCESSING'
    document.save()

    # Simulate processing time
    time.sleep(5)

    document.status = 'PROCESSED'
    document.save()

    logger.info(f"Completed processing for document {document.id}")
