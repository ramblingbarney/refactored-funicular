import os
import sys
import enum
import config
from flask import Flask, flash, render_template, redirect, request
from flask import url_for, session, abort, Response
from flask_login import LoginManager, UserMixin, login_required
from flask_login import login_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from forms import LoginForm, RegistrationForm
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from bson.son import SON
from bson.json_util import dumps
import random
import string
import urllib.parse
import urllib.request

if os.getenv('FLASK_CONFIG') == "production":
    app = Flask(__name__)
    app.config.from_object('config.ProductionConfig')
    app.config.from_envvar('YOURAPPLICATION_SETTINGS')

elif os.getenv('FLASK_CONFIG') == "development":
    app = Flask(__name__)
    app.config.from_object('config.DevelopmentConfig')
    app.config.from_envvar('YOURAPPLICATION_SETTINGS')


mongo = PyMongo(app)

# flask-login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


class User(UserMixin):
    '''
    User
    '''

    def __init__(self, id):
        self.id = id
        user_record = mongo.db.users.find_one({'_id': ObjectId(self.id)})

    def get_id(self):
        return self.id

    @staticmethod
    def validate_login(password_hash, password):
        return check_password_hash(password_hash, password)

    def __repr__(self):
        return "%s" % (self.id)


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


class SEARCH_TYPE(enum.Enum):
    CATEGORY_NAME = 'category_name.category_name'
    CUISINE_NAME = 'cuisine_name.cuisine_name'
    USER_VOTES = 'user_votes'


class SORT_COLUMN(enum.Enum):
    USER_VOTES = 'user_votes'
    TOTAL_TIME = 'total_time'


class SORT_ORDER(enum.Enum):
    USER_VOTES_ASCENDING = 'UserVotesAscending'
    USER_VOTES_DESCENDING = 'UserVotesDescending'
    TOTAL_TIME_ASCENDING = 'TotalTimeAscending'
    TOTAL_TIME_DESCENDING = 'TotalTimeDescending'


@app.before_request
def csrf_protect():
    if request.method == "POST":
        token = session.pop('_csrf_token', None)
        if not token or token != request.form.get('_csrf_token'):
            abort(403)


def generate_csrf_token():
    if '_csrf_token' not in session:
        session['_csrf_token'] = ''.join(
            [random.choice(
                string.ascii_letters + string.digits) for n in range(64)])
    return session['_csrf_token']


app.jinja_env.globals['csrf_token'] = generate_csrf_token


def get_collection_id(collection_name, search_field, search_value):
    '''
    Return collection id for a given collection name,
    field name containing search string
    '''

    field_name = urllib.parse.quote_plus(search_field)
    collection_record = mongo.db[collection_name].find_one(
        {field_name: search_value})
    return collection_record['_id']


def insert_record(
                id_name,
                insert_record_id,
                record_set_dict,
                filter_key,
                collection_name):
    '''
    Insert an Instruction or Ingredient record using using foreign key id
    '''

    if (filter_key == FILTER_KEYS.INGREDIENT.value):
        key_name = urllib.parse.quote_plus(FILTER_KEYS.INGREDIENT.value)
    elif (filter_key == FILTER_KEYS.INSTRUCTION.value):
        key_name = urllib.parse.quote_plus(FILTER_KEYS.INSTRUCTION.value)
    else:
        sys.stderr.write(
            'filter key ingredient/instruction :: error %s' % (filter_key))

    if (collection_name == COLLECTION_NAMES.INSTRUCTIONS.value):
        sub_record_name = urllib.parse.quote_plus(
            COLLECTION_NAMES.INSTRUCTIONS.value)
    elif (collection_name == COLLECTION_NAMES.INGREDIENTS.value):
        sub_record_name = urllib.parse.quote_plus(
            COLLECTION_NAMES.INGREDIENTS.value)
    else:
        sys.stderr.write(
            'collection name categories/cuisines/instructions/ingredients \
             not found :: error %s' % (collection_name))

    if (id_name == ID_NAME.RECIPE_ID.value):
        primary_record_id = urllib.parse.quote_plus(ID_NAME.RECIPE_ID.value)
    else:
        sys.stderr.write('id name recipe_id not found :: error %s' % (id_name))

    filtered_dict = {k: v for (k, v) in record_set_dict if key_name in k}
    record_doc = {
                    primary_record_id: insert_record_id,
                    sub_record_name: list(filtered_dict.values())}
    mongo.db[collection_name].insert_one(record_doc)


