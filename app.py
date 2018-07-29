import os
import sys
import enum
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

class COLLECTION_NAMES(enum.Enum):
    CATEGORIES = 'categories'
    CUISINES = 'cuisines'
    INSTRUCTIONS = 'instructions'
    INGREDIENTS = 'ingredients'

class FILTER_KEYS(enum.Enum):
    INGREDIENT = 'ingredient'
    INSTRUCTION = 'instruction'

class ID_NAME(enum.Enum):
    RECIPE_ID = 'recipe_id'


def get_collection_id(collection_name, search_field, search_value):

    field_name = urllib.parse.quote_plus(search_field)

    collection_record = mongo.db[collection_name].find_one({field_name : search_value})

    return collection_record['_id']


def insert_record(id_name, insert_record_id, record_set_dict, filter_key, collection_name):
    '''Insert an Instruction or Ingredient record using using foreign key id'''

    if (filter_key == FILTER_KEYS.INGREDIENT.value
        or filter_key == FILTER_KEYS.INSTRUCTION.value):

        key_name = urllib.parse.quote_plus(filter_key)

    else:

        sys.stderr.write('filter key ingredient/instruction :: error %s' % (filter_key))

    if (collection_name == COLLECTION_NAMES.INSTRUCTIONS.value
        or collection_name == COLLECTION_NAMES.INGREDIENTS.value):

        sub_record_name = urllib.parse.quote_plus(collection_name)

    else:

        sys.stderr.write('collection name categories/cuisines/instructions/ingredients not found :: error %s' % (collection_name))

    if ( id_name == ID_NAME.RECIPE_ID.value):

        primary_record_id = urllib.parse.quote_plus(id_name)

    else:

        sys.stderr.write('id name recipe_id not found :: error %s' % (id_name))

    filtered_dict = {k: v for (k, v) in record_set_dict
                                                if key_name in k}

    record_doc = {primary_record_id: insert_record_id,
                    sub_record_name: list(filtered_dict.values())}

    mongo.db[collection_name].insert_one(record_doc)


def update_record(id_name, update_record_id, record_set_dict, filter_key, collection_name):
    '''Update an Instruction or Ingredient record using using foreign key id'''

    if (filter_key == FILTER_KEYS.INGREDIENT.value
        or filter_key == FILTER_KEYS.INSTRUCTION.value):

        key_name = urllib.parse.quote_plus(filter_key)

    else:

        sys.stderr.write('filter key ingredient/instruction :: error %s' % (filter_key))

    if (collection_name == COLLECTION_NAMES.INSTRUCTIONS.value
        or collection_name == COLLECTION_NAMES.INGREDIENTS.value):

        sub_record_name = urllib.parse.quote_plus(collection_name)

    else:

        sys.stderr.write('collection name categories/cuisines/instructions/ingredients not found :: error %s' % (collection_name))

    if ( id_name == ID_NAME.RECIPE_ID.value):

        primary_record_id = urllib.parse.quote_plus(id_name)

    else:

        sys.stderr.write('id name recipe_id not found :: error %s' % (id_name))

    filtered_dict = {k: v for (k, v) in record_set_dict
                                                if key_name in k}

    record_doc = {primary_record_id: ObjectId(update_record_id),
                        sub_record_name: list(filtered_dict.values())}

    record_tobe_updated = mongo.db[collection_name].find_one({'recipe_id': ObjectId(update_record_id)})

    mongo.db[collection_name].update({'_id': ObjectId(record_tobe_updated['_id'])}, record_doc)

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
    insert_record(id_name='recipe_id', insert_record_id=_recipe_id.inserted_id, record_set_dict=request.form.to_dict().items(), filter_key='ingredient', collection_name='ingredients')

    # instructions record insertion
    insert_record(id_name='recipe_id', insert_record_id=_recipe_id.inserted_id, record_set_dict=request.form.to_dict().items(), filter_key='instruction', collection_name='instructions')

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
    update_record(id_name='recipe_id', update_record_id=recipe_id,
                record_set_dict=request.form.to_dict().items(), filter_key='ingredient',collection_name='ingredients')

    # instructions record update
    update_record(id_name='recipe_id', update_record_id=recipe_id,
                record_set_dict=request.form.to_dict().items(), filter_key='instruction',collection_name='instructions')

    return redirect(url_for('get_recipes'))


@app.route('/delete_recipe/<recipe_id>')
def delete_recipe(recipe_id):
    recipe_record=mongo.db.recipes.remove({'_id': ObjectId(recipe_id)})
    ingredients=mongo.db.ingredients.remove({'recipe_id': ObjectId(recipe_id)})
    instructions=mongo.db.instructions.remove({'recipe_id': ObjectId(recipe_id)})
    return redirect(url_for('get_recipes'))

if __name__ == '__main__':
    app.run(host=os.environ.get('IP'), debug=True)


# TODO: Add users https://realpython.com/using-flask-login-for-user-management-with-flask/
# TODO: pagination https://stackoverflow.com/questions/33556572/paginate-a-list-of-items-in-python-flask
# TODO: user votes
# TODO: you can use a Python library such as matplotlib, or a JS library such as d3/dc (that you learned about if you took the frontend modules) for visualisation
