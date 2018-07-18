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

def get_category_id(category_name):

    category_record = mongo.db.categories.find_one({'category_name': category_name})

    return category_record['_id']

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

# TODO:change new route to add

@app.route('/insert_category', methods=['POST'])
def insert_category():
    categories = mongo.db.categories
    category_doc = {'category_name': request.form['category_name']}
    categories.insert_one(category_doc)
    return redirect(url_for('get_categories'))


@app.route('/get_categories')
def get_categories():
    return render_template('get_categories.html',
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

# TODO: category will become time to cook 'quick get home late' 'Sunday Lunch for 2', 'Sunday Lunch for all the Family' and then create a copy category as 'cuisine'

@app.route('/add_recipe')
def add_recipe():
    return render_template('add_recipe.html',
                        categories=mongo.db.categories.find())


@app.route('/get_recipes')
def get_recipes():
    return render_template('get_recipes.html',
                            recipes=mongo.db.recipes.find())


@app.route('/insert_recipe', methods=['POST'])
def insert_recipe():

    # recipe record
    recipes = mongo.db.recipes

    category_id = get_category_id(request.form.to_dict()['category_name'])

    # TODO: request.form.to_dict()['cusine']

    recipe_doc = {'recipe_name': request.form.to_dict()['recipe_name'],
            'recipe_description': request.form.to_dict()['recipe_description'],
            'category_id': category_id,
            'cuisine_id': '9999999'}

    _recipe_id = recipes.insert_one(recipe_doc)

    # ingredients record insertion
    insert_ingredients(_recipe_id.inserted_id, request.form.to_dict().items())

    # instructions record insertion
    insert_instructions(_recipe_id.inserted_id, request.form.to_dict().items())

    return redirect(url_for('get_recipes'))


@app.route('/show_recipe/<recipe_id>')
def show_recipe(recipe_id):
    recipe_record=mongo.db.recipes.find_one({'_id': ObjectId(recipe_id)})
    print(recipe_record)
    ingredients=mongo.db.ingredients.find_one({'recipe_id': ObjectId(recipe_id)})
    instructions=mongo.db.instructions.find_one({'recipe_id': ObjectId(recipe_id)})
    return render_template('show_recipe.html',
        recipes=mongo.db.recipes.find_one({'_id': ObjectId(recipe_id)}),
        category=mongo.db.categories.find_one({'_id': recipe_record['category_id']}),
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
        selected_category=mongo.db.categories.find_one({'_id': recipe_record['category_id']}),
        instructions=instructions['instructions'],
        ingredients=ingredients['ingredients'])


@app.route('/recipe_item/<recipe_id>', methods=["POST"])
def update_recipe(recipe_id):
    recipe_item = mongo.db.recipes
    # TODO: category_item = mongo.db.categories
    instruction_items = mongo.db.instructions
    ingredient_items = mongo.db.ingredients
    recipe_item.update({'_id': ObjectId(recipe_id)},
                        {'recipe_name': request.form['recipe_name']},
                        {'recipe_description': request.form['recipe_description']})
    instruction_items.update({'recipe_id': ObjectId(recipe_id)},
                        {'instructions': request.form['instructions']})
    ingredient_items.update({'recipe_id': ObjectId(recipe_id)},
                        {'ingredients': request.form['ingredients']})
    return redirect(url_for('get_recipes'))


if __name__ == '__main__':
    app.run(host=os.environ.get('IP'), debug=True)
