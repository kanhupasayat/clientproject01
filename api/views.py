from rest_framework import viewsets, permissions
from .models import UploadedFile, StatusHistory
from .serializers import UploadedFileSerializer
from .permissions import IsOwnerOrReadOnly # Import the custom permission

class UploadedFileViewSet(viewsets.ModelViewSet):
    """
    ViewSet for viewing and editing uploaded files.
    """
    queryset = UploadedFile.objects.all().prefetch_related('status_history')
    serializer_class = UploadedFileSerializer
    # Apply two permissions:
    # 1. IsAuthenticated: Ensures the user is logged in.
    # 2. IsOwnerOrReadOnly: Ensures only the owner can edit/delete.
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        """
        Set the user for the new file and create the initial status history.
        """
        # Save the file with the current user.
        uploaded_file = serializer.save(user=self.request.user)
        # Create the first history record for the initial status.
        StatusHistory.objects.create(
            file=uploaded_file,
            status=uploaded_file.status,
            changed_by=self.request.user
        )

    def perform_update(self, serializer):
        """
        Save the updated file and create a new status history record if status changes.
        """
        # Check the status before saving the update.
        old_status = serializer.instance.status
        
        # Save the update.
        uploaded_file = serializer.save()
        
        # If the status has changed, create a new history record.
        if old_status != uploaded_file.status:
            StatusHistory.objects.create(
                file=uploaded_file,
                status=uploaded_file.status,
                changed_by=self.request.user
            )

    def get_queryset(self):
        """
        This view should return a list of all the files
        for the currently authenticated user.
        Superusers can see all files.
        """
        user = self.request.user
        if user.is_superuser:
            # For superusers, return all files.
            # .prefetch_related('status_history') makes the query more efficient.
            return UploadedFile.objects.all().prefetch_related('status_history')
        
        # For regular users, filter files by the current user.
        return UploadedFile.objects.filter(user=user).prefetch_related('status_history')

