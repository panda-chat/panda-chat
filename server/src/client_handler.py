from socket import timeout
from threading import Thread
import server

BUFFER_SIZE = 1024
RECV_TIMEOUT = 5.0


class ClientHandler:
    def __init__(self, socket, address):
        self.socket = socket
        self.address = address

        # Stop blocking every so often so the thread can be stopped if needed.
        # See server.py for more detail.
        self.socket.settimeout(RECV_TIMEOUT)

        # The listen thread will be stopped gracefully ASAP when this is switched to True.
        self.isStopping = False

        self.listen_thread = Thread(target=self.__listen)
        self.listen_thread.start()

    def __listen(self):
        print("Connected: " + str(self.address))
        while True:
            try:
                message = self.socket.recv(BUFFER_SIZE).decode("utf8")
                if message:
                    server.broadcast(message, self.address)
                else:
                    self.isStopping = True
            except timeout:
                pass

            if self.isStopping:
                print("Disconnected: " + str(self.address))
                server.remove_handler(self.address)
                self.socket.close()
                break

    def send(self, message):
        self.socket.send(bytes(message, "utf8"))

    def close(self):
        self.isStopping = True
