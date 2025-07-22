from libs.sessions.Session import Session

class SessionsLog:
    def __init__(self):
        self.sessions = {}

    def add_session(self, session: Session):
        self.sessions[session.session_id] = session

    def remove_session(self, session_id: str):
        del self.sessions[session_id]

    def session_exists(self, session_id: str):
        return session_id in self.sessions.keys()

    def get_session(self, session_id: str):
        return self.sessions[session_id]