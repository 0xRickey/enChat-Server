from libs.requests.Request import Request
from libs.sessions.Session import Session

class SessionFactory:
    @staticmethod
    def new_session(request: Request) -> Session:
        session_id: int = request.get_payload()["SESSION_ID"]
        session_key: int = request.get_payload()["SESSION_KEY"]
        return Session(session_id, session_key)
