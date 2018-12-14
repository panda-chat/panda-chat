#!/usr/bin/env python3

import server
from socket_listener import SocketListener
from socket_connection import SocketConnection

if __name__ == "__main__":
    server.start(
        SocketListener(
            lambda client_address: SocketConnection(
                client_address[0], client_address[1]
            )
        )
    )
