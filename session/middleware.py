from typing import Callable

from django.http import HttpRequest, HttpResponse


class MySessionMiddleware:
    def __init__(self, get_response: Callable) -> None:
        self.get_response = get_response

    def __call__(self, request: HttpRequest) -> HttpResponse:
        if request.COOKIES:
            request_session_id = request.COOKIES.get("sessionid")
            # do not forget to check the expiration date
            if request_session_id and MySession.is_valid(request_session_id):
                # get session data from database
                # request.session = MySession._get_session_data(request_session_id)
                ...
            else:
                # request.session = MySession._get_new_session()
                ...
        response = self.get_response(request)
        # response.set_cookie("sessionid", request.session.session_id)
        # if request.session.is_session_modified:
        #   save session data to database
        return response
