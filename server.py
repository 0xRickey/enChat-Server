import socket, sys, threading
from libs.constants import MAX_BUFFER_SIZE_IN_BYTES, LOCAL_HOST_IP

def start_server():
    serverIpAddr = LOCAL_HOST_IP
    serverPort = int(sys.argv[1])

    serverUdpSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    serverUdpSocket.bind((serverIpAddr, serverPort))

    threadLock = threading.Lock()

    while True:
        clientBytesMsg, clientSocketAddr = serverUdpSocket.recvfrom(MAX_BUFFER_SIZE_IN_BYTES)
        
        print("Message received from client!")

if __name__ == "__main__":
    try:
        start_server()
    except KeyboardInterrupt:
        print("Keyboard Interrupt detected, exiting gracefully...")