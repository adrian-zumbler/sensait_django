from rest_framework.permissions import BasePermission


class isArduinoPermission(BasePermission):
    def has_permission(self, request, view):
        ret = False
        try:
            token = request.META.get('HTTP_X_ARDUINOTOKEN', None)
            ret = token is not None
        except:
            pass
        return ret
