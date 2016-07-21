import feedparser
from flask import Flask, render_template
from flask import request

app = Flask(__name__)

RSS_FEEDS = {'bbc': 'http://feeds.bbci.co.uk/news/rss.xml',
			 'cnn': 'http://rss.cnn.com/rss/edition.rss',
			 'fox': 'http://feeds.foxnews.com/foxnews/latest',
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
			 'the_est': 'http://www.theestablishment.co/feed/'}

@app.route('/')
def get_news():
	query = request.args.get('publication')
	if not query or query.lower() not in RSS_FEEDS:
		publication = 'bbc'
	else:
		publication = query.lower()
	feed = feedparser.parse(RSS_FEEDS[publication])
	return render_template('home.html', articles=feed['entries'])

if __name__ == '__main__':
	app.run(debug=True, port = 7001)