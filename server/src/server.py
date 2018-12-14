from client_handler import ClientHandler

# Stop blocking to accept every so often so the main thread can be stopped if needed.
# I feel like there may be a better way to handle this.
# If a client attempts to connect during the very brief time between
#     calls to accept_connections(), will it fail?
ACCEPT_TIMEOUT = 5.0

client_handlers = {}


def start(listener):
    while True:
        try:
            connection = listener.accept_connections(ACCEPT_TIMEOUT)
            if connection != None:
                client_handlers[str(connection)] = ClientHandler(connection)
        except Exception as e:
            print("Fatal error: " + e.message)
            break
        # For now, the only way to shutdown the server is by Ctrl-C key interrupt.
        except KeyboardInterrupt:
            print("Shutting down...")
            break

    for handler in client_handlers.values():
        handler.close()

    listener.close()


def broadcast(message, from_connection):
    from_key = str(from_connection)
    for key, handler in client_handlers.items():
        if key != from_key:
            handler.send(from_key + ": " + message)


def remove_handler(connection):
    del client_handlers[str(connection)]
