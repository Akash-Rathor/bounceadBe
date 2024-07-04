from django.utils.deprecation import MiddlewareMixin
import copy


class RequestBodyCaptureMiddleware(MiddlewareMixin):
    def process_request(self, request):
        request._body_copy = copy.deepcopy(request.body)
