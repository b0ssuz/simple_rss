# simple rss

## Introduction

This program is a simple command-line RSS reader written in Python. It allows you to view and interact with RSS feeds from various sources. The program supports marking articles as read and provides a user-friendly interface for navigating through headlines.

**New Feature: Web UI**

We've added a web interface to make the RSS reading experience even more convenient. Now you can access and manage your feeds through a browser.

## Dependencies

- Python 3.x
- Flask (for the web UI)

## Usage

1. Clone the repository and navigate to the project directory.
2. Run the command-line version of the program using the following command:
   ```bash
   python main.py
   ```
3. To use the web UI, run the Flask app using the command:
   ```bash
   python flask_app.py
   ```
   Open your browser and navigate to `http://localhost:5000` to access the web interface.

## Configuration

Before running the program, make sure to create a `feeds.lst` file containing the URLs of the RSS feeds you want to subscribe to. Each URL should be on a separate line.

Example `feeds.lst`:

```
https://www.heise.de/rss/heise-Rubrik-IT.rdf
```

## Navigation

- Use the arrow keys (`j` and `k` or Up and Down arrow keys) to navigate through headlines.
- Press `Enter` or `l` to view the selected article's description and URL.
  - Press `Enter` or `l` again to open the article in your browser or any other key to go back to your feeds.
- Press `q` or `Esc` to exit the command-line program.

For the web UI, navigate through the feeds and articles using the provided buttons on the webpage.

## License

This program is licensed under the [GNU General Public License](https://www.gnu.org/licenses/gpl-3.0.html), version 3.0. See the provided `LICENSE` file for details.

## Author

- Bünyamin Sarikaya

Feel free to contribute and customize the program according to your needs!
