import time, socket

import libs.constants as constants


from threading import Thread, Lock

from libs.requests.Request import Request
from libs.sessions.SessionsLog import SessionsLog
from libs.sessions.Session import Session
from libs.response.ResponseLog import ResponseLog
from libs.response.Response import Response
from libs.response.ResponseFactory import ResponseFactory
from libs.KeyManager import KeyManager
from libs.Encryptor import Encryptor
from libs.Database import Database

class CheckUsernameThread(Thread):
    def __init__(
        self,
        request: Request,
        threadLock: Lock,
        serverUdpSocket: socket.socket,
        sessionsLog: SessionsLog,
        responseLog: ResponseLog,
        keyManager: KeyManager,
        encryptor: Encryptor
    ):
        super().__init__()
        self.request: Request = request
        self.threadLock: Lock = threadLock
        self.serverUdpSocket: socket.socket = serverUdpSocket
        self.sessionsLog: SessionsLog = sessionsLog
        self.responseLog: ResponseLog = responseLog
        self.keyManager: KeyManager = keyManager
        self.encryptor: Encryptor = encryptor

    def run(self):
        print(f"The client has requested to check the availability of a username")
        with self.threadLock:
            database: Database = Database()
            username: str = self.request.get_payload()["USERNAME"]
            
            if database.does_user_exist(username):
                print(f"The username '{username}' is unavailable")
                status = constants.USERNAME_TAKEN
            else:
                print(f"The username '{username}' is available")
                status = constants.USERNAME_AVAILABLE

            response: Response = ResponseFactory.create_response(
                status=status,
                payload={},
                metadata={},
                keyManager=self.keyManager
            )

            session: Session = self.sessionsLog.get_session(
                self.request.get_session_id()
            )

            aesEncryptedResBytes: bytes = self.encryptor.AES_encrypt(
                response=response,
                session_key=session.get_expanded_session_key()
            )

            self.responseLog.add_response(response)

            self.serverUdpSocket.sendto(
                aesEncryptedResBytes,
                self.request.get_return_addr()
            )

            print("Response sent to client")