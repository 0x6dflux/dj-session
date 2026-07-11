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
        expiration_date: datetime | None = None,
    ) -> None:
        self.session_id = id or uuid4()
        self.session_data = data or {}
        self.expiration_date = expiration_date or (timezone.now() + timedelta(days=1))
        self.is_session_modified = False
        self.is_retrieved_from_db = False
        # the below attribute, prevents a query to be performed multiple times
        self.session_db_obj: SessionModel | None = None

    def __contains__(self, item):
        return item in self.session_data

    def __getitem__(self, key: str) -> Any:
        return self.session_data.get(key)

    def __setitem__(self, key: str, value: Any) -> None:
        self.session_data[key] = value
        self.is_session_modified = True

    def get(self, key):
        return self.session_data.get(key)

    def cycle_key(self):
        pass


class SessionManager:
    def __init__(self) -> None:
        self.session_obj: MySession | None = None

    def load_session(self, session_id: UUID):
        """
        It is assumed that the self is a new raw instance of the SessionManager class.
        The middleware creates this object using the SessionManager.create_new_session method.

        Args:
            session_id (UUID): _description_
            This argument is set by the request.COOKIES.get("sessionid"),
            which is used by the Django ORM to find the session model stored in the DB.

        Raises:
            MultipleObjectsReturned: _description_

        Returns:
            _type_: _description_
        """

        try:
            session_model = SessionModel.objects.get(session_id=session_id)

            # data shall be decoded, if needed

            if not SessionManager.is_valid(session_model.expiration_date):
                # if the stored session in the database is expired
                # the SessionManager.load_session method shall create a new session instance
                self.create_new_session()

            else:
                self.session_obj = MySession(
                    id=session_model.session_id,
                    data=session_model.session_data,
                    expiration_date=session_model.expiration_date,
                )

                self.session_obj.is_retrieved_from_db = True
                self.session_obj.session_db_obj = session_model

        except SessionModel.DoesNotExist:
            # if the get query raises this error
            # the SessionManager.load_session method shall create a new session instance
            self.create_new_session()

        # this exception may be changed in the future
        # it is not desirable that the system crashes
        except SessionModel.MultipleObjectsReturned:
            raise MultipleObjectsReturned(
                "Multiple objects returned in the MySessionMiddleware."
            )

    def create_new_session(self):
        self.session_obj = MySession()

    @staticmethod
    def is_valid(expiration_date: datetime) -> bool:
        """
        This method checks whether the session is expired or not.
        """

        return timezone.now() < expiration_date

    def save_session(self):
        """
        This method will insert the session_data into the DB
        """

        if self.session_obj.is_retrieved_from_db:
            if self.session_obj.is_session_modified:
                # overwriting the session_data of the db object with the modified data
                self.session_obj.session_db_obj.session_data = (
                    self.session_obj.session_data
                )
                self.session_obj.session_db_obj.save()
            # the else statement is not needed,
            # since, the session_data has not been modified
            # do not insert the save expression after the if-else clause,
            # because it would affect the is_session_modified logic

        else:
            self.session_obj.session_db_obj = SessionModel(
                session_id=self.session_obj.session_id,
                session_data=self.session_obj.session_data,
                expiration_date=self.session_obj.expiration_date,
            )
            self.session_obj.session_db_obj.save()
