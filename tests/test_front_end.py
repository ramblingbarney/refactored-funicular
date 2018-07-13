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
        self.li_span_text = []

    def tearDown(self):
        # delete categories collection
        self.DB.categories.delete_many({})
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

# TODO: copy tests for category to time_estimates

# TODO: tests for add recipes -> get recipes
# TODO: tests for show recipies
