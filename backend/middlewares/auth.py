from django.http.response import JsonResponse
from backend.utils.exceptions.http_exception import AccessDeniedError, NotFoundError, BadRequestError
from backend.utils.auth.jwt import JWTAuth
import os
import jwt
import time
from bouncead.settings import Endpoints
from rest_framework.exceptions import APIException
# from backend.queries.config import ConfigQuery
from backend.utils.datetime import datetime
from backend.queries.user import UserQuery


# from backend.queries.api_call_log import ApiCallLogQuery


class AuthMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Executed for each request before the view (and later middleware) are called.

        try:
            excluded_endpoints_api = [
                "/hcheck",
                '/api/' + Endpoints.GENERATE_OTP.value,
                '/api/' + Endpoints.VERIFY_OTP.value,
                '/api/' + Endpoints.REGISTER.value,
                '/api/' + Endpoints.LOGIN.value,
            ]

            admin_endpoints = '/admin'
            blogs_endpoints = '/blogs'

            excluded_dynamic_endpoints = [

            ]

            token_authenticated_endpoints = [
            ]

            is_excluded = False

            if admin_endpoints in request.path or blogs_endpoints in request.path:
                is_excluded = True

            for endpoint in excluded_dynamic_endpoints:
                is_excluded = self.is_excluded(
                    path=request.path, endpoint=endpoint)
                if is_excluded:
                    break

            if request.path not in excluded_endpoints_api and not is_excluded:
                token = request.headers.get('Authorization')
                if token is None:
                    raise NotFoundError("Unauthorized request")
                try:
                    payload = JWTAuth().decode(token, os.getenv("JWT_SECRET"))
                except Exception as e:
                    raise AccessDeniedError('Session Expired, please re-login')
                    # raise AccessDeniedError("Invalid token")

                if payload.get('exp') < int(time.time()):
                    raise AccessDeniedError("Session Expired, please re-login")

                # if payload.get('mobile_app_version') != os.getenv('mobile_app_version'):
                #     raise AccessDeniedError(
                #         "Please download the latest app with new features and bug fixes.")

                payload.pop('exp')

                request.actor = payload

                try:
                    user = UserQuery().get_or_fail(id=payload.get('id'))
                except:
                    raise AccessDeniedError("Session Expired, please re-login")

        except APIException as ex:
            return JsonResponse({'msg': ex.detail}, status=ex.status_code)

        response = self.get_response(request)

        # Code to be executed for each request/response after the view is called.
        return response

    def is_excluded(self, path, endpoint):
        path_comp = path.split('/')[2:]
        endpoint_comp = endpoint.split('/')[2:]
        if len(path_comp) != len(endpoint_comp):
            return False
        for index, comp in enumerate(endpoint_comp):
            if comp[0] != '<' and comp != path_comp[index]:
                return False
        return True
