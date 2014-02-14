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


class TestVerifyCustomerDashboard(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.base_url = properties.vm_url
        self.verificationErrors = []
        self.accept_next_alert = True


    def verify_customer_dashboard(self):
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
        
        for i in range(0, 1):
            top5_device_id = "top_devices_" + str(i)

            #Retrieve the name of the client mentioned in the static stats file which is in form of mac
            name = utils.get_client_name()
            #Extract last 3 subsets of the mac and compare with that in the Client name griD
            expected_client_substr = name[-8:]
            actual_client_name = driver.find_element_by_css_selector('#' + top5_device_id + ' a').get_attribute('innerHTML').strip()
            print "Actual client name = " +str(actual_client_name) 
            print "Expected Client should contain: " +expected_client_substr
             
            if expected_client_substr in actual_client_name:    
                actual_client_traffic = driver.find_element_by_css_selector('#' + top5_device_id + ' div.overviewTableTextSecondary').get_attribute('innerHTML')
                print "Actual Top 5 Devices traffic = " +str(actual_client_traffic)
                bytes_rx = utils.get_client_stats("bytes_rx")
                bytes_tx = utils.get_client_stats("bytes_tx")
                expected_client_traffic = utils.caluclate_cust_dashboard_top5devices_traffic_kbps(bytes_rx, bytes_tx)
                print "Expected Top 5 Devices traffic =  " +str(expected_client_traffic)
                self.assertEqual(actual_client_traffic, expected_client_traffic, "Actual traffic of the Top 5 Devices is not same as Expected traffic!")
                break
            else:
                continue
            
        for i in range(0, 1):
            top5_ssid_id = "top_ssid_" + str(i)
   
            expected_ssid_name = columns['var_business_name'][2]
            actual_ssid_name = driver.find_element_by_css_selector('#' + top5_ssid_id + ' a').get_attribute('innerHTML').strip()
            print "Actual SSID name = " +str(actual_ssid_name) 
            print "Expected SSID name = " +expected_ssid_name
                
            if expected_ssid_name == actual_ssid_name:    
                actual_ssid_traffic = driver.find_element_by_css_selector('#' + top5_ssid_id + ' div.overviewTableTextSecondary').get_attribute('innerHTML')
                print "Actual Top 5 SSIDs traffic = " +str(actual_ssid_traffic)
                bytes_rx = utils.get_ap_stats("bytes_rx")
                bytes_tx = utils.get_ap_stats("bytes_tx")
                expected_ssid_traffic = utils.caluclate_cust_dashboard_top5ssids_traffic_kbps(bytes_rx, bytes_tx)
                print "Expected Top 5 SSIDs traffic =  " +expected_ssid_traffic
                self.assertEqual(actual_ssid_traffic, expected_ssid_traffic, "Actual traffic of the Top 5 SSIDs is not same as Expected traffic!")
                break
            else:
                continue

        for i in range(0, 1):
            top5_ap_id = "top_ap_" + str(i)
    
            expected_ap_name = properties.ap_name
            actual_ap_name = driver.find_element_by_css_selector('#' + top5_ap_id + ' a').get_attribute('innerHTML').strip()
            print "Actual AP name = " +str(actual_ap_name) 
            print "Expected AP name = " +expected_ap_name
             
            if expected_ap_name == actual_ap_name:    
                actual_ap_traffic = driver.find_element_by_css_selector('#' + top5_ap_id + ' div.overviewTableTextSecondary').get_attribute('innerHTML')
                print "Actual Top 5 APs traffic = " +str(actual_ap_traffic)
                bytes_rx = utils.get_ap_stats("bytes_rx")
                bytes_tx = utils.get_ap_stats("bytes_tx")
                expected_ap_traffic = utils.caluclate_cust_dashboard_top5aps_traffic_kbps(bytes_rx, bytes_tx)
                print "Expected Top 5 APs traffic =  " +expected_ap_traffic
                self.assertEqual(actual_ap_traffic, expected_ap_traffic, "Actual traffic of the Top 5 APs is not same as Expected traffic!")
                break
            else:
                continue


    def tearDown(self):
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)


def test_generate_result():
    suite = unittest.TestSuite()
    suite.addTest(TestVerifyCustomerDashboard("verify_customer_dashboard"))
    print suite
    print __file__
    results.run(suite, __file__)
