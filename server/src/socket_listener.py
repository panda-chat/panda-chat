from socket import socket, AF_INET, SOCK_STREAM, timeout

HOST = ""
PORT = 38383


class SocketListener:
    def __init__(self, connection_factory):
        self.connection_factory = connection_factory

        self.listen_socket = socket(AF_INET, SOCK_STREAM)
        self.listen_socket.bind((HOST, PORT))

        # Should the optional "backlog" parameter be set here?
        # What is a "default reasonable value" (https://docs.python.org/3/library/socket.html)?
        self.listen_socket.listen()

    # Returns connection.
    def accept_connections(self, timeout_seconds):
        try:
            self.listen_socket.settimeout(timeout_seconds)
            return self.connection_factory(self.listen_socket.accept())
        except timeout:
            return None

    def close(self):
        return self.listen_socket.close()
