from django.conf import settings
from rest_framework.permissions import BasePermission

ALLOW_ANY = '_ALLOW_ANY'
IS_AUTHENTICATED = '_IS_AUTHENTICATED'


class CustomPermission(BasePermission):
    """
    A class for setting permissions based on methods
    LIST, RETRIEVE, UPDATE, PARTIAL UPDATE, DESTROY

    """

    def has_permission(self, request, view):
        if view.permission_groups.get('all'):
            required_groups = view.permission_groups.get('all')
        else:
            required_groups = view.permission_groups.get(view.action)
            if required_groups == None:
                return False
        
        if IS_AUTHENTICATED in required_groups:
            return not request.user.is_anonymous
        elif ALLOW_ANY in required_groups:
            return True
        else:
            return False