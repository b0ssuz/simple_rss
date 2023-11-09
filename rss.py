from rss_parser import Parser
from requests import *
import hashlib
from json import dumps


class RSS():
    def __init__(self)->None:
        with open('feeds.lst', 'r') as f:
            lines = f.readlines()

        self.feeds = [lines.strip() for lines in lines]

        self.feeds_with_content = []

        for feed in self.feeds:
            response = get(feed)
            rss = Parser.parse(response.text)
            for item in rss.channel.items:
                self.feeds_with_content.append(item)

    def get_headlines(self, with_read:bool=True)->list:
        headlines = []
        for i,article in enumerate(self.feeds_with_content):
            if with_read == False and self.is_read(i):
                continue
            headlines.append(article.title.content)
        return headlines

    def get_description(self, index: int)->str:
        return self.feeds_with_content[index].description.content

    def get_article_url(self, index: int)->str:
        return self.feeds_with_content[index].link.content

    def mark_as_read(self, index: int)->None:
        title = self.feeds_with_content[index].title.content
        hash_object = hashlib.sha256()
        hash_object.update(title.encode('utf-8'))
        hashed_title = hash_object.hexdigest()
        with open("read_articles.lst","a+") as f:
            f.writelines(hashed_title+"\n")

    def is_read(self, index: int)->bool:
        title = self.feeds_with_content[index].title.content
        hash_object = hashlib.sha256()
        hash_object.update(title.encode('utf-8'))
        hashed_title = hash_object.hexdigest()
        with open("read_articles.lst","r") as f:
            lines = f.readlines()
            read_articles = [lines.strip() for lines in lines]
            if hashed_title in read_articles:
                return True
            else:
                return False
