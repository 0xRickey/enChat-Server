import time, socket

import libs.constants as constants

from threading import Thread, Lock
from pprint import pprint

from libs.requests.Request import Request
from libs.sessions.SessionsLog import SessionsLog
from libs.sessions.Session import Session
from libs.response.ResponseLog import ResponseLog
from libs.response.Response import Response
from libs.response.ResponseFactory import ResponseFactory
from libs.KeyManager import KeyManager
from libs.Encryptor import Encryptor
from libs.Database import Database

class LogoutThread(Thread):
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
        print("\nThe client has issued an EXIT command")
        
        with self.threadLock:
            session_id: int = self.request.get_metadata()["SESSION_ID"]
            self.sessionsLog.remove_session(session_id)

            response: Response = ResponseFactory.create_response(
                status=constants.LOGOUT_SUCCESS,
                payload={},
                metadata={},
                keyManager=self.keyManager
            )
            print("Response for the EXIT command:")
            pprint(response.as_dict())

            self.responseLog.add_response(response)

            rsaEncryptedResBytes: bytes = self.encryptor.RSA_encrypt(
                response=response,
                PEM_pub_key=self.request.get_PEM_pub_key()
            )

            self.serverUdpSocket.sendto(
                rsaEncryptedResBytes,
                self.request.get_return_addr()
            )

        print("Successfully removed the client's session. User is now logged out")
        print("Sending a response back to the client")


            
