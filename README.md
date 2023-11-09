# simple rss 

## Introduction
This program is a simple command-line RSS reader written in Python. It allows you to view and interact with RSS feeds from various sources. The program supports marking articles as read and provides a user-friendly interface for navigating through headlines.

## Dependencies
- Python 3.x
  
install dependencies with `pip install -r requirements.txt`

## Usage
1. Clone the repository and navigate to the project directory.
2. Run the program using the following command:
   ```bash
   python main.py
   ```

## Configuration
Before running the program, make sure to create a `feeds.lst` file containing the URLs of the RSS feeds you want to subscribe to. Each URL should be on a separate line.

Example `feeds.lst`:
```
https://www.heise.de/rss/heise-Rubrik-IT.rdf
https://www.heise.de/rss/heise-Rubrik-Netzpolitik.rdf
https://www.tagesschau.de/wissen/technologie/index~rss2.xml
https://feeds.feedburner.com/TheHackersNews
```

## Navigation
- Use the arrow keys (`j` and `k` or Up and Down arrow keys) to navigate through headlines.
- Press `Enter` to view the selected article's description and URL.
- Press `q` or `Esc` to exit the program.

## License
This program is licensed under the [GNU General Public License](https://www.gnu.org/licenses/gpl-3.0.html), version 3.0. See the provided `LICENSE` file for details.

## Author
- Bünyamin Sarikaya

Feel free to contribute and customize the program according to your needs!
