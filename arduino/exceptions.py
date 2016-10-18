from rest_framework.exceptions import APIException
from rest_framework import status


class StandardAPIException(APIException):

    status_code = status.HTTP_416_REQUESTED_RANGE_NOT_SATISFIABLE