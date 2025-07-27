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

class GetPubKeyThread(Thread):
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
        print("\nThe client has issed an GET_PUB_KEY command")

        with self.threadLock:
            database = Database()
            targetUser = self.request.get_payload()["TARGET_USER"]
            
            if not database.does_user_exist(targetUser):
                status = constants.USER_DOES_NOT_EXIST
                payload = {}
            else:
                status = constants.USER_EXISTS
                payload = {
                    "PUBLIC_KEY": database.get_user_pub_key(targetUser)
                }

            response: Response = ResponseFactory.create_response(
                status=status,
                payload=payload,
                metadata={},
                keyManager=self.keyManager
            )
            print("Response for the GET_PUB_KEY command:")
            pprint(response.as_dict())

            self.responseLog.add_response(response)

            session: Session = self.sessionsLog.get_session(
                self.request.get_session_id()
            )

            aesEncryptedResBytes: bytes = self.encryptor.AES_encrypt(
                response=response,
                session_key=session.get_expanded_session_key()
            )

            self.serverUdpSocket.sendto(
                aesEncryptedResBytes,
                self.request.get_return_addr()
            )

            print("The requested user exists and their public key was retrieved")
            print("Sending a response back to the client")