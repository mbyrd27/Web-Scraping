from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)

# Make MongoDB Connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")

# Create the root/index view. This should only render 
# the title and scrape button until the Mongo database has 
# been populated with the scraped web data. 
@app.route("/")
def index():
    data = mongo.db.data.find_one()
    return render_template("index.html", data=data)
    

# Create the scraping view. This will redirect the user back
# to the landing page. The Mongo database will have been populated
# and the data feeding the content of the landing page should render.
@app.route("/scrape")
def get_data():
    data = mongo.db.data
    to_app = scrape_mars.scrape()
    data.update({}, to_app, upsert=True)
    return redirect("/", code=302)

if __name__ == "__main__":
    app.run(debug=True)