def update_record(
                id_name,
                update_record_id,
                record_set_dict,
                filter_key,
                collection_name):
    '''
    Update an Instruction or Ingredient record using using foreign key id
    '''

    if (filter_key == FILTER_KEYS.INGREDIENT.value):
        key_name = urllib.parse.quote_plus(FILTER_KEYS.INGREDIENT.value)
    elif (filter_key == FILTER_KEYS.INSTRUCTION.value):
        key_name = urllib.parse.quote_plus(FILTER_KEYS.INSTRUCTION.value)
    else:
        sys.stderr.write(
            'filter key ingredient/instruction :: error %s' % (filter_key))

    if (collection_name == COLLECTION_NAMES.INSTRUCTIONS.value):
        sub_record_name = urllib.parse.quote_plus(
                                        COLLECTION_NAMES.INSTRUCTIONS.value)
    elif (collection_name == COLLECTION_NAMES.INGREDIENTS.value):
        sub_record_name = urllib.parse.quote_plus(
                                            COLLECTION_NAMES.INGREDIENTS.value)
    else:
        sys.stderr.write(
            'collection name categories/cuisines/instructions/ingredients \
            not found :: error %s' % (collection_name))

    if (id_name == ID_NAME.RECIPE_ID.value):
        primary_record_id = urllib.parse.quote_plus(ID_NAME.RECIPE_ID.value)
    else:
        sys.stderr.write('id name recipe_id not found :: error %s' % (id_name))

    filtered_dict = {k: v for (k, v) in record_set_dict if key_name in k}
    record_doc = {
                primary_record_id: ObjectId(update_record_id),
                sub_record_name: list(filtered_dict.values())}
    record_tobe_updated = mongo.db[collection_name].find_one(
        {'recipe_id': ObjectId(update_record_id)})
    mongo.db[collection_name].update(
        {'_id': ObjectId(record_tobe_updated['_id'])}, record_doc)


@app.route('/')
def home():
    '''
    Show home template with bubble chart
    '''

    chart_data = mongo.db.recipes.aggregate([
        {'$lookup': {
            'from': 'categories',
            'localField': 'category_id',
            'foreignField': '_id',
            'as': 'category_name'}},
        {'$unwind': '$category_name'},
        {'$lookup': {
            'from': 'cuisines',
            'localField': 'cuisine_id',
            'foreignField': '_id',
            'as': 'cuisine_name'}},
        {'$unwind': '$cuisine_name'},
        {'$group': {
            '_id': '$cuisine_name', 'total_votes': {'$sum': '$user_votes'}}},
        {'$sort': SON([('total_votes', -1), ('_id', -1)])}])

    result_cleaned = []

    for x in chart_data:
        result_cleaned.append({
            'name': x['_id']['cuisine_name'],
            'value': x['total_votes'],
            'url': os.environ['CURRENT_HOST'] +
            '/chart_search_recipes/' + x['_id']['cuisine_name']})

    if (len(result_cleaned) == 0):
        result_cleaned.append({
            'name': 'No Recipes, register to add recipes',
            'value': 1, 'url': os.environ['CURRENT_HOST'] + '/register'})

    chart_data = dumps({'name': 'A1', 'children': result_cleaned}, indent=2)

    return render_template(
        'index.html',
        resultData=chart_data,
        chart_switch=len(result_cleaned))


