from rss import RSS
import webbrowser
import subprocess
import signal
import sys

def goodbye_message():
    print("\n \n Goodbye! \n\n")
    # Add any other cleanup tasks here
    sys.exit(0)

# Register the goodbye_message function to be called on Ctrl+C
signal.signal(signal.SIGINT, lambda signal, frame: goodbye_message())

my_feed = RSS()

try:
        while True:
            my_feed.list_headlines()
            user_input_index = int(input("choose article: "))
            my_feed.read_article_description(user_input_index)
            user_input_read = input("read full article (y/n): ")
            if user_input_read == "y":
                    my_feed.mark_as_read(user_input_index)
                    subprocess.call(["w3m",my_feed.get_article_url(user_input_index)])
            else:
                continue
except KeyboardInterrupt:
        goodbye_message()
