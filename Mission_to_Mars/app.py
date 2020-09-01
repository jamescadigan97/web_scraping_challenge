from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import mars_scrape

app = Flask(__name__)

mongo = PyMongo(app, uri="mongodb://localhost:27017/weather_app")

# Route to render index.html template using data from Mongo
@app.route("/")
def home():

    # Find one record of data from the mongo database
    data = mongo.db.mars.find_one()
    
    # Return template and data
    return render_template("index.html", mars_article=data["mars_article"], mars_paragraph = data["mars_paragraph"], mars_picture_title=data["mars_picture_title"], mars_picture=data["mars_picture"])


# Route that will trigger the scrape function
@app.route("/scrape")
def scrape():

    # Run the scrape function
    mars_data = mars_scrape.scrape()

    # Update the Mongo database using update and upsert=True
    mongo.db.mars.update({}, mars_data, upsert=True)

    # Redirect back to home page
    return redirect("/")

@app.route("/images")
def images():
    data = mongo.db.mars.find_one()
    base_url = "https://astrogeology.usgs.gov"
    return render_template("Mars_images.html", mars_image_title1=data["mars_image_titles"][0], mars_image_title2=data["mars_image_titles"][1], mars_image_title3=data["mars_image_titles"][2], mars_image_title4=data["mars_image_titles"][3], mars_image_links1=data["mars_image_links"][0], mars_image_links2=data["mars_image_links"][1], mars_image_links3=data["mars_image_links"][2], mars_image_links4=data["mars_image_links"][3])
if __name__ == "__main__":
    app.run(debug=True)
