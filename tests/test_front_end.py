import unittest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import time
import datetime


class RecipeBuddyUITests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        # create selenium browser instance
        options = Options()
        # options.set_headless(headless=True)
        self.driver = webdriver.Chrome(options=options)
        self.today = datetime.date.today()
        self.elements = []

    def tearDown(self):
        self.driver.quit()

    def test_add_category(self):
        ''' Test Adding a Category'''
        page = self.driver.get("http://localhost:5000/get_categories")
        time.sleep(3)
        element = self.driver.find_element_by_id("add_category")
        time.sleep(3)
        element.click()
        time.sleep(3)
        self.driver.find_element_by_id("category_name").send_keys(
                                            'PPPPPPPPPPPP' + str(self.today))
        time.sleep(3)
        added_category_button = self.driver.find_element_by_id("add_category")
        added_category_button.click()
        time.sleep(3)
        soup = BeautifulSoup(self.driver.page_source, 'html5lib')
        for line in soup.find('div', {'class': 'category_container'}).find_all(
                'span', {'class': 'category_list_item'}):
            self.elements.append(line.text.strip())
        self.assertIn('PPPPPPPPPPPP' + str(self.today), self.elements)

    def test_delete_all_categories(self):
        ''' Test Deleting all Categories'''
        page = self.driver.get("http://localhost:5000/get_categories")
        time.sleep(3)
        delete_buttons = self.driver.find_elements_by_class_name(
            "delete_category_button")
        delete_buttons_before_count = len(delete_buttons)
        for x in delete_buttons:
            try:
                x.click()
            except:
                continue
        time.sleep(3)
        soup = BeautifulSoup(self.driver.page_source, 'html5lib')
        for line in soup.find('div', {'class': 'category_container'}).find_all(
                'span', {'class': 'category_list_item'}):
            self.elements.append(line.text.strip())
        assert delete_buttons_before_count - len(self.elements) == 1
