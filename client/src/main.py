""" Client main file """

import sys
import unbox_client

def main():
    client = unbox_client.UnBoxClient()
    client.main_loop()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        sys.exit(0)
