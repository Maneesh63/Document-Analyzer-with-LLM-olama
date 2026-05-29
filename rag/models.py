from django.db import models
import uuid

# Create your models here.
class Document(models.Model):

    processing = 'processing'
    ready = 'ready'
    failed = 'failed'
    DOCUMENT_STATUS_CHOICES = [
        (processing, 'Processing'),
        (ready,      'Ready'),
        (failed,     'Failed'),
    ]

    document_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    file = models.FileField(upload_to='documents/', null=True, blank=True)
    file_name = models.CharField(max_length=255, null=True)
    file_path = models.CharField(max_length=255, null=True)
    file_url = models.URLField(max_length=255, null=True, blank=True)
    status = models.CharField(max_length=50, default=processing, choices=DOCUMENT_STATUS_CHOICES)
    total_chunks= models.IntegerField(default=0)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.file_name if self.file_name else str(self.document_id)
    

class QueryHistory(models.Model):
    id          = models.UUIDField(primary_key=True, default=uuid.uuid4)
    document    = models.ForeignKey(Document, on_delete=models.CASCADE)
    question    = models.TextField()
    answer      = models.TextField()
    created_at  = models.DateTimeField(auto_now_add=True)

     
        

