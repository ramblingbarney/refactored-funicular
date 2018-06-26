import unittest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time


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
        options.set_headless(headless=True)
        self.driver = webdriver.Chrome(options=options)

    def tearDown(self):
        self.driver.quit()


    def test_home_status_code(self):
        ''' Test index/home page route'''
        page = self.driver.get("http://localhost:5000/get_categories")
        time.sleep(3)
        self.driver.save_screenshot('/home/conor/screenie.png')
        print("screen shot done")
        # print(page)
