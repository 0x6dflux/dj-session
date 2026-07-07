from typing import Callable
from uuid import UUID

from django.http import HttpRequest, HttpResponse

from session.session_store import SessionManager


class MySessionMiddleware:
    def __init__(self, get_response: Callable) -> None:
        self.get_response = get_response

    def __call__(self, request: HttpRequest) -> HttpResponse:
        if request_session_id := request.COOKIES.get("sessionid"):
            print("*** request cookies sessionid", request_session_id)
            print("*** request cookies sessionid type", type(request_session_id))

            request_session_id = UUID(request_session_id)

            # note that if the request_session_id does not exists in the DB,
            # the SessionManager will create a new MySession object
            session_manager = SessionManager.load_or_create_session(request_session_id)

            if session_manager.is_valid():
                request.session = session_manager.session_obj
            else:
                request.session = SessionManager.create_new_session().session_obj

        else:
            request.session = SessionManager.create_new_session().session_obj
        # the above if clause shall refactor later!!

        response = self.get_response(request)
        # response.set_cookie("sessionid", request.session.session_id)
        # if request.session.is_session_modified:
        #   save session data to database
        return response
