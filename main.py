from rss import RSS
import webbrowser
import subprocess
import signal
import sys
import curses

def goodbye_message():
    print("\n \n Goodbye! \n\n")
    # Add any other cleanup tasks here
    sys.exit(0)

# Register the goodbye_message function to be called on Ctrl+C
signal.signal(signal.SIGINT, lambda signal, frame: goodbye_message())

# use curses to display the feed

def main(stdscr):
    my_feed = RSS()
    selected = 0
    scroll_offset = 0  # Added to keep track of scrolling

    try:
        while True:
            height, width = stdscr.getmaxyx()
            items = my_feed.get_headlines()
            num_displayed_items = min(height, len(items))
            
            # Adjust the selected item if it goes out of the visible region
            if selected < scroll_offset:
                scroll_offset = selected
            elif selected >= scroll_offset + num_displayed_items:
                scroll_offset = selected - num_displayed_items + 1

            stdscr.clear()

            # Print the list of items within the visible region
            for i in range(num_displayed_items):
                item_index = i + scroll_offset
                item = items[item_index]

                if i == selected - scroll_offset:
                    stdscr.addstr(i, 0, f"> {item}", curses.A_STANDOUT)
                else:
                    stdscr.addstr(i, 0, f"  {item}")

            stdscr.refresh()

            key = stdscr.getch()

            if key == ord("j") and selected < len(items) - 1:
                selected += 1
            elif key == ord("k") and selected > 0:
                selected -= 1
            elif key == curses.KEY_DOWN and selected < len(items) - 1:
                selected += 1
            elif key == curses.KEY_UP and selected > 0:
                selected -= 1
            elif key == 10:  # Enter key
                # Handle the selected item (you can add your logic here)
                stdscr.clear()  # Clear the screen
                for i in range(10):
                    stdscr.addstr(i, 0, f"Item {selected} selected")
                stdscr.addstr(height - 1, 0, f"Selected: {items[selected]}, Index: {selected}")
                stdscr.refresh()
                stdscr.getch()
            elif key == 27 or ord("q"):  # Escape key to exit
                break
            else:
                continue

    except KeyboardInterrupt:
        goodbye_message()

if __name__ == "__main__":
    curses.wrapper(main)

