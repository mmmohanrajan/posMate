from rest_framework.permissions import BasePermission
from core.models import Business
from rest_framework.exceptions import PermissionDenied


class CanViewProductsPermission(BasePermission):
    def has_permission(self, request, view):
        # Check if the user has permission to view products based on business_id
        business_id = request.query_params.get('business_id')
        
        # Implement your custom logic here
        if business_id:
            # Get the business associated with the provided business_id
            try:
                business = Business.objects.get(pk=business_id)
            except Business.DoesNotExist:
                raise PermissionDenied("Business not found with the provided ID")
            
            # Check if the requesting user is an owner, manager, or staff member of the business
            if (request.user in business.owners.all() or
                request.user in business.managers.all() or
                request.user in business.staff.all()):
                return True
            else:
                raise PermissionDenied("You do not have permission to view products for this business")
        else:
            raise PermissionDenied("Business ID is required to view products")

        return False  # Return False if business_id is not provided