# somewhere to login
@app.route("/login", methods=['GET', 'POST'])
def login():
    '''
    Login or show the login template
    '''

    form = LoginForm()
    if request.method == 'POST':
        if not form.validate_on_submit():
            return render_template('login.html', form=form)
        else:
            email = request.form['email']
            form_password = request.form['password']
            try:
                login_user_record = mongo.db.users.find_one({'email': email})
                user = User(str(login_user_record['_id']))
            except(TypeError):
                flash('Sorry login failed')
                return render_template('login.html', form=form)

            login_user(user, remember=request.form.get('remember_me', False))

            is_valid_user = user.validate_login(
                login_user_record['password'], form_password)

            if is_valid_user is True:
                login_user(
                    user, remember=request.form.get('remember_me', False))
                flash('Welcome back, you\'re logged in')
                return redirect('/')
            else:
                flash('Sorry login failed')
                return render_template('login.html', form=form)
    else:
        return render_template('login.html', form=form)


# somewhere to regiser
@app.route("/register", methods=['GET', 'POST'])
def register():
    '''
    Register a new user or update an existing user where email exists
    '''

    form = RegistrationForm()
    if request.method == 'POST':
        if not form.validate_on_submit():
            return render_template('register.html', form=form)
        else:
            username = request.form['username']
            email = request.form['email']
            password = request.form['password']
            existing_user = mongo.db.users.find_one({'email': email})
            hashpass = generate_password_hash(
                request.form['password'], method='pbkdf2:sha512')

            if existing_user:
                register_record = mongo.db.users.update({
                    '_id': ObjectId(existing_user['_id'])},
                        {'username': username, 'email': email,
                            'password': hashpass})
                user = User(str(existing_user['_id']))
            else:
                user_doc = {
                    'username': username,
                    'email': email,
                    'password': hashpass}
                register_record = mongo.db.users.insert_one(user_doc)
                user = User(str(register_record.inserted_id))

            login_user(user)
        return redirect('/add_category')
    else:
        return render_template('register.html', form=form)


# somewhere to logout
@app.route("/logout")
@login_required
def logout():
    '''
    Logout
    '''

    logout_user()
    return render_template('logout.html')


# callback to reload the user object
@login_manager.user_loader
def load_user(userid):
    '''
    Login
    '''

    return User(userid)


@app.route('/add_category')
@login_required
def add_category():
    '''
    Show create category template
    '''
    return render_template('add_category.html')


@app.route('/add_cuisine')
@login_required
def add_cuisine():
    '''
    Show create cuisine template
    '''

    return render_template('add_cuisine.html')


@app.route('/insert_category', methods=['POST'])
@login_required
def insert_category():
    '''
    Create a category
    '''

    categories = mongo.db.categories
    category_doc = {'category_name': request.form['category_name']}
    categories.insert_one(category_doc)
    return redirect(url_for('get_categories'))


@app.route('/insert_cuisine', methods=['POST'])
@login_required
def insert_cuisine():
    '''
    Create a cuisine
    '''

    cuisines = mongo.db.cuisines
    cuisine_doc = {'cuisine_name': request.form['cuisine_name']}
    cuisines.insert_one(cuisine_doc)
    return redirect(url_for('get_cuisines'))


@app.route('/get_categories')
def get_categories():
    '''
    Show all categories
    '''

    return render_template(
        'get_categories.html', categories=mongo.db.categories.find())


@app.route('/get_cuisines')
def get_cuisines():
    '''
    Show all cuisines
    '''
    return render_template(
        'get_cuisines.html', cuisines=mongo.db.cuisines.find())


@app.route('/edit_category/<category_id>')
@login_required
def edit_category(category_id):
    '''
    Show the edit category template
    '''

    return render_template(
        'edit_category.html',
        category=mongo.db.categories.find_one({'_id': ObjectId(category_id)}))


@app.route('/edit_cuisine/<cuisine_id>')
@login_required
def edit_cuisine(cuisine_id):
    '''
    Show the edit cuisine template
    '''

    return render_template(
        'edit_cuisine.html',
        cuisine=mongo.db.cuisines.find_one({'_id': ObjectId(cuisine_id)}))


