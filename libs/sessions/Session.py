class Session:
    def __init__(self, session_id: str, session_key: bytes):
        self.session_id = session_id
        self.session_key = session_key
        self.server_next_nonce = 0
        self.client_next_nonce = 0

    def get_session_id(self):
        return self.session_id

    def get_session_key(self):
        return self.session_key

    def get_server_next_nonce(self):
        return self.server_next_nonce
    
    def get_client_next_nonce(self):
        return self.client_next_nonce

    def increment_server_nonce(self):
        self.server_next_nonce += 1

    def increment_client_nonce(self):
        self.client_next_nonce += 1
        