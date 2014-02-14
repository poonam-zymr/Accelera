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


class TestVerifyApGrid(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.base_url = properties.vm_url
        self.verificationErrors = []
        self.accept_next_alert = True

    def verify_apgrid(self):
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
                time.sleep(20)

        driver.find_element_by_id("menuAccessPoints").click()
        time.sleep(10)
        
        i = 0
        for option in driver.find_elements_by_css_selector("#ap_grid_table tbody tr"):
            client_name_id = "AP_Name_" + str(i)
            location_id = "Location_" + str(i)
            template_id = "Template_" + str(i)
            mac_address_id = "MAC_Address_" + str(i)
            ip_address_id = "IP_Address_" + str(i)
            assoc_clients_id = "Associated_Clients_" + str(i)
            ap_model_id = "AP_Model_" + str(i)
            status_id = "Status_" + str(i)
            if properties.ap_name == str(driver.find_element_by_css_selector("#" + client_name_id + " a").get_attribute('innerHTML')):

                print "AP Name = " + str(driver.find_element_by_css_selector('#' + client_name_id + ' a').get_attribute('innerHTML'))
                actual_ap_location = driver.find_element_by_id(location_id).get_attribute('innerHTML')
                print "Actual location of the AP = " +actual_ap_location
                print "Expected location of the AP = " +columns['var_business_name'][2]
                self.assertEqual(actual_ap_location, columns['var_business_name'][2], "Actual location of the AP is not same as Expected location!")
 
                actual_config = driver.find_element_by_id(template_id).get_attribute('innerHTML')
                print "Actual config of the AP = " +actual_config
                print "Expected config of the AP = " +columns['var_business_name'][2]
                self.assertEqual(actual_config, columns['var_business_name'][2], "Actual config of the AP is not same as Expected config!")
                
                actual_mac = driver.find_element_by_id(mac_address_id).get_attribute('innerHTML')
                print "Actual MAC of the AP = " +actual_mac
                expected_mac = db.search_mac_in_ap_collection(properties.ap_name)
                print "Expected MAC of the AP = " +expected_mac
                self.assertEqual(actual_mac, expected_mac, "Actual MAC address of the AP is not same as Expected MAC address!")
                
                actual_ip = driver.find_element_by_id(ip_address_id).get_attribute('innerHTML')
                print "Actual IP of the AP = " +actual_ip
                expected_ip = db.search_ip_in_ap_collection(properties.ap_name)
                print "Expected IP of the AP = " +expected_ip
                self.assertEqual(actual_ip, expected_ip, "Actual AP address of the AP is not same as Expected AP address!")
                
                actual_no_of_clients = driver.find_element_by_id(assoc_clients_id).get_attribute('innerHTML')
                print "Actual Clients of the AP = " +actual_no_of_clients
                expected_no_of_clients = utils.get_client_count()
                print "Expected Clients of the AP = " +expected_no_of_clients
                self.assertEqual(actual_no_of_clients, expected_no_of_clients, "Actual Number of clients of the AP is not same as Expected clients!")

                actual_model = driver.find_element_by_id(ap_model_id).get_attribute('innerHTML')
                print "Actual model of the AP = " +actual_model
                expected_model = db.search_model_in_ap_collection(properties.ap_name)
                print "Expected model of the AP = " +expected_model
                self.assertEqual(actual_model, expected_model, "Actual Model of the AP is not same as Expected Model!")

                actual_ap_status = driver.find_element_by_css_selector('#' + status_id + ' img').get_attribute('title')
                print "Actual status of the AP = " +actual_ap_status
                expected_ap_status = 'available'
                print "Expected status of the AP = " +expected_ap_status
                self.assertEqual(actual_ap_status, expected_ap_status, "AP is in Not Available status!")

            i = i+1

            
    def tearDown(self):
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)


def test_generate_result():
    suite = unittest.TestSuite()
    suite.addTest(TestVerifyApGrid("verify_apgrid"))
    print suite
    print __file__
    results.run(suite, __file__)
