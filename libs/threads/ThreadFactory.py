from libs.requests.Request import Request
from libs.threads.NewSessionThread import NewSessionThread
from libs.sessions.SessionsLog import SessionsLog
from libs.response.ResponseLog import ResponseLog
from libs.KeyManager import KeyManager
from libs.Encryptor import Encryptor
from threading import Lock
import socket

class ThreadFactory:
    @staticmethod
    def create_thread(
        request: Request,
        threadLock: Lock,
        serverUdpSocket: socket.socket,
        sessionsLog: SessionsLog,
        responseLog: ResponseLog,
        keyManager: KeyManager,
        encryptor: Encryptor
    ):
        match request.get_command():
            case "START_SESSION":
                return NewSessionThread(
                    request,
                    threadLock,
                    serverUdpSocket,
                    sessionsLog,
                    responseLog,
                    keyManager,
                    encryptor
                )
            case _:
                return