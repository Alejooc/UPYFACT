import curses

def capture_key_sequences():
    def get_key_code(stdscr):
        stdscr.nodelay(True)
        while True:
            key = stdscr.getch()
            if key != -1:
                print(f"Key code: {key}, Character: {chr(key)}")
            if key == ord('q'):  # Press 'q' to quit
                break

    curses.wrapper(get_key_code)

if __name__ == "__main__":
    capture_key_sequences()