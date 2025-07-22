from libs.requests.Request import Request
from libs.threads.NewSessionThread import NewSessionThread
from server import Server

class ThreadFactory:
    @staticmethod
    def create_thread(request: Request, server: Server):
        match request.get_command():
            case "START_SESSION":
                return NewSessionThread(request, server)
            case _:
                return