from flask import Flask, render_template
from rss import RSS

app = Flask(__name__, template_folder='templates')

class FlaskApp:
    def __init__(self):
        self.my_feed = RSS()
        self.list_read_articles = False

    def run(self):
        app.run(debug=True)

@app.route('/')
def index():
    """
    Renders the index page of the Flask web interface.
    """
    return render_template('index.html', items=flask_app.my_feed.feeds_with_content)

if __name__ == "__main__":
    flask_app = FlaskApp()
    flask_app.run()
