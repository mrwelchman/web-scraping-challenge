from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)

# set up mongo connection
app.config['MONGO_URI'] = 'mongodb://localhost:27017/mars'
mongo = PyMongo(app)

@app.route('/')
def index():
	mars_feed = mongo.db.mars_feed.find_one()
	return render_template('index.html', mars_feed=mars_feed)

@app.route('/scrape')
def scraper():
	mars_feed = mongo.db.mars_feed
	mars_data = scrape_mars.scrape()
	mars_feed.update({}, mars_data, upsert=True)
	return redirect('/', code=302)

if __name__ == '__main__':
	app.run(debug=True)