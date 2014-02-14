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


class TestOnboardAP(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.base_url = properties.vm_url
        self.verificationErrors = []
        self.accept_next_alert = True

    def onboard_ap(self):
        columns = utils.get_var_details()
        driver = self.driver

        driver.get(self.base_url + "/home/login")
        driver.find_element_by_id("email").clear()
        driver.find_element_by_id("email").send_keys(columns['email'][0])
        driver.find_element_by_id("password").clear()
        driver.find_element_by_id("password").send_keys(columns['password'][0])
        driver.find_element_by_id("btnLogin").click()
        time.sleep(10)
        print "Clicking VAR filter dropdown"
        dropdown = driver.find_element_by_id("varFilter")
        for option in dropdown.find_elements_by_tag_name("option"):
            if option.text == columns['var_business_name'][0]:
                option.click()
                time.sleep(5)
        print "Clickin Customers dropdown"
        dropdown = driver.find_element_by_id("customerFilter")
        for option in dropdown.find_elements_by_tag_name("option"):
            if option.text == columns['var_business_name'][1]:
                option.click()
                time.sleep(5)
        print "Clickin Location dropdown"
        dropdown = driver.find_element_by_id("locationFilter")
        for option in dropdown.find_elements_by_tag_name("option"):
            if option.text == columns['var_business_name'][2]:
                option.click()
                time.sleep(5)
        driver.find_element_by_id("menuAccessPoints").click()
        driver.find_element_by_id("addBtn").click()
        driver.find_element_by_id("ap_name").clear()
        driver.find_element_by_id("ap_name").send_keys(properties.ap_name)
        driver.find_element_by_id("serial_number").clear()
        ap_jid = utils.get_ap_jid(properties.real_ap_ip)
        serial_no = db.search_serialno_in_new_ap_collection(ap_jid.strip())
        driver.find_element_by_id("serial_number").send_keys(serial_no)
        driver.find_element_by_id("addBtn").click()
        #driver.find_element_by_id("cancelBtn").click()
        time.sleep(3)
        db.search_ap_in_ap_collection(ap_jid.strip())
        
        #here put a check for template name should be updated as the config set for location

    def tearDown(self):
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)


def test_generate_result():
    suite = unittest.TestSuite()
    suite.addTest(TestOnboardAP("onboard_ap"))
    print suite
    print __file__
    results.run(suite, __file__)
