from datetime import datetime, timedelta
from typing import Any
from uuid import UUID, uuid4

from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist
from django.utils import timezone

from session.models import SessionModel


class MySession:
    def __init__(
        self,
        id: UUID | None = None,
        data: dict[str, Any] | None = None,
        exp_date: datetime | None = None,
    ) -> None:
        self.session_id = id or uuid4()
        self.session_data = data or {}
        self.expiration_date = exp_date or (timezone.now() + timedelta(days=1))
        self.is_session_modified = False

    def __getitem__(self, key: str) -> Any:
        return self.session_data.get(key)

    def __setitem__(self, key: str, value: Any) -> None:
        self.session_data[key] = value
        self.is_session_modified = True


class SessionManager:
    def __init__(self, session_obj: MySession) -> None:
        self.session_obj = session_obj

    @classmethod
    def load_or_create_session(cls, session_id: UUID):
        try:
            session_model = SessionModel.objects.get(session_id=session_id)
            # data shall be decoded, if needed
            my_session = MySession(
                session_model.session_data,
                session_model.session_id,
                session_model.expiration_date,
            )
            return SessionManager(my_session)
        except ObjectDoesNotExist:
            return cls.create_new_session()
        except MultipleObjectsReturned:
            raise MultipleObjectsReturned(
                "Multiple objects returned in the MySessionMiddleware."
            )

    @classmethod
    def create_new_session(cls):
        return SessionManager(MySession({}))

    def is_valid(self) -> bool:
        """
        This method checks whether the session is expired or not.
        """

        return timezone.now() < self.session_obj.expiration_date
