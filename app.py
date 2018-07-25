import os
import config
from flask import Flask, render_template, redirect, request, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
import urllib.parse


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

def get_collection_id(collection_name, search_field, search_value):

    field_name = urllib.parse.quote_plus(search_field)

    collection_record = mongo.db[collection_name].find_one({field_name : search_value})

    return collection_record['_id']

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

def update_ingredients(update_recipe_id, recipe_dict):

    ingredients_filtered = {k: v for (k, v) in recipe_dict
                                                if 'ingredient' in k}

    ingredients_doc = {'recipe_id': ObjectId(update_recipe_id),
                        'ingredients': list(ingredients_filtered.values())}

    ingredients = mongo.db.ingredients

    ingredients_record = ingredients.find_one({'recipe_id': ObjectId(update_recipe_id)})

    ingredients.update({'_id': ObjectId(ingredients_record['_id'])}, ingredients_doc)

def update_instructions(update_recipe_id, recipe_dict):

    instructions_filtered = {k: v for (k, v) in recipe_dict
                                                if 'instruction' in k}

    instructions_doc = {'recipe_id': ObjectId(update_recipe_id),
                        'instructions': list(instructions_filtered.values())}

    instructions = mongo.db.instructions

    instructions_record = instructions.find_one({'recipe_id': ObjectId(update_recipe_id)})

    instructions.update({'_id': ObjectId(instructions_record['_id'])}, instructions_doc)


@app.route('/add_category')
def add_category():
    return render_template('add_category.html')


@app.route('/add_cuisine')
def add_cuisine():
    return render_template('add_cuisine.html')


@app.route('/insert_category', methods=['POST'])
def insert_category():
    categories = mongo.db.categories
    category_doc = {'category_name': request.form['category_name']}
    categories.insert_one(category_doc)
    return redirect(url_for('get_categories'))


@app.route('/insert_cuisine', methods=['POST'])
def insert_cuisine():
    cuisines = mongo.db.cuisines
    cuisine_doc = {'cuisine_name': request.form['cuisine_name']}
    cuisines.insert_one(cuisine_doc)
    return redirect(url_for('get_cuisines'))


@app.route('/get_categories')
def get_categories():
    return render_template('get_categories.html',
                        categories=mongo.db.categories.find())


@app.route('/get_cuisines')
def get_cuisines():
    return render_template('get_cuisines.html',
                        cuisines=mongo.db.cuisines.find())


@app.route('/edit_category/<category_id>')
def edit_category(category_id):
    return render_template('edit_category.html',
        category=mongo.db.categories.find_one({'_id': ObjectId(category_id)}))


@app.route('/edit_cuisine/<cuisine_id>')
def edit_cuisine(cuisine_id):
    return render_template('edit_cuisine.html',
        cuisine=mongo.db.cuisines.find_one({'_id': ObjectId(cuisine_id)}))


@app.route('/category_item/<category_id>', methods=["POST"])
def update_category(category_id):
    category_items = mongo.db.categories
    category_items.update({'_id': ObjectId(category_id)},
                            {'category_name': request.form['category_name']})
    return redirect(url_for('get_categories'))


@app.route('/cuisine_item/<cuisine_id>', methods=["POST"])
def update_cuisine(cuisine_id):
    cuisine_items = mongo.db.cuisines
    cuisine_items.update({'_id': ObjectId(cuisine_id)},
                            {'cuisine_name': request.form['cuisine_name']})
    return redirect(url_for('get_cuisines'))


@app.route('/delete_category/<category_id>')
def delete_category(category_id):
    mongo.db.categories.remove({'_id': ObjectId(category_id)})
    return redirect(url_for("get_categories"))


@app.route('/delete_cuisine/<cuisine_id>')
def delete_cuisine(cuisine_id):
    mongo.db.cuisines.remove({'_id': ObjectId(cuisine_id)})
    return redirect(url_for("get_cuisines"))


