import os
import unittest
import config
from app import app
from flask_pymongo import PyMongo
from pymongo import MongoClient
import urllib.parse
from bson.objectid import ObjectId

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import helper_Web_Driver_Wait_CSS_Element


class RecipeBuddyUITests(unittest.TestCase):

    USERNAME = urllib.parse.quote_plus(config.MONGO_USERNAME)
    PASSWORD = urllib.parse.quote_plus(config.MONGO_PASSWORD)

    CLIENT = MongoClient('mongodb://%s:%s@ds131721.mlab.com:31721/recipe_app_testing' % (USERNAME, PASSWORD))

    DB = CLIENT.recipe_app_testing

    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):

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

        # creates a test client
        self.app = app.test_client()

        # propagate the exceptions to the test client
        self.app.testing = True

        # create selenium browser instance
        options = Options()
        options.add_argument("--headless")
        self.driver = webdriver.Chrome(options=options)

        self.elements = []

    def tearDown(self):
        # delete categories collection
        self.DB.categories.delete_many({})
        self.driver.quit()

    def test_three_categories(self):
        ''' Test 3 categories present '''

        page = self.driver.get("http://localhost:5000/get_categories")
        self.driver.implicitly_wait(0) # seconds

        self.elements = self.driver.find_elements_by_class_name("category_list_item")

        li_span_text = []
        test_list = ['Thai','Chinese','Indian']

        for element in self.elements:
            li_span_text.append(element.text)

        self.assertListEqual(test_list, li_span_text)

    def test_categories_delete_buttons(self):
        ''' Test 3 delete buttons present '''

        page = self.driver.get("http://localhost:5000/get_categories")
        self.driver.implicitly_wait(0) # seconds

        self.elements = self.driver.find_elements_by_class_name("delete_category_button")

        self.assertEqual(len(self.elements), 3)

    def test_categories_edit_buttons(self):
        ''' Test 3 edit buttons present '''

        page = self.driver.get("http://localhost:5000/get_categories")
        self.driver.implicitly_wait(0) # seconds

        self.elements = self.driver.find_elements_by_class_name("edit_category_button")

        self.assertEqual(len(self.elements), 3)
