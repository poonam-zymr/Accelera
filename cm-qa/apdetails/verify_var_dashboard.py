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


class TestVerifyVARDashboard(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.base_url = properties.vm_url
        self.verificationErrors = []
        self.accept_next_alert = True

    def verify_var_dashboard(self):
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
        def get_text_excluding_children(driver, element):     
            return driver.execute_script("""     return jQuery(arguments[0]).contents().filter(function() {         return this.nodeType == Node.TEXT_NODE;     }).text();     """, element)
            #cust = get_text_excluding_children(driver, driver.find_element_by_css_selector("#cust_name_0"))
        
        for i in range (0, 10):
            cust_id = "#cust_name_" + str(i)
            #print cust_id
            cust = get_text_excluding_children(driver, driver.find_element_by_css_selector(cust_id))
            cust = cust.strip()
            print cust
            if cust == columns['var_business_name'][1]:
                print "VAR dashboard details for the customer: " +cust 
                location_id = "#location_" + str(i) + " h4"
                no_of_location = driver.find_element_by_css_selector(location_id).get_attribute("innerHTML").strip()
                print "No. of Locations = " +no_of_location   
                exp_no_of_locs = 1
                self.assertEqual(str(no_of_location), str(exp_no_of_locs), "No. of Location present under the customer are not as expected!")
                
                ap_up_id = "#ap_" + str(i) + " h4"     
                no_of_aps_up = driver.find_element_by_css_selector(ap_up_id).get_attribute("innerHTML").strip()
                exp_no_of_aps_up = 1
                print "No. of AP's that are Up = " +no_of_aps_up
                self.assertEqual(str(no_of_aps_up), str(exp_no_of_aps_up), "APs that are UP don't match the expected APs!")

                ap_down_id = "#apDown_" + str(i) + " h4"    
                no_of_aps_down = driver.find_element_by_css_selector(ap_down_id).get_attribute("innerHTML").strip()
                exp_no_of_aps_down = 0
                print "No. of AP's that are Down = " +no_of_aps_down
                self.assertEqual(str(no_of_aps_down), str(exp_no_of_aps_down), "APs that are down don't match the expected APs!")

                try:
                    informative_event_id = "#Informative_" + str(i) + " span.eventCountBox"    
                    no_of_info_events = driver.find_element_by_css_selector(informative_event_id).get_attribute("innerHTML").strip()
                    print "No. of Informative Events = " +no_of_info_events
                except NoSuchElementException:
                    print "0 Informative Events!"
                try:
                    critical_event_id = "#Critical_" + str(i) + " span.eventCountBox"   
                    no_of_critical_events = driver.find_element_by_css_selector(critical_event_id).get_attribute("innerHTML").strip()
                    print "No. of Critical Events = " +no_of_critical_events
                except NoSuchElementException:
                    print "0 Critical Events!"
                try:
                    important_event_id = "#Important_" + str(i) + " span.eventCountBox"
                    no_of_imp_events = driver.find_element_by_css_selector(important_event_id).get_attribute("innerHTML").strip()
                    print "No. of Important Events = " +no_of_imp_events
                except NoSuchElementException:
                    print "0 Important Events!"
                break
            else:
                continue
        
    def tearDown(self):
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)

def test_generate_result():
    suite = unittest.TestSuite()
    suite.addTest(TestVerifyVARDashboard("verify_var_dashboard"))
    print suite
    print __file__
    results.run(suite, __file__)
