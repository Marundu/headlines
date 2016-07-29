import feedparser
from flask import Flask, render_template, request
import json
import urllib
import urllib2

app = Flask(__name__)

RSS_FEEDS = {'bbc': 'http://feeds.bbci.co.uk/news/rss.xml',
			 'cnn': 'http://rss.cnn.com/rss/edition.rss',
			 'iol': 'http://www.iol.co.za/cmlink/1.640',
			 'aj': 'http://www.aljazeera.com/?feed=rss2',
			 'mg': 'http://mg.co.za/rss/',
			 'mash': 'http://feeds.mashable.com/Mashable',
			 'guard': 'https://www.theguardian.com/world/rss',
			 'granta': 'http://granta.com/feed/',
			 'fdn': 'http://feeds.feedburner.com/FeministDailyNews',
			 'ars_index': 'http://feeds.arstechnica.com/arstechnica/index/',
			 'ars_oss': 'http://feeds.arstechnica.com/arstechnica/open-source/',
			 'ars_biz': 'http://feeds.arstechnica.com/arstechnica/business/',
			 'aeon': 'https://aeon.co/feed',
			 'the_est': 'http://www.theestablishment.co/feed/',
			 'sethgodin': 'http://feeds.feedblitz.com/sethsblog&x=1'}

WEATHER_URL = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=62b8bd5ad99b7f38bc9be259871bf155'
CURRENCY_URL = 'https://openexchangerates.org/api/latest.json?app_id=6a99b61a553c437daf7f4795c973aec9'

DEFAULTS = {'publication': 'bbc',
			'city': 'Nairobi, KE',
			'currency_from': 'USD',
			'currency_to': 'KES'}


@app.route('/')
def home():

	# Get customized headlines based on user input
	publication = request.args.get('publication')
	if not publication:
		publication = DEFAULTS['publication']
	articles = get_news(publication)

	# Get customized weather based on user input
	city = request.args.get('city')
	if not city:
		city = DEFAULTS['city']
	weather = get_weather(city)

	# Get customized currency data based on user input or default
	currency_from = request.args.get('currency_from')
	if not currency_from:
		currency_from = DEFAULTS['currency_from']
	currency_to = request.args.get('currency_to')
	if not currency_to:
		currency_to = DEFAULTS['currency_to']
	rate, currencies = get_rate(currency_from, currency_to)

	return render_template('home.html', articles=articles, weather=weather,
							currency_from=currency_from, currency_to=currency_to,
							rate=rate, currencies=sorted(currencies))

def get_rate(frm, to):
	allcurrency = urllib2.urlopen(CURRENCY_URL).read()
	parsed = json.loads(allcurrency).get('rates')
	frm_rate = parsed.get(frm.upper())
	to_rate = parsed.get(to.upper())
	return (to_rate / frm_rate, parsed.keys())

def get_news(query):
	if not query or query.lower() not in RSS_FEEDS:
		publication = DEFAULTS['publication']
	else:
		publication = query.lower()
	feed = feedparser.parse(RSS_FEEDS[publication])
	return feed['entries']

def get_weather(query):
	query = urllib.quote(query)
	url = WEATHER_URL.format(query)
	data = urllib2.urlopen(url).read()
	parsed = json.loads(data)
	weather = None
	if parsed.get('weather'):
		weather = {'description': parsed['weather'][0]['description'],
					'temperature': parsed['main']['temp'],
					'city': parsed['name'],
					'country': parsed['sys']['country']}
	return weather


if __name__ == '__main__':
	app.run(debug=True, port=7001)