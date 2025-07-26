from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

STATUS_CHOICES = (
    ('Investigation', 'Investigation'),
    ('Under Trial', 'Under Trial'),
    ('Case Closed', 'Case Closed'),
    ('Referred to Court', 'Referred to Court'),
    ('Other Relevant Status', 'Other Relevant Status'),
)

class UploadedFile(models.Model):
    """
    Represents a file uploaded by a user.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='uploaded_files')
    category = models.CharField(max_length=100)
    file = models.FileField(upload_to='uploads/')
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='Investigation')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.category}"

class StatusHistory(models.Model):
    """
    Tracks the history of status changes for an UploadedFile.
    This creates a log every time the status of a file is changed.
    """
    file = models.ForeignKey(UploadedFile, on_delete=models.CASCADE, related_name='status_history')
    status = models.CharField(max_length=30, choices=STATUS_CHOICES)
    changed_at = models.DateTimeField(auto_now_add=True)
    changed_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        # Orders the history records by the most recent change first.
        ordering = ['-changed_at']

    def __str__(self):
        return f"{self.file.id} - {self.status} at {self.changed_at.strftime('%Y-%m-%d %H:%M')}"
