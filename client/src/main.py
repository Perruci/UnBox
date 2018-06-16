""" Client main file """

import sys
import unbox_client

def main():
    client = unbox_client.UnBoxClient()
    while client.main_loop():
        pass

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        sys.exit(0)
