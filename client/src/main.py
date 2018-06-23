""" Client main file """

import sys
import main_window

def main():
    ui = main_window.MainWindow()
    ui.setup()
    while ui.main_loop():
        pass

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        sys.exit(0)
