import os
import config
from flask import Flask, render_template, redirect, request, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId


if os.getenv('FLASK_CONFIG') == "production":
    app = Flask(__name__)
    app.config.from_object('config.ProductionConfig')
    app.config.from_envvar('YOURAPPLICATION_SETTINGS')

elif os.getenv('FLASK_CONFIG') == "development":
    app = Flask(__name__)
    app.config.from_object('config.DevelopmentConfig')
    app.config.from_envvar('YOURAPPLICATION_SETTINGS')

elif os.getenv('FLASK_CONFIG') == "testing":
    app = Flask(__name__)
    app.config.from_object('config.TestingConfig')
    app.config.from_envvar('YOURAPPLICATION_SETTINGS')


mongo = PyMongo(app)

# TODO: insert, update and delete category update a constant dict of id : category name

def insert_ingredients(inserted_recipe_id, recipe_dict):

    ingredients_filtered = {k: v for (k, v) in recipe_dict
                                                if 'ingredient' in k}

    ingredients_doc = {'recipe_id': inserted_recipe_id,
                        'ingredients': list(ingredients_filtered.values())}

    ingredients = mongo.db.ingredients
    ingredients.insert_one(ingredients_doc)


def insert_instructions(inserted_recipe_id, recipe_dict):

    instructions_filtered = {k: v for (k, v) in recipe_dict
                                                if 'instruction' in k}

    instructions_doc = {'recipe_id': inserted_recipe_id,
                        'instructions': list(instructions_filtered.values())}

    instructions = mongo.db.instructions
    instructions.insert_one(instructions_doc)


@app.route('/new_category')
def new_category():
    return render_template('add_category.html')


@app.route('/insert_category', methods=['POST'])
def insert_category():
    categories = mongo.db.categories
    category_doc = {'category_name': request.form['category_name']}
    categories.insert_one(category_doc)
    return redirect(url_for('get_categories'))


@app.route('/get_categories')
def get_categories():
    return render_template('categories.html',
                        categories=mongo.db.categories.find())


@app.route('/edit_category/<category_id>')
def edit_category(category_id):
    return render_template('edit_category.html',
        category=mongo.db.categories.find_one({'_id': ObjectId(category_id)}))


@app.route('/category_item/<category_id>', methods=["POST"])
def update_category(category_id):
    category_items = mongo.db.categories
    category_items.update({'_id': ObjectId(category_id)},
                            {'category_name': request.form['category_name']})
    return redirect(url_for('get_categories'))


@app.route('/delete_category/<category_id>')
def delete_category(category_id):
    mongo.db.categories.remove({'_id': ObjectId(category_id)})
    return redirect(url_for("get_categories"))

# TODO: copy category to time to cook, 30 min slots

@app.route('/add_recipe')
def add_recipe():
    return render_template('add_recipe.html',
                        categories=mongo.db.categories.find())


@app.route('/get_recipies')
def get_recipes():
    return render_template('get_recipies.html',
                            recipies=mongo.db.recipes.find())


@app.route('/insert_recipe', methods=['POST'])
def insert_recipe():

    # recipe record
    recipes = mongo.db.recipes
    recipe_doc = {'recipe_name': request.form.to_dict()['recipe_name'],
            'recipe_description': request.form.to_dict()['recipe_description']}

    _recipe_id = recipes.insert_one(recipe_doc)

    # ingredients record insertion
    insert_ingredients(_recipe_id.inserted_id, request.form.to_dict().items())

    # instructions record insertion
    insert_instructions(_recipe_id.inserted_id, request.form.to_dict().items())

    return redirect(url_for('get_recipes'))


if __name__ == '__main__':
    app.run(host=os.environ.get('IP'), debug=True)
