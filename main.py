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
import webbrowser
from rss import RSS

class SimpleRSS:
    def __init__(self):
        """
        Initializes the SimpleRSS object.

        Attributes:
        - my_feed: An instance of the RSS class, representing the RSS feed.
        - selected: Index of the currently selected item in the feed.
        - scroll_offset: Offset used for scrolling through the feed items.
        - list_read_articles: Determines if read articles ar listed or not
        """
        self.my_feed = RSS()
        self.selected = 0
        self.scroll_offset = 0
        self.list_read_articles = False

    def display_items(self, stdscr):
        """
        Displays the RSS feed items on the terminal screen.

        Parameters:
        - stdscr: The curses standard screen object.

        This method calculates the number of items to display based on the terminal height,
        handles scrolling, and highlights the selected item.
        """
        height, width = stdscr.getmaxyx()
        num_displayed_items = min(height, len(self.items))

        if self.selected < self.scroll_offset:
            self.scroll_offset = self.selected
        elif self.selected >= self.scroll_offset + num_displayed_items:
            self.scroll_offset = self.selected - num_displayed_items + 1

        stdscr.clear()

        if num_displayed_items == 0:
            stdscr.addstr(0, 0, f"> Nothing left here.. press q to quit or b to browse read articles", curses.A_STANDOUT)
            # wait until closed
            while True:
                key = stdscr.getch()
                if key in [ord('q'), 27]:
                    exit(0)

        for i in range(num_displayed_items):
            item_index = i + self.scroll_offset
            if item_index < len(self.items) and i == self.selected - self.scroll_offset:
                stdscr.addstr(i, 0, f"> {self.items[item_index]}", curses.A_STANDOUT)
            elif item_index < len(self.items):
                stdscr.addstr(i, 0, f"  {self.items[item_index]}")

        stdscr.refresh()

    def handle_selected_item(self, stdscr):
        """
        Handles the selection of an RSS feed item, marking it as read and displaying details.

        Parameters:
        - stdscr: The curses standard screen object.

        Displays the item title, description, and URL. Opens the article in a web browser if 'l' or Enter is pressed.
        """
        height = stdscr.getmaxyx()[0]
        stdscr.clear()
        self.my_feed.mark_as_read(self.selected)
        stdscr.addstr(0, 0, self.items[self.selected])
        stdscr.addstr(2, 0, self.my_feed.get_description(self.selected))
        stdscr.addstr(12, 0, self.my_feed.get_article_url(self.selected))
        stdscr.addstr(height - 1, 0, "Press 'l' or Enter to open the article or any other key to go back")
        key = stdscr.getch()

        if key in [10, ord("l")]:
            webbrowser.open(self.my_feed.get_article_url(self.selected))

    def handle_key_press(self, stdscr, key):
        """
        Handles key presses during the main loop of the application.

        Parameters:
        - stdscr: The curses standard screen object.
        - key: The key code of the pressed key.

        Returns:
        - True if the key press signals to exit the loop, otherwise False.
        """
        if key in [curses.KEY_DOWN, ord("j")] and self.selected < len(self.items) - 1:
            self.selected += 1
        elif key in [curses.KEY_UP, ord("k")] and self.selected > 0:
            self.selected -= 1
        elif key in [10, ord("l")]:
            self.handle_selected_item(stdscr)
        elif key in [27, ord("q")]:
            return True  # Signal to exit the loop
        return False

    def run(self, stdscr):
        """
        Runs the main loop of the SimpleRSS application.

        Parameters:
        - stdscr: The curses standard screen object.

        This method continuously updates and displays the RSS feed items, handling key presses
        until a key press signals to exit the loop.
        """
        while True:
            self.items = self.my_feed.get_headlines(with_read=self.list_read_articles)

            self.display_items(stdscr)

            key = stdscr.getch()

            if self.handle_key_press(stdscr, key):
                break

if __name__ == "__main__":
    # Run the SimpleRSS application using curses.wrapper
    curses.wrapper(SimpleRSS().run)
