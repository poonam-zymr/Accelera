from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
import unittest
import time
import re
from utils import utils, db, results
import properties


class TestCreateVar(unittest.TestCase):
    def setUp(self):
        utils.call_display_headless_browser()
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.base_url = properties.vm_url
        self.verificationErrors = []
        self.accept_next_alert = True

    def create_var(self):
        columns = utils.get_var_details()

        driver = self.driver
        driver.get(self.base_url + "/home/login")
        time.sleep(5)
        driver.find_element_by_id("SignUpLink").click()
        time.sleep(5)
        driver.find_element_by_id("name").clear()
        driver.find_element_by_id("name").send_keys(columns['var_business_name'][0])
        driver.find_element_by_id("street_addr_line_1").clear()
        driver.find_element_by_id("street_addr_line_1").send_keys(columns['street_addres_1'][0])
        driver.find_element_by_id("street_addr_line_2").clear()
        driver.find_element_by_id("street_addr_line_2").send_keys(columns['street_addres_2'][0])
        driver.find_element_by_id("city").clear()
        driver.find_element_by_id("city").send_keys(columns['city'][0])
        driver.find_element_by_id("zip_code").clear()
        driver.find_element_by_id("zip_code").send_keys(columns['zip'][0])
        driver.find_element_by_id("first_name").clear()
        driver.find_element_by_id("first_name").send_keys(columns['first_name'][0])
        driver.find_element_by_id("last_name").clear()
        driver.find_element_by_id("last_name").send_keys(columns['last_name'][0])
        driver.find_element_by_id("email").clear()
        driver.find_element_by_id("email").send_keys(columns['email'][0])
        driver.find_element_by_id("password").clear()
        driver.find_element_by_id("password").send_keys(columns['password'][0])
        driver.find_element_by_id("confirm_password").clear()
        driver.find_element_by_id("confirm_password").send_keys(columns['confirm_password'][0])
        driver.find_element_by_id("btnSignUp").click()
        time.sleep(10)

        #Verify VAR user was created in database
        var_name = str(columns['var_business_name'][0])
        db.search_var_in_var_collection(var_name)

        self.assertTrue(driver.find_element_by_id("congrats-popup").is_displayed())
        driver.find_element_by_id("LoginLink").click()

    def tearDown(self):
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)

# 
# if __name__ == "__main__":
#     unittest.main()


def test_generate_result():
    suite = unittest.TestSuite()
    #suite.addTest(TestCreateVar("setUp"))
    suite.addTest(TestCreateVar("create_var"))
    #suite.addTest(TestCreateVar("tearDown"))
    print suite
    print __file__
    results.run(suite, __file__)
