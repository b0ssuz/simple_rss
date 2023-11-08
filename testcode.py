from rss import RSS
from pprint import pprint

r = RSS()

for i in r.get_headlines():
    print(i)