@app.route('/category_item/<category_id>', methods=["POST"])
@login_required
def update_category(category_id):
    '''
    Update a category record
    '''

    category_items = mongo.db.categories
    category_items.update({
        '_id': ObjectId(category_id)},
        {'category_name': request.form['category_name']})
    return redirect(url_for('get_categories'))


@app.route('/cuisine_item/<cuisine_id>', methods=["POST"])
@login_required
def update_cuisine(cuisine_id):
    '''
    Update a cuisine record
    '''

    cuisine_items = mongo.db.cuisines
    cuisine_items.update({
        '_id': ObjectId(cuisine_id)},
        {'cuisine_name': request.form['cuisine_name']})
    return redirect(url_for('get_cuisines'))


@app.route('/delete_category/<category_id>')
@login_required
def delete_category(category_id):
    '''
    Delete a category
    '''

    mongo.db.categories.remove({'_id': ObjectId(category_id)})
    return redirect(url_for("get_categories"))


@app.route('/delete_cuisine/<cuisine_id>')
@login_required
def delete_cuisine(cuisine_id):
    '''
    Delete a cuisine
    '''

    mongo.db.cuisines.remove({'_id': ObjectId(cuisine_id)})
    return redirect(url_for("get_cuisines"))


@app.route('/add_recipe')
@login_required
def add_recipe():
    '''
    Show create recipe template
    '''

    return render_template(
        'add_recipe.html',
        categories=mongo.db.categories.find(),
        cuisines=mongo.db.cuisines.find())


@app.route('/get_recipes')
def get_recipes():
    '''
    Show all recipes
    '''

    return render_template(
        'get_recipes.html',
        recipes=mongo.db.recipes.aggregate([{
            '$lookup': {
                'from': 'categories',
                'localField': 'category_id',
                'foreignField': '_id',
                'as': 'category_name'}},
            {'$unwind': '$category_name'},
            {'$lookup': {
                'from': 'cuisines',
                'localField': 'cuisine_id',
                'foreignField': '_id',
                'as': 'cuisine_name'}},
            {'$unwind': '$cuisine_name'}]))


@app.route('/search')
def search():
    return render_template('search.html')


@app.route('/search_recipes', methods=["POST"])
def search_recipes():
    '''
    Search for recipes by Category/Cuisine/User Votes
    and containing search string
    '''

    search_text = request.form['search_text']

    if (SEARCH_TYPE.CATEGORY_NAME.value == request.form['search_selected']):
        search_column = urllib.parse.quote_plus(
            SEARCH_TYPE.CATEGORY_NAME.value)
    elif (SEARCH_TYPE.CUISINE_NAME.value == request.form['search_selected']):
        search_column = urllib.parse.quote_plus(SEARCH_TYPE.CUISINE_NAME.value)
    elif (SEARCH_TYPE.USER_VOTES.value == request.form['search_selected']):
        search_column = urllib.parse.quote_plus(SEARCH_TYPE.USER_VOTES.value)

    if (SORT_ORDER.USER_VOTES_ASCENDING.value
            == request.form['order_selected']):
        sort_column = urllib.parse.quote_plus(SORT_COLUMN.USER_VOTES.value)
        sort_order = 1
    elif (SORT_ORDER.USER_VOTES_DESCENDING.value
            == request.form['order_selected']):
        sort_column = urllib.parse.quote_plus(SORT_COLUMN.USER_VOTES.value)
        sort_order = -1
    elif (SORT_ORDER.TOTAL_TIME_ASCENDING.value
            == request.form['order_selected']):
        sort_column = urllib.parse.quote_plus(SORT_COLUMN.TOTAL_TIME.value)
        sort_order = 1
    elif (SORT_ORDER.TOTAL_TIME_DESCENDING.value
            == request.form['order_selected']):
        sort_column = urllib.parse.quote_plus(SORT_COLUMN.TOTAL_TIME.value)
        sort_order = -1

    results = mongo.db.recipes.aggregate([
        {'$lookup': {
            'from': 'categories',
            'localField': 'category_id',
            'foreignField': '_id',
            'as': 'category_name'}},
        {'$unwind': '$category_name'},
        {'$lookup': {
            'from': 'cuisines',
            'localField': 'cuisine_id',
            'foreignField': '_id',
            'as': 'cuisine_name'}},
        {'$unwind': '$cuisine_name'},
        {'$match': {search_column: {'$regex': search_text, '$options': 'i'}}},
        {'$sort': SON([(sort_column, sort_order)])}])

    return render_template(
        'search_recipes.html',
        recipes=mongo.db.recipes.aggregate([{
            '$lookup': {
                'from': 'categories',
                'localField': 'category_id',
                'foreignField': '_id',
                'as': 'category_name'}},
            {'$unwind': '$category_name'},
            {'$lookup': {
                'from': 'cuisines',
                'localField': 'cuisine_id',
                'foreignField': '_id',
                'as': 'cuisine_name'}},
            {'$unwind': '$cuisine_name'},
            {'$match': {search_column: {
                '$regex': search_text, '$options': 'i'}}},
            {'$sort': SON([(sort_column, sort_order)])}]),
        number_results=len(list(results)))


