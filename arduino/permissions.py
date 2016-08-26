from rest_framework.permissions import BasePermission
from arduino.models import Arduino

class isArduinoPermission(BasePermission):
    def has_permission(self, request, view):
        ret = False
        try:
            token = request.META.get('HTTP_X_ARDUINOTOKEN', None)
            ret = token is not None
            arduino = Arduino.objects.get(arduino_token=request.META['HTTP_X_ARDUINOTOKEN'])
            request.arduino = arduino
        except Exception as e:
            return False
        return ret
