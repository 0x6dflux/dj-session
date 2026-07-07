from typing import Callable

from django.http import HttpRequest, HttpResponse


class MySessionMiddleware:
    def __init__(self, get_response: Callable) -> None:
        self.get_response = get_response

    def __call__(self, request: HttpRequest) -> HttpResponse:
        # read cookies
        # get sessionid from cookies
        # if sessionid exists, get session data from database
        # else assign a new MySession obj
        # request.session = MySession({})
        # do not forget to check the expiration date
        response = self.get_response(request)
        print("after response", request.COOKIES)
        return response
