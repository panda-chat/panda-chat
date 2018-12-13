from socket import socket, AF_INET, SOCK_STREAM, timeout
from threading import Thread

HOST = "127.0.0.1"
PORT = 38383
BUFFER_SIZE = 1024
TIMEOUT = 5.0


class TestClient:
    def __init__(self):
        self.socket = socket(AF_INET, SOCK_STREAM)
        self.socket.connect((HOST, PORT))
        self.socket.settimeout(TIMEOUT)

        self.isStopping = False
        recv_thread = Thread(target=self.__receive)
        recv_thread.start()

        while True:
            try:
                self.socket.send(bytes(input(), "utf8"))
            except Exception as e:
                print("Fatal error: " + e.message)
                break
            # The only way to shutdown the test client is by Ctrl-C key interrupt.
            except KeyboardInterrupt:
                print("Shutting down...")
                break

        self.isStopping = True
        recv_thread.join()
        self.socket.close()

    def __receive(self):
        while True:
            try:
                message = self.socket.recv(BUFFER_SIZE).decode("utf8")
                if message:
                    print(message)
                else:
                    self.isStopping = True
            except timeout:
                pass

            if self.isStopping:
                break


TestClient()
