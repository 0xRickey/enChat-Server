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
from server import Server

class NewSessionThread(Thread):
    def __init__(self, request: Request, server: Server):
        super().__init__()
        self.request: Request = request
        self.threadLock: Lock = server.threadLock
        self.serverUdpSocket: socket.socket = server.serverUdpSocket
        self.sessionsLog: SessionsLog = server.sessionsLog
        self.responseLog: ResponseLog = server.responseLog
        self.keyManager: KeyManager = server.keyManager
        self.encryptor: Encryptor = server.encryptor

    def run(self):
        with self.threadLock:
            new_session: Session = SessionFactory.new_session(self.request)
            self.sessionsLog.add_session(new_session)

            # create response
            response: Response = ResponseFactory.create_response(
                status=constants.START_SESSION_SUCCESS,
                payload={
                    "SESSION_ID": new_session.get_session_id(),
                    "SERVER_NONCE": new_session.get_server_next_nonce(),
                    "TIMESTAMP": int(time.time())
                },
                metadata={},
                keyManager=self.keyManager
            )

            # update response log
            self.responseLog.add_response(response)

            # encrypt with session key (found in session object)
            encrypted_response: bytes = self.encryptor.AES_encrypt(
                response,
                new_session.get_session_key()
            )

            # send the encrypted response and
            # intitialisation vector to client via udp socket
            self.serverUdpSocket.sendto(
                encrypted_response,
                self.request.get_address()
            )

            