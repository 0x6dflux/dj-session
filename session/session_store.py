from typing import Any


class MySession:
    def __init__(self, data: dict[str, Any]):
        self.session_data = data
        self.is_session_modified = False

    def __getitem__(self, key: str) -> Any:
        return self.session_data.get(key)

    def __setitem__(self, key: str, value: Any) -> None:
        self.session_data[key] = value
        self.is_session_modified = True


# class SessionManager:
