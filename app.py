import os
from flask import Flask, render_template, redirect, request, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

app = Flask(__name__)
app.config["MONGO_DBNAME"] = 'recipe_buddy'
app.config["MONGO_URI"] = 'mongodb://recipeapp:Changethis$3d@ds261570.mlab.com:61570/recipe_buddy'

mongo = PyMongo(app)

@app.route('/new_category')
def new_category():
    return render_template('add_category.html')

@app.route('/insert_category', methods=['POST'])
def insert_category():
    categories = mongo.db.categories
    category_doc = {'category_name': request.form['category_name']}
    categories.insert_one(category_doc)
    return redirect(url_for('new_category'))


if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
        debug=True)
