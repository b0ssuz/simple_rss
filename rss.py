from constants import *
from rss_parser import Parser
from requests import *
from bs4 import BeautifulSoup


class RSS():
    def __init__(self)->None:
        with open('feeds.lst', 'r') as datei:
            lines = datei.readlines()

        feeds = [lines.strip() for lines in lines]

        self.feeds_with_content = []

        for feed in feeds:
            response = get(feed)
            rss = Parser.parse(response.text)
            for item in rss.channel.items:
                self.feeds_with_content.append(item)

    def list_headlines(self)->None:
        index = 0
        for article in self.feeds_with_content:
            print(f"{index} - {article.title.content}")
            index += 1

    def read_article_description(self, index: int)->None:
        print(f"\n--- {index} \n{self.feeds_with_content[index].title.content} \n")
        print(f"{self.feeds_with_content[index].description.content} \n")

    def get_article_url(self, index: int)->str:
        return self.feeds_with_content[index].link.content

    def read_full_content_as_html(self, index: int)->str:
        response = get(self.feeds_with_content[index].link.content)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            return(soup.prettify())
        else:
            return('Error with statuscode:', response.status_code)
