from rest_framework.exceptions import APIException
from rest_framework import status


"""Not found error exception"""


class NotFoundError(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = "Resource not found"


"""Access denied error exception"""


class AccessDeniedError(APIException):
    status_code = 401
    default_detail = "Access Denied"


"""Bad request error exception"""


class BadRequestError(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "Bad Request"


"""Bad request with Redirect status code"""


class BadRequestWithRedirectError(APIException):
    status_code = status.HTTP_301_MOVED_PERMANENTLY
    default_detail = "Bad Request"


"""Access forbidden error exception"""


class AccessForbiddenError(APIException):
    status_code = status.HTTP_403_FORBIDDEN
    default_detail = "Access Forbidden"


"""Validation error exception"""


class ValidationError(APIException):
    status_code = 422
    default_detail = "Validation Error"

    def __init__(self, message, errors=None):
        super(APIException, self).__init__(message)
        # Add validation errors in exception
        self.errors = errors
        self.detail = message


"""Internal server error exception"""


class InternalServerError(APIException):
    status_code = 500
    default_detail = "Internal Server Error"


class TOO_MANY_REQUESTS(APIException):
    status_code = 429
    default_detail = "Too many requests!"


class ResetContent(APIException):
    status_code = 205
    default_details = "Content re-setted"
