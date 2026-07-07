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


# class SessionManager:
