from threading import Thread
import server

RECV_TIMEOUT = 5.0


class ClientHandler:
    def __init__(self, connection):
        self.connection = connection

        # The listen thread will be stopped gracefully ASAP when this is switched to True.
        self.isStopping = False

        self.listen_thread = Thread(target=self.__listen)
        self.listen_thread.start()

    def __listen(self):
        print("Connected: " + str(self.connection))
        while True:
            message = self.connection.receive(RECV_TIMEOUT)
            if message == "":
                self.isStopping = True
            elif message != None:
                server.broadcast(message, self.connection)

            if self.isStopping:
                print("Disconnected: " + str(self.connection))
                server.remove_handler(self.connection)
                self.connection.close()
                break

    def send(self, message):
        self.connection.send(message)

    def close(self):
        self.isStopping = True
