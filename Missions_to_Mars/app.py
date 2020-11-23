# import dependencies
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

# create flask app and mongodb
app = Flask(__name__)

app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_data"
mongo = PyMongo(app)

# create home route


@app.route('/')
def home():

    mars_collection = mongo.db.collection.find_one()

    return render_template('index.html', mars=mars_collection)

# create route to link to scrape script


@app.route("/scrape")
def scraper():
    mars_info = scrape_mars.scrape()

    mongo.db.collection.update({}, mars_info, upsert=True)

    return redirect('/')


if __name__ == "__main__":
    app.run(debug=True)
