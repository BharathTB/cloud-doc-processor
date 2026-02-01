from django.db import models

class Document(models.Model):
    file = models.FileField(upload_to='documents/')
    filename = models.CharField(max_length=255)
    file_size = models.PositiveIntegerField()
    status = models.CharField(max_length=50, default='UPLOADED')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.filename

