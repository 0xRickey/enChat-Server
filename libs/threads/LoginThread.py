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

class LoginThread(Thread):
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
        print(f"\nThe client has requested to login")

        with self.threadLock:
            username: str = self.request.get_payload()["USERNAME"]
            password: str = self.request.get_payload()["PASSWORD"]

            database = Database()

            # first check if the user exists
            if not database.does_user_exist(username):
                print(f"Error: there is no user with username {username}")
                status = constants.USER_DOES_NOT_EXIST

            # then check if logging in is ok
            elif not database.try_user_login(username, password):
                status = constants.INCORRECT_PASSWORD

            else:
                status = constants.LOGIN_SUCCESS

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

            print("Successfully username and password match, logging user in")
            print("Sending a response back to the client")
            