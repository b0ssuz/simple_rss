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

from requests import get, ConnectionError
import hashlib
import os
from rss_parser import Parser

class RSS:
    """
    Represents an RSS feed manager with methods to load, retrieve, and manage feed data.

    Attributes:
    - RSS_FEEDS_FILE: A constant representing the file name storing the list of RSS feeds.
    - READ_ARTICLES_FILE: A constant representing the file name storing the list of read articles.

    Methods:
    - __init__(self): Initializes the RSS object and loads the RSS feeds.
    - load_feeds(self): Loads RSS feeds from the specified file, handles connection errors,
      and marks feeds as FAILED if necessary.
    - get_headlines(self, with_read: bool = True) -> list: Retrieves headlines from loaded feeds,
      optionally excluding already read articles.
    - get_description(self, index: int) -> str: Retrieves the description of the article at the specified index.
    - get_article_url(self, index: int) -> str: Retrieves the URL of the article at the specified index.
    - mark_as_read(self, index: int): Marks the article at the specified index as read.
    - is_read(self, index: int) -> bool: Checks if the article at the specified index is marked as read.

    """
    RSS_FEEDS_FILE = "feeds.lst"
    READ_ARTICLES_FILE = "read_articles.lst"

    def __init__(self) -> None:
        """
        Initializes the RSS object and loads the RSS feeds.
        """
        self.load_feeds()

    def load_feeds(self):
        """
        Loads RSS feeds from the specified file, handles connection errors,
        and marks feeds as FAILED if necessary.
        """
        with open(self.RSS_FEEDS_FILE, 'r') as file:
            lines = file.readlines()

        self.feeds = [line.strip() for line in lines]
        self.feeds_with_content = []

        for feed in self.feeds:
            if "FAILED" in feed:
                continue
            try:
                response = get(feed)
                rss = Parser.parse(response.text)
            except ConnectionError:
                exit("no internet connection")
            except Exception:
                # mark feed as FAILED in file
                with open(self.RSS_FEEDS_FILE) as f:
                    newText=f.read().replace(feed, f"{feed} FAILED")

                with open(self.RSS_FEEDS_FILE, "w") as f:
                    f.write(newText)
                continue
            for item in rss.channel.items:
                self.feeds_with_content.append(item)

    def get_headlines(self, with_read: bool = True) -> list:
        """
        Retrieves headlines from loaded feeds, optionally excluding already read articles.

        Parameters:
        - with_read: A boolean indicating whether to include read articles. Default is True.

        Returns:
        - A list of headlines.
        """
        headlines = []
        for i, article in enumerate(self.feeds_with_content):
            if not with_read and self.is_read(i):
                continue
            headlines.append(article.title.content)
        return headlines

    def get_description(self, index: int) -> str:
        """
        Retrieves the description of the article at the specified index.

        Parameters:
        - index: The index of the article.

        Returns:
        - The description of the article.
        """
        return self.feeds_with_content[index].description.content

    def get_article_url(self, index: int) -> str:
        """
        Retrieves the URL of the article at the specified index.

        Parameters:
        - index: The index of the article.

        Returns:
        - The URL of the article.
        """
        return self.feeds_with_content[index].link.content

    def mark_as_read(self, index: int) -> None:
        """
        Marks the article at the specified index as read.

        Parameters:
        - index: The index of the article.
        """
        title = self.feeds_with_content[index].title.content
        hashed_title = hashlib.sha256(title.encode('utf-8')).hexdigest()
        with open(self.READ_ARTICLES_FILE, "a+") as file:
            file.writelines(hashed_title + "\n")

    def is_read(self, index: int) -> bool:
        """
        Checks if the article at the specified index is marked as read.

        Parameters:
        - index: The index of the article.

        Returns:
        - True if the article is marked as read, False otherwise.
        """
        title = self.feeds_with_content[index].title.content
        hashed_title = hashlib.sha256(title.encode('utf-8')).hexdigest()

        if not os.path.exists(self.READ_ARTICLES_FILE):
            with open(self.READ_ARTICLES_FILE, 'w+'):
                pass

        with open(self.READ_ARTICLES_FILE, "r") as file:
            lines = file.readlines()
            read_articles = [line.strip() for line in lines]
            return hashed_title in read_articles
