from django.db import models

class Document(models.Model):

    STATUS_CHOICES = [
        ('UPLOADED', 'Uploaded'),
        ('PROCESSING', 'Processing'),
        ('PROCESSED', 'Processed'),
    ]

    file = models.FileField(upload_to='documents/')
    filename = models.CharField(max_length=255)
    file_size = models.PositiveIntegerField()
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='UPLOADED'
    )
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.filename