@app.route('/add_recipe')
def add_recipe():
    return render_template('add_recipe.html',
                        categories=mongo.db.categories.find(),
                        cuisines=mongo.db.cuisines.find())


@app.route('/get_recipes')
def get_recipes():
    return render_template('get_recipes.html',
                            recipes=mongo.db.recipes.find())


@app.route('/insert_recipe', methods=['POST'])
def insert_recipe():

    # recipe collection
    recipes = mongo.db.recipes

    category_id = get_collection_id('categories', 'category_name', request.form.to_dict()['category_name'])

    cuisine_id = get_collection_id('cuisines','cuisine_name', request.form.to_dict()['cuisine_name'])

    recipe_doc = {'recipe_name': request.form.to_dict()['recipe_name'],
            'recipe_description': request.form.to_dict()['recipe_description'],
            'category_id': category_id,
            'cuisine_id': cuisine_id,
            'total_time': request.form.to_dict()['total_time']}

    # recipes record insertion
    _recipe_id = recipes.insert_one(recipe_doc)

    # ingredients record insertion
    insert_ingredients(_recipe_id.inserted_id, request.form.to_dict().items())

    # instructions record insertion
    insert_instructions(_recipe_id.inserted_id, request.form.to_dict().items())

    return redirect(url_for('get_recipes'))


@app.route('/show_recipe/<recipe_id>')
def show_recipe(recipe_id):
    recipe_record=mongo.db.recipes.find_one({'_id': ObjectId(recipe_id)})
    ingredients=mongo.db.ingredients.find_one({'recipe_id': ObjectId(recipe_id)})
    instructions=mongo.db.instructions.find_one({'recipe_id': ObjectId(recipe_id)})
    return render_template('show_recipe.html',
        recipes=mongo.db.recipes.find_one({'_id': ObjectId(recipe_id)}),
        categories=mongo.db.categories.find_one({'_id': recipe_record['category_id']}),
        cuisines=mongo.db.cuisines.find_one({'_id': recipe_record['cuisine_id']}),
        instructions=instructions['instructions'],
        ingredients=ingredients['ingredients'])


@app.route('/edit_recipe/<recipe_id>')
def edit_recipe(recipe_id):
    recipe_record=mongo.db.recipes.find_one({'_id': ObjectId(recipe_id)})
    ingredients=mongo.db.ingredients.find_one({'recipe_id': ObjectId(recipe_id)})
    instructions=mongo.db.instructions.find_one({'recipe_id': ObjectId(recipe_id)})
    return render_template('edit_recipe.html',
        recipes=mongo.db.recipes.find_one({'_id': ObjectId(recipe_id)}),
        categories=mongo.db.categories.find(),
        cuisines=mongo.db.cuisines.find(),
        selected_category=mongo.db.categories.find_one({'_id': recipe_record['category_id']}),
        selected_cuisine=mongo.db.cuisines.find_one({'_id': recipe_record['cuisine_id']}),
        instructions=instructions['instructions'],
        ingredients=ingredients['ingredients'])


@app.route('/update_recipe/<recipe_id>', methods=["POST"])
def update_recipe(recipe_id):

    recipes = mongo.db.recipes

    category_id = get_collection_id('categories', 'category_name', request.form.to_dict()['category_name'])

    cuisine_id = get_collection_id('cuisines','cuisine_name', request.form.to_dict()['cuisine_name'])

    recipe_doc = {'recipe_name': request.form.to_dict()['recipe_name'],
            'recipe_description': request.form.to_dict()['recipe_description'],
            'category_id': category_id,
            'cuisine_id': cuisine_id,
            'total_time': request.form.to_dict()['total_time']}

    # recipes record update
    recipes.update({'_id': ObjectId(recipe_id)},recipe_doc)

    # ingredients record update
    ing_result = update_ingredients(recipe_id, request.form.to_dict().items())

    # instructions record update
    update_instructions(recipe_id, request.form.to_dict().items())

    return redirect(url_for('get_recipes'))


if __name__ == '__main__':
    app.run(host=os.environ.get('IP'), debug=True)