@app.route('/chart_search_recipes/<name>')
def chart_search_recipes(name):
    '''
    Show recipes from clicked chart bubble
    '''

    search_text = name
    search_column = 'cuisine_name.cuisine_name'
    sort_column = 'user_votes'
    sort_order = -1
    results = mongo.db.recipes.aggregate([
        {'$lookup': {
            'from': 'categories',
            'localField': 'category_id',
            'foreignField': '_id',
            'as': 'category_name'}},
        {'$unwind': '$category_name'},
        {'$lookup': {
            'from': 'cuisines',
            'localField': 'cuisine_id',
            'foreignField': '_id',
            'as': 'cuisine_name'}},
        {'$unwind': '$cuisine_name'},
        {'$match': {search_column: {'$regex': search_text, '$options': 'i'}}},
        {'$sort': SON([(sort_column, sort_order)])}])
    return render_template(
        'search_recipes.html',
        recipes=mongo.db.recipes.aggregate([
            {'$lookup': {
                'from': 'categories',
                'localField': 'category_id',
                'foreignField': '_id',
                'as': 'category_name'}},
            {'$unwind': '$category_name'},
            {'$lookup': {
                'from': 'cuisines',
                'localField': 'cuisine_id',
                'foreignField': '_id',
                'as': 'cuisine_name'}},
            {'$unwind': '$cuisine_name'},
            {'$match': {search_column: {
                '$regex': search_text, '$options': 'i'}}},
            {'$sort': SON([(sort_column, sort_order)])}]),
        number_results=len(list(results)))


@app.route('/insert_recipe', methods=['POST'])
@login_required
def insert_recipe():
    '''
    Create a recipe
    '''

    recipes = mongo.db.recipes
    category_id = get_collection_id(
        'categories', 'category_name', request.form.to_dict()['category_name'])
    cuisine_id = get_collection_id(
        'cuisines', 'cuisine_name', request.form.to_dict()['cuisine_name'])
    recipe_doc = {
        'recipe_name': request.form.to_dict()['recipe_name'],
        'recipe_description': request.form.to_dict()['recipe_description'],
        'category_id': category_id,
        'cuisine_id': cuisine_id,
        'total_time': int(request.form.to_dict()['total_time']),
        'user_votes': int(request.form.to_dict()['user_votes'])}
    # recipes record insertion
    _recipe_id = recipes.insert_one(recipe_doc)
    # ingredients record insertion
    insert_record(
        id_name='recipe_id',
        insert_record_id=_recipe_id.inserted_id,
        record_set_dict=request.form.to_dict().items(),
        filter_key='ingredient', collection_name='ingredients')
    # instructions record insertion
    insert_record(
        id_name='recipe_id', insert_record_id=_recipe_id.inserted_id,
        record_set_dict=request.form.to_dict().items(),
        filter_key='instruction', collection_name='instructions')
    return redirect(url_for('get_recipes'))


