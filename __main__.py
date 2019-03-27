import asyncore
import signal
import socket
import sys

class Server(asyncore.dispatcher):
    def __init__(self):
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.bind(('0.0.0.0', 0))
        self.listen(10)
    @property
    def port(self):
        return self.socket.getsockname()[1]
    def handle_accept(self):
        sock, addr = self.accept()
        Handler(sock)

class Handler(asyncore.dispatcher_with_send):
    def __init__(self, sock):
        asyncore.dispatcher_with_send.__init__(self, sock)
    def handle_read(self):
        print(self.recv(1024))
        response = input('Response: ').strip()
        if not response or response == 'quit':
            return
        self.send('{}\n'.format(response).encode())

if __name__ == '__main__':
    server = Server()
    def sys_exit(*args):
        sys.exit(0)
    signal.signal(signal.SIGTERM, sys_exit)

    try:
        print('port: {}'.format(server.port))
        asyncore.loop()
    except KeyboardInterrupt:
        pass
    finally:
        asyncore.close_all()
        sys.exit(0)
