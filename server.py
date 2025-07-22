import socket, sys, threading
from libs.constants import MAX_BUFFER_SIZE_IN_BYTES, SERVER_IP_ADDR, SERVER_PORT
from libs.KeyManager import KeyManager
from libs.Decryptor import Decryptor
from libs.Requests.RequestFactory import RequestFactory
from libs.sessions.SessionsLog import SessionsLog
from libs.response.ResponseLog import ResponseLog
from libs.threads.ThreadFactory import ThreadFactory

class Server:
    def __init__(self):
        self.serverUdpSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.serverUdpSocket.bind((SERVER_IP_ADDR, SERVER_PORT))
        self.threadLock = threading.Lock()
        self.sessionsLog = SessionsLog()
        self.keyManager = KeyManager()
        self.decryptor = Decryptor(self.keyManager)
        self.requestFactory = RequestFactory(self.decryptor)
        self.responseLog = ResponseLog()

    def start_server(self):
        print("Server started")
        while True:
            clientBytesMsg, clientSocketAddr = self.serverUdpSocket.recvfrom(MAX_BUFFER_SIZE_IN_BYTES)
            print(f"Message received from client {clientSocketAddr}")

            # Extract the request from the message
            print(f"Decrypting and extracting request from message...")
            request = self.requestFactory.extract_request(clientBytesMsg)

            # check message integrity
            if not request.verify_integrity():
                print("Message integrity check failed")
                continue

            print("Message integrity check passed")

            newThread = ThreadFactory.create_thread(request, self)
            newThread.start()

if __name__ == "__main__":
    try:
        server = Server()
        server.start_server()
    except KeyboardInterrupt:
        print("Keyboard Interrupt detected, exiting gracefully...")