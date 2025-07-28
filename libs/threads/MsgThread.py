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

class MsgThread(Thread):
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
        print("\nThe client has issued a MSG command")
        
        with self.threadLock:
            toUser = self.request.get_payload()["TO_USER"]
            fromUser = self.request.get_payload()["FROM_USER"]
            msg = self.request.get_payload()["MESSAGE"]
            timestamp = self.request.get_payload()["TIMESTAMP"]

            database = Database()
            database.add_msg(fromUser, toUser, msg, timestamp)

            response: Response = ResponseFactory.create_response(
                status=constants.MSG_SUCCESS,
                payload={},
                metadata={},
                keyManager=self.keyManager
            )

            print("Response for the MSG command:")
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

            print("Message successfully sent to the recipient!")
            print("Sending a response back to the client")
            