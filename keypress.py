import sys

if False: # "Windows":
    import msvcrt
    def _getch():
        return msvcrt.getwch()
else:
    import tty
    import termios
    def _getch():
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
            return ch

    def getch():
        ch = _getch()
        return ch

if __name__ == "__main__":
    i = 0
    while i < 12:
        key = str(getch())
        key = key.encode()
        print(type(key))
        print(str(key))
        i += 1
            
