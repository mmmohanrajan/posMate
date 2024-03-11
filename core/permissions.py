from rest_framework import permissions
from rest_framework.exceptions import PermissionDenied


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner of the expense
        return obj.user == request.user
    

class CanCreateExpenseForBusiness(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == 'POST':
            business_id = request.data.get('business')
            if business_id:
                user = request.user
                has_access = user.owned_businesses.filter(pk=business_id).exists() or \
                 user.managed_businesses.filter(pk=business_id).exists() or \
                 user.assigned_businesses.filter(pk=business_id).exists()
                if has_access:
                    return True
                else:
                    raise PermissionDenied("You do not have permission to create expenses for this business.")
            else:
                raise PermissionDenied("You must specify a business ID when creating an expense.")
        return True  # Allow other methods
