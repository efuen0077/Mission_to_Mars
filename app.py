#use Flask and Mongo to begin creating
#Robin's web app

#import dependencies
from flask import Flask, render_template
from flask_pymongo import PyMongo
import scraping

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

#Define our route
@app.route("/")
def index():
   mars = mongo.db.mars.find_one()
   return render_template("index.html", mars=mars)

#add next route and function to our code
#this is the button of the web application
#the "scraping" button
@app.route("/scrape")
def scrape():
   mars = mongo.db.mars
   mars_data = scraping.scrape_all()
   mars.update({}, mars_data, upsert=True)
   return "Scraping Successful!"

#tell Flask to run
if __name__ == "__main__":
   app.run()
