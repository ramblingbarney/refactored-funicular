import os
import unittest
import config
from app import app
from pymongo import MongoClient
import urllib.parse
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException


class RecipeBuddyUITests(unittest.TestCase):

    USERNAME = urllib.parse.quote_plus(config.MONGO_USERNAME)
    PASSWORD = urllib.parse.quote_plus(config.MONGO_PASSWORD)

    CLIENT = MongoClient('mongodb://%s:%s@127.0.0.1:27017/recipe_app_testing' % (USERNAME, PASSWORD))

    DB = CLIENT.recipe_app_testing

    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):

        # delete fixture collections
        self.DB.categories.delete_many({})
        self.DB.recipes.delete_many({})
        self.DB.instructions.delete_many({})
        self.DB.ingredients.delete_many({})

        # create the 'categories' collection in MongoDB
        self.collection_categories = self.DB.categories

        # categores to insert

        category_1 = {
            'category_name': 'Thai'
        }
        category_2 = {
            'category_name': 'Chinese'
        }
        category_3 = {
            'category_name': 'Indian'
        }

        # insert categories collection
        new_result = self.collection_categories.insert_many([category_1,
                                                            category_2,
                                                            category_3])

        # create the 'recipes' collection in MongoDB
        self.collection_recipes = self.DB.recipes

        # recipes to insert

        recipe_1 = {'recipe_name': 'Avocado and Tuna Tapas',
                'recipe_description': 'Living in Spain I have come across a literal plethora of tapas. This is a light, healthy tapa that goes best with crisp white wines and crunchy bread. This recipe is great for experimenting with a variety of different vegetables, spices, and vinegars.'}


        recipe_2 = {'recipe_name': 'Chinese Pepper Steak',
                'recipe_description': 'A delicious meal, served with boiled white rice, that\'s easy and made from items that I\'ve already got in my cupboards! My mother clipped this recipe from somewhere and it became a specialty of mine; however, I\'ve been unable to find the original source.'}


        recipe_3 = {'recipe_name': 'Moroccan Chicken with Saffron and Preserved Lemon',
                'recipe_description': 'Chicken thighs full of spice and amazing scents to take you right to the Mediterranean. Great with quinoa or brown rice and lots green veggies.'}


        # insert recipes collection

        insert_recipe_1 = self.collection_recipes.insert_one(recipe_1)
        insert_recipe_2 = self.collection_recipes.insert_one(recipe_2)
        insert_recipe_3 = self.collection_recipes.insert_one(recipe_3)

        instructions_1 = {'recipe_id': insert_recipe_1.inserted_id, 'instructions' : [ "mix 3 eggs", "whisk", "put on low heat"]}

        ingredients_1 = {'recipe_id': insert_recipe_1.inserted_id, 'ingredients' : [ "3 eggs", "100g butter", "0.5l water"]}

        instructions_2 = {'recipe_id': insert_recipe_2.inserted_id, 'instructions' : [ "peel 2 oranges", 'add flour', "put on high heat"]}

        ingredients_2 = {'recipe_id': insert_recipe_2.inserted_id, 'ingredients' : [ "2 oranges", "100g butter", "1l water", "200g flour"]}

        instructions_3 = {'recipe_id': insert_recipe_3.inserted_id, 'instructions' : [ "chop carrots", "fry on high heat with olive oil", "chop onions", "add onions once carrots soft"]}

        ingredients_3 = {'recipe_id': insert_recipe_3.inserted_id, 'ingredients' : [ "200g carrots", "drop of olive oil", "200g brown onions"]}

        # create the 'instructions' collection in MongoDB
        self.collection_instructions = self.DB.instructions
        # insert
        self.collection_instructions.insert_many([instructions_1, instructions_2, instructions_3])

        # create the 'ingredients' collection in MongoDB
        self.collection_ingredients = self.DB.ingredients
        # insert
        self.collection_ingredients.insert_many([ingredients_1, ingredients_2, ingredients_3])

        # creates a test client
        self.app = app.test_client()

        # propagate the exceptions to the test client
        self.app.testing = True

        # create selenium browser instance
        options = Options()
        options.add_argument("--headless")
        self.driver = webdriver.Chrome(options=options)

        self.elements = []
        self.li_span_text = []

    def tearDown(self):
        # delete fixture collections
        self.DB.categories.delete_many({})
        self.DB.recipes.delete_many({})
        self.DB.instructions.delete_many({})
        self.DB.ingredients.delete_many({})
        self.driver.quit()

    def test_three_categories(self):
        ''' Test 3 categories present '''

        self.driver.get("http://localhost:5000/get_categories")
        self.driver.implicitly_wait(0)  # seconds

        self.elements = self.driver.find_elements_by_class_name(
                                                        "category_list_item")

        test_list = ['Thai', 'Chinese', 'Indian']

        for element in self.elements:
            self.li_span_text.append(element.text)

        self.assertListEqual(test_list, self.li_span_text)

    def test_categories_delete_buttons(self):
        ''' Test 3 delete buttons present '''

        self.driver.get("http://localhost:5000/get_categories")
        self.driver.implicitly_wait(0)  # seconds

        self.elements = self.driver.find_elements_by_class_name(
                                                    "delete_category_button")

        self.assertEqual(len(self.elements), 3)

    def test_categories_edit_buttons(self):
        ''' Test 3 edit buttons present '''

        self.driver.get("http://localhost:5000/get_categories")
        self.driver.implicitly_wait(0)  # seconds

        self.elements = self.driver.find_elements_by_class_name(
                                                        "edit_category_button")

        self.assertEqual(len(self.elements), 3)

    def test_add_category(self):
        ''' Test Adding a Category'''

        self.driver.get("http://localhost:5000/get_categories")
        self.driver.implicitly_wait(0)  # seconds
        element = self.driver.find_element_by_id("add_category")
        element.click()
        self.driver.implicitly_wait(0)  # seconds
        self.driver.find_element_by_id("category_name").send_keys(
                                            'Spanish')
        self.driver.implicitly_wait(0)  # seconds
        added_category_button = self.driver.find_element_by_id("add_category")
        added_category_button.click()
        self.driver.implicitly_wait(0)  # seconds

        self.elements = self.driver.find_elements_by_class_name(
                                                        "category_list_item")

        test_list = ['Thai', 'Chinese', 'Indian', 'Spanish']

        for element in self.elements:
            self.li_span_text.append(element.text)

        self.assertListEqual(test_list, self.li_span_text)

    def test_delete_first_category(self):
        ''' Test Deleting the first Category item'''

        self.driver.get("http://localhost:5000/get_categories")
        self.driver.implicitly_wait(0)  # seconds
        try:
            element = self.driver.find_element_by_class_name(
                                                    "delete_category_button")
            element.click()

        except NoSuchElementException:
            True

        self.elements = self.driver.find_elements_by_class_name(
                                                        "category_list_item")

        test_list = ['Chinese', 'Indian']

        for element in self.elements:
            self.li_span_text.append(element.text)

        self.assertListEqual(test_list, self.li_span_text)

    def test_delete_all_categories(self):
        ''' Test Deleting the first Category item'''

        self.driver.get("http://localhost:5000/get_categories")
        self.driver.implicitly_wait(0)  # seconds

        while len(self.driver.find_elements_by_class_name(
                                                "delete_category_button")) > 0:
            try:
                element = self.driver.find_element_by_class_name(
                                                    "delete_category_button")
                element.click()

            except NoSuchElementException:
                True

        self.assertEqual(len(self.driver.find_elements_by_class_name(
                                                "delete_category_button")), 0)

    def test_delete_last_category(self):
        ''' Test Deleting the first Category item'''

        self.driver.get("http://localhost:5000/get_categories")
        self.driver.implicitly_wait(0)  # seconds
        try:
            elements = self.driver.find_elements_by_class_name(
                                                    "delete_category_button")
            elements[2].click()

        except NoSuchElementException:
            True

        self.elements = self.driver.find_elements_by_class_name(
                                                        "category_list_item")

        test_list = ['Thai', 'Chinese']

        for element in self.elements:
            self.li_span_text.append(element.text)

        self.assertListEqual(test_list, self.li_span_text)

    def test_edit_last_category(self):
        ''' Test editing the last Category'''

        self.driver.get("http://localhost:5000/get_categories")
        self.driver.implicitly_wait(0)  # seconds

        element = self.driver.find_elements_by_class_name(
                                                        "edit_category_button")
        element[2].click()
        self.driver.implicitly_wait(0)  # seconds
        self.driver.find_element_by_id("category_name").send_keys('1')
        edit_category_button = self.driver.find_element_by_id("edit_category")
        edit_category_button.click()
        self.driver.implicitly_wait(0)  # seconds

        self.elements = self.driver.find_elements_by_class_name(
                                                        "category_list_item")

        test_list = ['Thai', 'Chinese', 'Indian1']

        for element in self.elements:
            self.li_span_text.append(element.text)

        self.assertListEqual(test_list, self.li_span_text)

    def test_cancel_edit_category(self):
        ''' Test cancelling editing a Category'''
        self.driver.get("http://localhost:5000/get_categories")
        elements = self.driver.find_elements_by_class_name(
                                                        "edit_category_button")
        elements[1].click()
        self.driver.implicitly_wait(0)  # seconds
        self.driver.find_element_by_id("cancel_category").click()
        self.driver.implicitly_wait(0)  # seconds
        self.assertEqual(self.driver.current_url,
                        'http://localhost:5000/get_categories')


    def test_three_recipes_headings(self):
        ''' Test 3 recipes headings present '''

        self.driver.get("http://localhost:5000/get_recipes")
        self.driver.implicitly_wait(0)  # seconds

        self.elements = self.driver.find_elements_by_xpath("//div[starts-with(@class, 'recipe-header')]/strong")

        test_list = ['Avocado and Tuna Tapas',
                    'Chinese Pepper Steak',
                    'Moroccan Chicken with Saffron and Preserved Lemon']
        #
        for element in self.elements:
            self.li_span_text.append(element.text)

        self.assertListEqual(test_list, self.li_span_text)

    def test_three_recipes_description(self):
        ''' Test 3 recipes headings present '''

        self.driver.get("http://localhost:5000/get_recipes")
        self.driver.implicitly_wait(0)  # seconds

        self.elements = self.driver.find_elements_by_xpath("//div[contains(@class, 'recipe-description')]/span")

        self.assertEqual(len(self.elements), 3)


    def test_add_recipe_headings(self):
        ''' Test Adding a Recipe Heading'''

        self.driver.get("http://localhost:5000/add_recipe")
        self.driver.implicitly_wait(0)  # seconds
        self.driver.find_element_by_id("recipe-name").send_keys(
                                            'Vietnamese Grilled Lemongrass Chicken')
        self.driver.find_element_by_id("recipe-description").send_keys('Chicken marinated with lemongrass and grilled. Garnish with rice paper, lettuce, cucumber, bean sprouts, mint, and ground peanut.')
        self.driver.implicitly_wait(0)  # seconds
        added_category_button = self.driver.find_element_by_id("add-recipe")
        added_category_button.click()
        self.driver.implicitly_wait(3)  # seconds

        self.elements = self.driver.find_elements_by_xpath("//div[starts-with(@class, 'recipe-header')]/strong")

        test_list = ['Avocado and Tuna Tapas',
                        'Chinese Pepper Steak',
                        'Moroccan Chicken with Saffron and Preserved Lemon',
                        'Vietnamese Grilled Lemongrass Chicken']

        for element in self.elements:
            self.li_span_text.append(element.text)

        self.assertListEqual(test_list, self.li_span_text)

    def test_add_recipe_descriptions(self):
        ''' Test Adding a Recipe Description'''

        self.driver.get("http://localhost:5000/add_recipe")
        self.driver.implicitly_wait(0)  # seconds
        self.driver.find_element_by_id("recipe-name").send_keys(
                                            'Vietnamese Grilled Lemongrass Chicken')
        self.driver.find_element_by_id("recipe-description").send_keys('Chicken marinated with lemongrass and grilled. Garnish with rice paper, lettuce, cucumber, bean sprouts, mint, and ground peanut.')
        self.driver.implicitly_wait(0)  # seconds
        added_category_button = self.driver.find_element_by_id("add-recipe")
        added_category_button.click()
        self.driver.implicitly_wait(0)  # seconds

        self.elements = self.driver.find_elements_by_xpath("//div[contains(@class, 'recipe-description')]/span")

        self.assertEqual(len(self.elements), 4)

    def test_first_show_recipe_heading(self):
        ''' Test first show recipe headings present '''

        self.driver.get("http://localhost:5000/get_recipes")
        self.driver.implicitly_wait(0)  # seconds

        self.elements = self.driver.find_elements_by_xpath("//a[contains(@class, 'show_recipe_button')]")
        self.elements[0].click()

        self.driver.implicitly_wait(0)  # seconds

        self.element = self.driver.find_element_by_xpath("//div[starts-with(@class, 'recipe-header')]/strong")
        self.assertEqual('Avocado and Tuna Tapas', self.element.text)

    def test_first_show_recipe_description(self):
        ''' Test first show recipe description present '''

        self.driver.get("http://localhost:5000/get_recipes")
        self.driver.implicitly_wait(0)  # seconds

        self.elements = self.driver.find_elements_by_xpath("//a[contains(@class, 'show_recipe_button')]")
        self.elements[0].click()

        self.driver.implicitly_wait(0)  # seconds

        description_text = 'Living in Spain I have come across a literal plethora of tapas. This is a light, healthy tapa that goes best with crisp white wines and crunchy bread. This recipe is great for experimenting with a variety of different vegetables, spices, and vinegars.'

        self.element = self.driver.find_element_by_xpath("//div[contains(@class, 'recipe-description')]/span")

        self.assertEqual(self.element.text, description_text)

    def test_second_show_recipe_heading(self):
        ''' Test first show recipe headings present '''

        self.driver.get("http://localhost:5000/get_recipes")
        self.driver.implicitly_wait(0)  # seconds

        self.elements = self.driver.find_elements_by_xpath("//a[contains(@class, 'show_recipe_button')]")
        self.elements[1].click()

        self.driver.implicitly_wait(0)  # seconds

        self.element = self.driver.find_element_by_xpath("//div[starts-with(@class, 'recipe-header')]/strong")
        self.assertEqual('Chinese Pepper Steak', self.element.text)

    def test_second_show_recipe_description(self):
        ''' Test second show recipe description present '''

        self.driver.get("http://localhost:5000/get_recipes")
        self.driver.implicitly_wait(0)  # seconds

        self.elements = self.driver.find_elements_by_xpath("//a[contains(@class, 'show_recipe_button')]")
        self.elements[1].click()

        self.driver.implicitly_wait(0)  # seconds

        description_text = 'A delicious meal, served with boiled white rice, that\'s easy and made from items that I\'ve already got in my cupboards! My mother clipped this recipe from somewhere and it became a specialty of mine; however, I\'ve been unable to find the original source.'

        self.element = self.driver.find_element_by_xpath("//div[contains(@class, 'recipe-description')]/span")

        self.assertEqual(self.element.text, description_text)

    def test_third_show_recipe_heading(self):
        ''' Test third show recipe headings present '''

        self.driver.get("http://localhost:5000/get_recipes")
        self.driver.implicitly_wait(0)  # seconds

        self.elements = self.driver.find_elements_by_xpath("//a[contains(@class, 'show_recipe_button')]")
        self.elements[2].click()

        self.driver.implicitly_wait(0)  # seconds

        self.element = self.driver.find_element_by_xpath("//div[starts-with(@class, 'recipe-header')]/strong")
        self.assertEqual('Moroccan Chicken with Saffron and Preserved Lemon', self.element.text)

    def test_third_show_recipe_description(self):
        ''' Test third show recipe description present '''

        self.driver.get("http://localhost:5000/get_recipes")
        self.driver.implicitly_wait(0)  # seconds

        self.elements = self.driver.find_elements_by_xpath("//a[contains(@class, 'show_recipe_button')]")
        self.elements[2].click()

        self.driver.implicitly_wait(0)  # seconds

        description_text = 'Chicken thighs full of spice and amazing scents to take you right to the Mediterranean. Great with quinoa or brown rice and lots green veggies.'

        self.element = self.driver.find_element_by_xpath("//div[contains(@class, 'recipe-description')]/span")

        self.assertEqual(self.element.text, description_text)





# TODO: copy tests for category to time_estimates

# TODO: tests for show recipes
