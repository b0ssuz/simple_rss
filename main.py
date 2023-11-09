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

import curses
from rss import RSS

def display_items(stdscr, items, selected, scroll_offset):
    height, width = stdscr.getmaxyx()
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

def handle_selected_item(stdscr, my_feed, items, selected):
    height = stdscr.getmaxyx()[0]
    stdscr.clear()  # Clear the screen
    my_feed.mark_as_read(selected)
    stdscr.addstr(0, 0, my_feed.get_description(selected))
    stdscr.addstr(10, 0, my_feed.get_article_url(selected))
    stdscr.addstr(height - 1, 0, f"Selected: {items[selected]}, Index: {selected}")
    stdscr.refresh()
    stdscr.getch()

def main(stdscr):
    my_feed = RSS()
    selected = 0
    scroll_offset = 0  # Added to keep track of scrolling

    while True:
        items = my_feed.get_headlines(with_read=False)

        display_items(stdscr, items, selected, scroll_offset)

        key = stdscr.getch()

        if key in [curses.KEY_DOWN, ord("j")] and selected < len(items) - 1:
            selected += 1
        elif key in [curses.KEY_UP, ord("k")] and selected > 0:
            selected -= 1
        elif key in [10, ord("l")]:  # Enter or l key to select
            handle_selected_item(stdscr, my_feed, items, selected)
        elif key in [27, ord("q")]:  # Escape key or q to exit
            break

if __name__ == "__main__":
    curses.wrapper(main)

