""" Código principal de chamada do servidor """

import unbox_server
import sys

def main():
    """ Main function """
    server = unbox_server.UnBoxServer()
    while True:
        server.serve()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        sys.exit(0)
