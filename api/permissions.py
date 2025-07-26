from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit or delete it.
    Assumes the model instance has a `user` attribute.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any authenticated request,
        # so anyone can view their own files (this is handled by get_queryset in the view).
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner of the file.
        # obj.user is the user who uploaded the file.
        # request.user is the user making the current request.
        return obj.user == request.user
