from typing import Callable

from django.http import HttpRequest, HttpResponse


class MySessionMiddleware:
    def __init__(self, get_response: Callable) -> None:
        self.get_response = get_response

    def __call__(self, request: HttpRequest) -> HttpResponse:
        response = self.get_response(request)
        print("after response", request.COOKIES)
        return response
