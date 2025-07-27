import socket

import libs.constants as constants

from threading import Lock

from libs.requests.Request import Request
from libs.threads.NewSessionThread import NewSessionThread
from libs.threads.CheckUsernameThread import CheckUsernameThread
from libs.threads.RegisterUserThread import RegisterUserThread
from libs.threads.LoginThread import LoginThread
from libs.threads.LogoutThread import LogoutThread
from libs.threads.GetPubKeyThread import GetPubKeyThread
from libs.threads.MsgThread import MsgThread
from libs.sessions.SessionsLog import SessionsLog
from libs.response.ResponseLog import ResponseLog
from libs.KeyManager import KeyManager
from libs.Encryptor import Encryptor

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
            case constants.START_SESSION:
                return NewSessionThread(
                    request,
                    threadLock,
                    serverUdpSocket,
                    sessionsLog,
                    responseLog,
                    keyManager,
                    encryptor
                )
            case constants.CHECK_USERNAME:
                return CheckUsernameThread(
                    request,
                    threadLock,
                    serverUdpSocket,
                    sessionsLog,
                    responseLog,
                    keyManager,
                    encryptor
                )
            case constants.REGISTER_USER:
                return RegisterUserThread(
                    request,
                    threadLock,
                    serverUdpSocket,
                    sessionsLog,
                    responseLog,
                    keyManager,
                    encryptor
                )
            case constants.LOGIN:
                return LoginThread(
                    request,
                    threadLock,
                    serverUdpSocket,
                    sessionsLog,
                    responseLog,
                    keyManager,
                    encryptor
                )
            case constants.EXIT:
                return LogoutThread(
                    request,
                    threadLock,
                    serverUdpSocket,
                    sessionsLog,
                    responseLog,
                    keyManager,
                    encryptor
                )
            case constants.GET_PUB_KEY:
                return GetPubKeyThread(
                    request,
                    threadLock,
                    serverUdpSocket,
                    sessionsLog,
                    responseLog,
                    keyManager,
                    encryptor
                )
            case constants.MSG:
                return MsgThread(
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