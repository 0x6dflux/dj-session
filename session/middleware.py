from typing import Callable
from uuid import UUID

from django.http import HttpRequest, HttpResponse

from session.session_store import SessionManager


class MySessionMiddleware:
    def __init__(self, get_response: Callable) -> None:
        self.get_response = get_response

    def __call__(self, request: HttpRequest) -> HttpResponse:
        session_manager = SessionManager.create_new_session()

        if request_session_id := request.COOKIES.get("sessionid"):
            print("*** request cookies sessionid", request_session_id)
            # delete later
            print("*** request cookies sessionid type", type(request_session_id))
            # delete later

            # converting from str to uuid
            # the type of the sessionid value in the cookies, is str
            session_manager = session_manager.load_session(UUID(request_session_id))
            # note that if the request_session_id does not exists in the DB,
            # the SessionManager will create a new MySession object

        request.session = session_manager.session_obj

        response = self.get_response(request)

        response.set_cookie("sessionid", request.session.session_id)
        # print("*** request session is_modified", request.session.is_session_modified)
        # request.session["user"] = request.user.pk
        # print("*** request session is_modified", request.session.is_session_modified)
        # session_manager
        # if request.session.is_session_modified:
        #   encode the data
        #   save session data to database
        return response
