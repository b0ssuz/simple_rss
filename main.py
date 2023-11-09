'''
GNU GENERAL PUBLIC LICENSE
Version 3, 29 June 2007

Copyright (C) 2023 Bünyamin Sarikaya

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
'''

import os
import sys
import curses
from rss import RSS

def main(stdscr):
    my_feed = RSS()
    selected = 0
    scroll_offset = 0  # Added to keep track of scrolling

    while True:
        height, width = stdscr.getmaxyx()
        items = my_feed.get_headlines(with_read=False)
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
            if item_index < len(items) and i == selected - scroll_offset:
                stdscr.addstr(i, 0, f"> {items[item_index]}", curses.A_STANDOUT)
            elif item_index < len(items):
                stdscr.addstr(i, 0, f"  {items[item_index]}")

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
            # Handle the selected item
            stdscr.clear()  # Clear the screen
            my_feed.mark_as_read(selected)
            stdscr.addstr(0, 0, my_feed.get_description(selected))
            stdscr.addstr(3, 0, my_feed.get_article_url(selected))
            stdscr.addstr(height - 1, 0, f"Selected: {items[selected]}, Index: {selected}")
            stdscr.refresh()
            stdscr.getch()
        elif key == 27 or key == ord("q"):  # Escape key or q to exit
            break
        else:
            continue

if __name__ == "__main__":
    curses.wrapper(main)

