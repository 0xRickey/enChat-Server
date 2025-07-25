import time, socket

import libs.constants as constants

from threading import Thread, Lock

from libs.requests.Request import Request
from libs.sessions.SessionFactory import SessionFactory
from libs.sessions.SessionsLog import SessionsLog
from libs.sessions.Session import Session
from libs.response.ResponseLog import ResponseLog
from libs.response.Response import Response
from libs.response.ResponseFactory import ResponseFactory
from libs.KeyManager import KeyManager
from libs.Encryptor import Encryptor

class NewSessionThread(Thread):
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
        print("Client initiated a start new session request")
        with self.threadLock:
            new_session: Session = SessionFactory.new_session(self.request)
            self.sessionsLog.add_session(new_session)

            # create response
            responseMsg: Response = ResponseFactory.create_response(
                status=constants.START_SESSION_SUCCESS,
                payload={
                    "SESSION_ID": new_session.get_session_id(),
                    "SERVER_NONCE": new_session.get_server_next_nonce(),
                    "TIMESTAMP": int(time.time())
                },
                metadata={},
                keyManager=self.keyManager
            )

            # encrypt message with session key (found in session object)
            aesEncryptedResBytes: bytes = self.encryptor.AES_encrypt(
                responseMsg,
                new_session.get_session_key()
                # init_vec field not included because we want the function to generate us one
            )

            # update response log
            self.responseLog.add_response(responseMsg)

            print("New Session Registered, Sending a response back to client")

            # send the encrypted response and
            # intitialisation vector to client via udp socket
            self.serverUdpSocket.sendto(
                aesEncryptedResBytes,
                self.request.get_address()
            )

            