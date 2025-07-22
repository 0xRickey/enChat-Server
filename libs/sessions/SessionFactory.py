from libs.Requests.Request import Request
from libs.sessions.Session import Session

class SessionFactory:
    @staticmethod
    def new_session(request: Request) -> Session:
        session_id: str = request.get_payload()["SESSION_ID"]
        session_key: bytes = request.get_payload()["SESSION_KEY"].encode()
        return Session(session_id, session_key)