@app.route('/show_recipe/<recipe_id>')
def show_recipe(recipe_id):
    '''
    Show a selected recipe
    '''

    recipe_record = mongo.db.recipes.find_one({'_id': ObjectId(recipe_id)})
    ingredients = mongo.db.ingredients.find_one({
        'recipe_id': ObjectId(recipe_id)})
    instructions = mongo.db.instructions.find_one({
        'recipe_id': ObjectId(recipe_id)})
    return render_template(
        'show_recipe.html',
        recipes=mongo.db.recipes.find_one({'_id': ObjectId(recipe_id)}),
        categories=mongo.db.categories.find_one({
            '_id': recipe_record['category_id']}),
        cuisines=mongo.db.cuisines.find_one({
            '_id': recipe_record['cuisine_id']}),
        instructions=instructions['instructions'],
        ingredients=ingredients['ingredients'])


@app.route('/edit_recipe/<recipe_id>')
@login_required
def edit_recipe(recipe_id):
    '''
    Edit recipe
    '''

    recipe_record = mongo.db.recipes.find_one({'_id': ObjectId(recipe_id)})
    ingredients = mongo.db.ingredients.find_one({
        'recipe_id': ObjectId(recipe_id)})
    instructions = mongo.db.instructions.find_one({
        'recipe_id': ObjectId(recipe_id)})
    return render_template(
        'edit_recipe.html',
        recipes=mongo.db.recipes.find_one({'_id': ObjectId(recipe_id)}),
        categories=mongo.db.categories.find(),
        cuisines=mongo.db.cuisines.find(),
        selected_category=mongo.db.categories.find_one({
            '_id': recipe_record['category_id']}),
        selected_cuisine=mongo.db.cuisines.find_one({
            '_id': recipe_record['cuisine_id']}),
        instructions=instructions['instructions'],
        ingredients=ingredients['ingredients'])


@app.route('/update_recipe/<recipe_id>', methods=["POST"])
@login_required
def update_recipe(recipe_id):
    '''
    Update recipe
    '''

    recipes = mongo.db.recipes
    category_id = get_collection_id('categories', 'category_name',
                                    request.form.to_dict()['category_name'])
    cuisine_id = get_collection_id(
        'cuisines', 'cuisine_name', request.form.to_dict()['cuisine_name'])
    recipe_doc = {
        'recipe_name': request.form.to_dict()['recipe_name'],
        'recipe_description': request.form.to_dict()['recipe_description'],
        'category_id': category_id,
        'cuisine_id': cuisine_id,
        'total_time': int(request.form.to_dict()['total_time']),
        'user_votes': int(request.form.to_dict()['user_votes'])}

    # recipes record update
    recipes.update({'_id': ObjectId(recipe_id)}, recipe_doc)
    # ingredients record update
    update_record(
        id_name='recipe_id', update_record_id=recipe_id,
        record_set_dict=request.form.to_dict().items(),
        filter_key='ingredient', collection_name='ingredients')
    # instructions record update
    update_record(
        id_name='recipe_id', update_record_id=recipe_id,
        record_set_dict=request.form.to_dict().items(),
        filter_key='instruction', collection_name='instructions')
    return redirect(url_for('get_recipes'))


@app.route('/delete_recipe/<recipe_id>')
@login_required
def delete_recipe(recipe_id):
    '''
    Delete recipe
    '''

    recipe_record = mongo.db.recipes.remove({'_id': ObjectId(recipe_id)})
    ingredients = mongo.db.ingredients.remove({
        'recipe_id': ObjectId(recipe_id)})
    instructions = mongo.db.instructions.remove({
        'recipe_id': ObjectId(recipe_id)})
    return redirect(url_for('get_recipes'))


if __name__ == '__main__':
    app.run(host=os.environ.get('IP'), port=os.environ['PORT'], debug=True)
