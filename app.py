from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import Mission_To_Mars
from pprint import pprint

app = Flask(__name__)

# Use PyMongo to establish Mongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_database")

@app.route("/")
def home():

    # Set cursor to db, pprint it
    cursor = mongo.db.collection.find_one({})
    for document in cursor:
        pprint(document)

    return render_template("index.html", data=cursor)

@app.route("/scrape")
def scrape():

    # Run the scrape function
    mars_data = Mission_To_Mars.scrape_info()

    # Update the Mongo database using update and upsert=True
    mongo.db.collection.update({}, mars_data, upsert=True)

    # Redirect back to home page
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)