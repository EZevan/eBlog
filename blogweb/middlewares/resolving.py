from django.utils.deprecation import MiddlewareMixin
import json


class ResolvingMiddleware(MiddlewareMixin):
    """
    Resolving the http POST request data
    """

    def process_request(self, request):
        if request.method == "POST":
            data = json.loads(request.body, encoding="utf8")
            request.data = data

    def prcess_response(self, response):
        return response
