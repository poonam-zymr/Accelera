from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
import unittest
import time
import properties
from utils import utils, db, results


class TestApplyConfig(unittest.TestCase):
    """This class verifies apply config functionality.
    """
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.base_url = properties.vm_url
        self.verificationErrors = []
        self.accept_next_alert = True

    def test_2_edit_config(self):
        """This test case verifies whether config is edited succesfully.
        """
        
    
    def tearDown(self):
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)    

        
if __name__ == "__main__":
    unittest.main()