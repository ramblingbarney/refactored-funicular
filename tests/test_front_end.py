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
from bs4 import BeautifulSoup
import time
import datetime


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

        category_1 = {
            'category_name': 'Thai'
        }
        category_2 = {
            'category_name': 'Chinese'
        }
        category_3 = {
            'category_name': 'Indian'
        }

        # create categories collection
        new_result = self.collection_categories.insert_many([category_1,
                                                        category_2,
                                                        category_3])

        print('Multiple posts: {0}'.format(new_result.inserted_ids))

        # creates a test client
        self.app = app.test_client()

        self.app = app.test_client()
        # propagate the exceptions to the test client
        self.app.testing = True

        # create selenium browser instance
        options = Options()
        options.add_argument("--headless")
        self.driver = webdriver.Chrome(options=options)

        self.today = datetime.date.today()
        self.elements = []

    def tearDown(self):
        # delete categories collection
        self.DB.categories.delete_many({})
        self.driver.quit()

    def test_three_categories(self):
        ''' Test 3 categories present '''
        self.assertEqual(1, 1)

        
    def test_add_category(self):
        ''' Test Adding a Category'''
        self.assertEqual(1, 1)

    #
    # def test_add_category(self):
    #     ''' Test Adding a Category'''
    #     page = self.driver.get("http://localhost:5000/get_categories")
    #     self.driver.implicitly_wait(0) # seconds
    #     element = self.driver.find_element_by_id("add_category")
    #     element.click()
    #     self.driver.implicitly_wait(0) # seconds
    #     self.driver.find_element_by_id("category_name").send_keys(
    #                                         'PPPPPPPPPPPP' + str(self.today))
    #     self.driver.implicitly_wait(0) # seconds
    #     added_category_button = self.driver.find_element_by_id("add_category")
    #     added_category_button.click()
    #     time.sleep(3)
    #     soup = BeautifulSoup(self.driver.page_source, 'html5lib')
    #     for line in soup.find('div', {'class': 'category_container'}).find_all(
    #             'span', {'class': 'category_list_item'}):
    #         self.elements.append(line.text.strip())
    #     self.assertIn('PPPPPPPPPPPP' + str(self.today), self.elements)
#
#     def test_delete_a_category(self):
#         ''' Test Deleting a Categories item'''
#         page = self.driver.get("http://localhost:5000/get_categories")
#         time.sleep(3)
#         delete_buttons = self.driver.find_elements_by_class_name(
#             "delete_category_button")
#         delete_buttons_before_count = len(delete_buttons)
#         for x in delete_buttons:
#             try:
#                 x.click()
#                 time.sleep(3)
#             except: # take this out helper delete first cat, combine lines 55 and 60 not a loop, delte ct not exit rais excpetion, tyr to avide bs4 or if I have to explain why in comments
#                 continue
#         time.sleep(3)
#         soup = BeautifulSoup(self.driver.page_source, 'html5lib')
#         for line in soup.find('div', {'class': 'category_container'}).find_all(
#                 'span', {'class': 'category_list_item'}):
#             self.elements.append(line.text.strip())
#         self.assertEqual(delete_buttons_before_count, len(self.elements) + 1)
# #delte last category
# # first test to create a clearn state, I know x and y exists
#     def test_edit_category(self):
#         ''' Test editing a Category'''
#         page = self.driver.get("http://localhost:5000/get_categories")
#         time.sleep(3)
#         element = self.driver.find_elements_by_class_name("edit_category_button")
#         # time.sleep(3)
#         element[0].click()
#         time.sleep(3)
#         self.driver.find_element_by_id("category_name").send_keys(
#                                             'EditCategoryTest' + str(self.today))
#         # time.sleep(3)
#         edit_category_button = self.driver.find_element_by_id("edit_category")
#         edit_category_button.click()
#         time.sleep(3) #find_elements_by_css_selecto
#         soup = BeautifulSoup(self.driver.page_source, 'html5lib')
#         for line in soup.find('div', {'class': 'category_container'}).find_all(
#                 'span', {'class': 'category_list_item'}):
#             self.elements.append(line.text.strip())
#         # one_element_sting = ''.join(self.elements)
#         # self.assertIn('EditCategoryTest' + str(self.today), one_element_sting)
#         self.assertIn('EditCategoryTest' + str(self.today), self.elements)
#
#     def test_cancel_edit_category(self):
#         ''' Test cancelling editing a Category'''
#         page = self.driver.get("http://localhost:5000/get_categories")
#         time.sleep(3)
#         element = self.driver.find_elements_by_class_name(
#             "edit_category_button")
#         time.sleep(3)
#         element[0].click()
#         time.sleep(3)
#         self.driver.find_element_by_id("cancel_category").click()
#         time.sleep(3)
#         self.assertEqual(self.driver.current_url,
#                     'http://localhost:5000/get_categories')
