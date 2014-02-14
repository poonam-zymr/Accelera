from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
import unittest
import time
import re
import properties
from utils import utils, db, results


class TestCreateCustomer(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.base_url = properties.vm_url
        self.verificationErrors = []
        self.accept_next_alert = True

    def create_customer(self):
        columns = utils.get_var_details()
        driver = self.driver

        driver.get(self.base_url + "/home/login")
        driver.find_element_by_id("email").clear()
        driver.find_element_by_id("email").send_keys(columns['email'][0])
        driver.find_element_by_id("password").clear()
        driver.find_element_by_id("password").send_keys(columns['password'][0])
        driver.find_element_by_id("btnLogin").click()

        #driver.get(self.base_url + "/var/var_dashboard")
        time.sleep(10)
        print "Clicking VAR filter dropdown"
        dropdown = driver.find_element_by_id("varFilter")
        for option in dropdown.find_elements_by_tag_name("option"):
            if option.text == columns['var_business_name'][0]:
                option.click()
                time.sleep(5)
        driver.find_element_by_id("btnAddCustomer").click()
        driver.find_element_by_id("name").clear()
        driver.find_element_by_id("name").send_keys(columns['var_business_name'][1])
        driver.find_element_by_id("street_addr_line_1").clear()
        driver.find_element_by_id("street_addr_line_1").send_keys(columns['street_addres_1'][1])
        driver.find_element_by_id("street_addr_line_2").clear()
        driver.find_element_by_id("street_addr_line_2").send_keys(columns['street_addres_2'][1])
        driver.find_element_by_id("city").clear()
        driver.find_element_by_id("city").send_keys(columns['city'][1])
        driver.find_element_by_id("zip_code").clear()
        driver.find_element_by_id("zip_code").send_keys(columns['zip'][1])
        driver.find_element_by_id("first_name").clear()
        driver.find_element_by_id("first_name").send_keys(columns['first_name'][1])
        driver.find_element_by_id("last_name").clear()
        driver.find_element_by_id("last_name").send_keys(columns['last_name'][1])
        driver.find_element_by_id("email").clear()
        driver.find_element_by_id("email").send_keys(columns['email'][1])
        driver.find_element_by_id("password").clear()
        driver.find_element_by_id("password").send_keys(columns['password'][1])
        driver.find_element_by_id("confirm_password").clear()
        driver.find_element_by_id("confirm_password").send_keys(columns['confirm_password'][1])
        driver.find_element_by_id("btnAddCustomer").click()

        #Verify Customer user was created in database
        cust_name = str(columns['var_business_name'][1])
        print "Customer name is: " + cust_name
        time.sleep(2)
        db.search_cust_in_customer_collection(cust_name)

    def tearDown(self):
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)


def test_generate_result():
    suite = unittest.TestSuite()
    suite.addTest(TestCreateCustomer("create_customer"))
    print suite
    print __file__
    results.run(suite, __file__)
