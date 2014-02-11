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


class TestCreateLocation(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.base_url = properties.vm_url
        self.verificationErrors = []
        self.accept_next_alert = True

    def create_location(self):
        columns = utils.get_var_details()
        driver = self.driver

        driver.get(self.base_url + "/home/login")
        driver.find_element_by_id("email").clear()
        driver.find_element_by_id("email").send_keys(columns['email'][0])
        driver.find_element_by_id("password").clear()
        driver.find_element_by_id("password").send_keys(columns['password'][0])
        driver.find_element_by_id("btnLogin").click()
        time.sleep(10)
        print "Clickin Customers default dropdown"
        dropdown = driver.find_element_by_id("customerFilter")
        for option in dropdown.find_elements_by_tag_name("option"):
            if option.get_attribute('value') == "-1":
                option.click()
                time.sleep(5)
        print "Clickin Customers dropdown"
        dropdown = driver.find_element_by_id("customerFilter")
        for option in dropdown.find_elements_by_tag_name("option"):
            if option.text == columns['var_business_name'][1]:
                option.click()
                time.sleep(5)

        driver.find_element_by_id("btnAddLocation").click()
        driver.find_element_by_id("name").clear()
        driver.find_element_by_id("name").send_keys(columns['var_business_name'][2])
        driver.find_element_by_id("street_addr_line_1").clear()
        driver.find_element_by_id("street_addr_line_1").send_keys(columns['street_addres_1'][2])
        driver.find_element_by_id("street_addr_line_2").clear()
        driver.find_element_by_id("street_addr_line_2").send_keys(columns['street_addres_2'][2])
        driver.find_element_by_id("city").clear()
        driver.find_element_by_id("city").send_keys(columns['city'][2])
        driver.find_element_by_id("state").clear()
        driver.find_element_by_id("state").send_keys(columns['state'][2])
        driver.find_element_by_id("zip_code").clear()
        driver.find_element_by_id("zip_code").send_keys(columns['zip'][2])

        config_dropdown = driver.find_element_by_id("config_id")
        for option in config_dropdown.find_elements_by_tag_name("option"):
            if option.text == columns['var_business_name'][2]:
                option.click()
                time.sleep(5)

        driver.find_element_by_id("btnAddLocation").click()
        time.sleep(3)
        db.search_location_in_location_collection(columns['var_business_name'][2])

    def tearDown(self):
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)


def test_generate_result():
    suite = unittest.TestSuite()
    suite.addTest(TestCreateLocation("create_location"))
    print suite
    print __file__
    results.run(suite, __file__)
