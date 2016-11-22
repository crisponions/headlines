from flask import render_template
import feedparser
from flask import request
from flask import Flask
import json
import urllib2
import urllib

app = Flask(__name__)

RSS_FEEDS = {'bbc': 'http://feeds.bbci.co.uk/news/rss.xml',
             'cnn': 'http://rss.cnn.com/rss/edition.rss',
             'fox': 'http://feeds.foxnews.com/foxnews/latest',
            } 

@app.route('/')
def get_news():
    query = request.args.get('publication')
    if not query or query.lower() not in RSS_FEEDS:
        publication = 'bbc'
    else:
        publication = query.lower()

    feed = feedparser.parse(RSS_FEEDS[publication])
    weather = get_weather("London,UK")
    return render_template("home.html", articles=feed['entries'],weather=weather)

def get_weather(query):
    api_url = 'http://api.openweathermap.org/data/2.5/weather?q={}&appid=889b61e24fccd317a493e8929428ee57'
    query = urllib.quote(query)
    url = api_url.format(query)
    data = urllib2.urlopen(url).read()
    parsed = json.loads(data)
    weather = None
    if parsed.get("weather"):
        weather = {"description":parsed["weather"][0]["description"],
                   "temperature":parsed["main"]["temp"],
                   "city":parsed["name"]}

    return weather

if __name__ == "__main__":
    app.run('0.0.0.0', port=5000, debug=True)

