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

from requests import get
import hashlib
import os
from rss_parser import Parser

class RSS:
    READ_ARTICLES_FILE = "read_articles.lst"

    def __init__(self) -> None:
        with open('feeds.lst', 'r') as file:
            lines = file.readlines()

        self.feeds = [line.strip() for line in lines]
        self.feeds_with_content = []

        for feed in self.feeds:
            response = get(feed)
            rss = Parser.parse(response.text)
            for item in rss.channel.items:
                self.feeds_with_content.append(item)

    def get_headlines(self, with_read: bool = True) -> list:
        headlines = []
        for i, article in enumerate(self.feeds_with_content):
            if not with_read and self.is_read(i):
                continue
            headlines.append(article.title.content)
        return headlines

    def get_description(self, index: int) -> str:
        return self.feeds_with_content[index].description.content

    def get_article_url(self, index: int) -> str:
        return self.feeds_with_content[index].link.content

    def mark_as_read(self, index: int) -> None:
        title = self.feeds_with_content[index].title.content
        hashed_title = hashlib.sha256(title.encode('utf-8')).hexdigest()
        with open(self.READ_ARTICLES_FILE, "a+") as file:
            file.writelines(hashed_title + "\n")

    def is_read(self, index: int) -> bool:
        title = self.feeds_with_content[index].title.content
        hashed_title = hashlib.sha256(title.encode('utf-8')).hexdigest()

        if not os.path.exists(self.READ_ARTICLES_FILE):
            with open(self.READ_ARTICLES_FILE, 'w+'):
                pass

        with open(self.READ_ARTICLES_FILE, "r") as file:
            lines = file.readlines()
            read_articles = [line.strip() for line in lines]
            return hashed_title in read_articles
