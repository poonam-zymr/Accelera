from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
import unittest
import time
import paramiko
import properties
from utils import utils, db, results, seleutils
from registration import create_config

class TestVerifyApplyTemplate(unittest.TestCase):
    """This class verifies data displays on Apply Template form.
    """
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.base_url = properties.vm_url
        self.verificationErrors = []
        self.accept_next_alert = True

    def _1_verify_apply_template_form(self):
        """This test case verifies fields and the data on Apply Template form
        """
        
        columns = utils.get_var_details()
        driver = self.driver
        driver.get(self.base_url + "/home/login")
        driver.find_element_by_id("email").clear()
        driver.find_element_by_id("email").send_keys(columns['email'][1])
        driver.find_element_by_id("password").clear()
        driver.find_element_by_id("password").send_keys(columns['password'][1])
        driver.find_element_by_id("btnLogin").click()
        time.sleep(10)
        
        driver.find_element_by_id("menuAccessPoints").click()
        time.sleep(5)
        
        i = 0
        for option in driver.find_elements_by_css_selector("#ap_grid_table tbody tr"):
            client_name_id = "AP_Name_" + str(i)
            select_checkbox_id = "_" + str(i)
            if properties.ap_name == str(driver.find_element_by_css_selector("#" + client_name_id + " a").get_attribute('innerHTML')):
                print "pass"
                driver.find_element_by_css_selector("#" + select_checkbox_id + " div").click()
                time.sleep(5)
                driver.find_element_by_id("applyTemplateBtn").click()
                time.sleep(3)
                
                ###Verifying the Selected APs table contents.
                j = 0
                for option1 in driver.find_elements_by_css_selector("#selected_ap_list_table tbody tr"):
                    selectedap_name_id = "AP_Name_" + str(j)
                    location_id = "Location_" + str(j)
                    actual_selected_ap_name = driver.find_element_by_id(selectedap_name_id).get_attribute('innerHTML')
                    expected_selected_ap_name = properties.ap_name
                    print "Actual selected AP name = " + actual_selected_ap_name
                    print "Expected selected AP name = " + expected_selected_ap_name
                    try:
                        self.assertEqual(actual_selected_ap_name, expected_selected_ap_name,
                                "Actual selected AP name is not same as Expected selected AP name!")
                    except AssertionError as e: self.verificationErrors.append(str(e))
                    
                    actual_selected_ap_location = driver.find_element_by_id(location_id).get_attribute('innerHTML')
                    expected_selected_ap_location = columns['var_business_name'][2]
                    print "Actual selected AP's location name = " + actual_selected_ap_location
                    print "Expected selected AP's location name = " + expected_selected_ap_location
                    try:
                        self.assertEqual(actual_selected_ap_name, expected_selected_ap_name,
                                "Actual selected AP's location name is not same as Expected selected AP's location name!")
                    except AssertionError as e: self.verificationErrors.append(str(e))
                
                ###Verifying the Selected AP's available templates table contents.    
                j = 0
                for option2 in driver.find_elements_by_css_selector("#config_list_table tbody tr"):
                    template_name_id = "Template_name_" + str(j)
                    ssid_id = "SSID_" + str(j)
                    actual_template_name = driver.find_element_by_id(template_name_id).get_attribute('innerHTML')
                    expected_template_name = properties.config_name
                    print "Actual template name = " + actual_template_name
                    print "Expected template name = " + expected_template_name
                    try:
                        self.assertEqual(actual_template_name, expected_template_name,
                                "Actual template name is not same as Expected template name!")
                    except AssertionError as e: self.verificationErrors.append(str(e))
                    
                    actual_ssid_name = driver.find_element_by_id(ssid_id).get_attribute('innerHTML')
                    expected_ssid_name = properties.config_name
                    print "Actual template's SSID name = " + actual_ssid_name
                    print "Expected template's SSID name = " + expected_ssid_name
                    try:
                        self.assertEqual(actual_ssid_name, expected_ssid_name,
                                "Actual template's SSID name is not same as Expected Expected template's SSID name!")
                    except AssertionError as e: self.verificationErrors.append(str(e))    
                
    
    def tearDown(self):
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)    

        
#if __name__ == "__main__":
#    unittest.main()
def test_generate_result():
    suite = unittest.TestSuite()
    suite.addTest(TestVerifyApplyTemplate("_1_verify_apply_template_form"))
    print suite
    print __file__
    results.run(suite, __file__)
