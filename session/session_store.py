from datetime import timedelta
from typing import Any
from uuid import uuid4

from django.utils import timezone


class MySession:
    def __init__(self, data: dict[str, Any]) -> None:
        self.session_id = uuid4()
        self.session_data = data
        self.expiration_date = timezone.now() + timedelta(days=1)
        self.is_session_modified = False

    def __getitem__(self, key: str) -> Any:
        return self.session_data.get(key)

    def __setitem__(self, key: str, value: Any) -> None:
        self.session_data[key] = value
        self.is_session_modified = True


class SessionManager:
    def __init__(self, session_obj: MySession) -> None:
        self.session_obj = session_obj

# class SessionManager:

    def is_valid(self) -> bool:
        """
        This method checks whether the session is expired or not.
        """

        return timezone.now() < self.session_obj.expiration_date
