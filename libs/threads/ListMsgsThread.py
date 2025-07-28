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
from libs.Message import Message

class ListMsgsThread(Thread):
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
        print("\nThe Client has issued a LIST command")
        with self.threadLock:
            fromUser = self.request.get_payload()["FROM_USER"]
            toUser   = self.request.get_payload()["TO_USER"]

            database = Database()
            chat = database.get_messages(fromUser, toUser)

            if not database.does_user_exist(fromUser):
                status = constants.USER_DOES_NOT_EXIST
                payload = {}
            elif chat == None:
                status = constants.NO_CHATS
                payload = {}
            else:
                status = constants.LIST_SUCCESS
                payload = {
                    "MESSAGES": [msg.as_dict() for msg in chat]
                }

            response: Response = ResponseFactory.create_response(
                status=status,
                payload=payload,
                metadata={},
                keyManager=self.keyManager
            )

            print("Response for the LIST command:")
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

            print("Sending the response back to the client")