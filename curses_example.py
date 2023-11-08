import curses

def main(stdscr):
    # Set up the screen
    curses.curs_set(0)
    stdscr.clear()
    stdscr.refresh()

    items = ["Option 1", "Option 2", "Option 3", "Option 4"]
    selected = 0

    while True:
        stdscr.clear()
        height, width = stdscr.getmaxyx()

        # Print the list of items
        for i, item in enumerate(items):
            if i == selected:
                stdscr.addstr(i, 0, f"> {item}", curses.A_STANDOUT)
            else:
                stdscr.addstr(i, 0, f"  {item}")

        stdscr.refresh()

        # Wait for user input
        key = stdscr.getch()

        if key == ord("j") and selected < len(items) - 1:
            selected += 1
        elif key == ord("k") and selected > 0:
            selected -= 1
        elif key == 10:  # Enter key
            # Handle the selected item (you can add your logic here)
            stdscr.addstr(height - 1, 0, f"Selected: {items[selected]}")
            stdscr.refresh()
            stdscr.getch()
            print("HELLO")
        elif key == 27:  # Escape key to exit
            break

if __name__ == "__main__":
    curses.wrapper(main)

