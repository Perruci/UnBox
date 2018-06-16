""" Código principal de chamada do servidor """

import socket
import client_thread
import sys

def main():
    LOCALHOST = ''
    PORT = 8888
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((LOCALHOST, PORT))
    print("Server started")
    print("Waiting for client request..")
    while True:
        server.listen(1)
        clientsock, clientAddress = server.accept()
        newthread = client_thread.ClientThread(clientAddress, clientsock)
        newthread.start()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        sys.exit(0)
