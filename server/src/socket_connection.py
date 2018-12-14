from socket import timeout

BUFFER_SIZE = 1024


class SocketConnection:
    def __init__(self, socket, address):
        self.socket = socket
        self.address = address

    def __str__(self):
        return str(self.address)

    # Returns message as a string.
    #     An empty string means the client has closed the connection.
    #     None means the timeout has expired.
    def receive(self, timeout_seconds):
        try:
            self.socket.settimeout(timeout_seconds)
            return self.socket.recv(BUFFER_SIZE).decode("utf8")
        except timeout:
            return None

    def send(self, message):
        self.socket.send(bytes(message, "utf8"))

    def close(self):
        self.socket.close()
