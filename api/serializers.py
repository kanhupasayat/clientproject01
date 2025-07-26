from rest_framework import serializers
from .models import UploadedFile, StatusHistory
from django.contrib.auth.models import User

class StatusHistorySerializer(serializers.ModelSerializer):
    """
    Serializer for the StatusHistory model.
    Includes the username of the person who changed the status.
    """
    changed_by = serializers.ReadOnlyField(source='changed_by.username')

    class Meta:
        model = StatusHistory
        fields = ['status', 'changed_at', 'changed_by']


class UploadedFileSerializer(serializers.ModelSerializer):
    """
    Serializer for the UploadedFile model.
    - Makes the user field read-only and displays the username.
    - Includes nested status history.
    """
    # Source='user.username' fetches the username from the related User model.
    user = serializers.ReadOnlyField(source='user.username')
    status_history = StatusHistorySerializer(many=True, read_only=True)

    class Meta:
        model = UploadedFile
        # Added 'status_history' to the fields list.
        fields = ['id', 'user', 'category', 'file', 'status', 'uploaded_at', 'status_history']
        read_only_fields = ['user', 'uploaded_at', 'status_history']

