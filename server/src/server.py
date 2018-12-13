from socket import socket, AF_INET, SOCK_STREAM, timeout
from client_handler import ClientHandler

HOST = ""
PORT = 38383
ACCEPT_TIMEOUT = 5.0

client_handlers = {}


def start():
    panda_sock = socket(AF_INET, SOCK_STREAM)
    panda_sock.bind((HOST, PORT))

    # Should the optional "backlog" parameter be set here?
    # What is a "default reasonable value" (https://docs.python.org/3/library/socket.html)?
    panda_sock.listen()

    # Stop blocking every so often so the main thread can be stopped if needed.
    # I feel like there may be a better way to handle this.
    # If a client attempts to connect during the very brief time between
    #     calls to accept(), will it fail?
    panda_sock.settimeout(ACCEPT_TIMEOUT)

    while True:
        try:
            try:
                client, address = panda_sock.accept()
                client_handlers[address] = ClientHandler(client, address)
            except timeout:
                pass
        except Exception as e:
            print("Fatal error: " + e.message)
            break
        # For now, the only way to shutdown the server is by Ctrl-C key interrupt.
        except KeyboardInterrupt:
            print("Shutting down...")
            break

    for handler in client_handlers.values():
        handler.close()

    panda_sock.close()


def broadcast(message, from_address):
    for address, handler in client_handlers.items():
        if address != from_address:
            handler.send(str(from_address) + ": " + message)


def remove_handler(address):
    del client_handlers[address]
