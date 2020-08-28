from rest_framework.permissions import BasePermission
from .models import BlackListedToken


class IsTokenValid(BasePermission):
    """
    Class for validating if the token is present in the blacklisted token list.
    """

    def has_permission(self, request, view):
        """
        Function for checking if the caller of this function has
         permission to access particular API.
        """
        is_allowed_user = True
        auth_header = request.META.get('HTTP_AUTHORIZATION')
        if auth_header:
            key, token = auth_header.split(' ')
            if key == 'Bearer':
                print(token)
                try:
                    is_blacklisted = BlackListedToken.objects.get(token=token)
                    if is_blacklisted:
                        is_allowed_user = False
                except BlackListedToken.DoesNotExist:
                    is_allowed_user = True
                return is_allowed_user
        else:
            is_allowed_user = False
            return is_allowed_user
