from django.http.response import JsonResponse
from rest_framework import status
from django.db import OperationalError, InterfaceError
from django.db.utils import DatabaseError
import time
from backend.utils.exceptions.http_exception import BadRequestError
from backend.queries.api_call_log import ApiCallLogQuery


def respond_200(data, msg=""):
    """Return success json response"""
    return JsonResponse({"msg": msg, "data": data}, status=status.HTTP_200_OK)


def respond_201(data, msg=""):
    """Return created json response"""
    return JsonResponse({"msg": msg, "data": data}, status=status.HTTP_201_CREATED)


def respond_with_msg(msg=""):
    """Return json response with just message"""
    return respond_200(None, msg)


def respond_with_error(msg="", status=status.HTTP_400_BAD_REQUEST):
    """Return json response with error message and status code"""

    return JsonResponse({"msg": msg}, status=status)


def respond_just_json(data):
    return JsonResponse(data)


def execute_with_retry_decorator(my_method):
    max_retries = 3
    delay = 1

    def execute_my_method(*args, **kwargs):
        for attempt in range(max_retries):
            try:
                return my_method(*args, **kwargs)
            except (OperationalError, InterfaceError, DatabaseError) as e:
                if attempt < max_retries - 1:
                    time.sleep(delay)
                    return execute_my_method(args, kwargs)
                else:
                    raise BadRequestError("Please try again later")

    return execute_my_method
