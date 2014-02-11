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


class TestValidateAddTemplate(unittest.TestCase):
    """This class validates Add Template form for error messages.
    """
    @classmethod
    def setUpClass(self):
        global driver, columns
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.base_url = properties.vm_url
        self.accept_next_alert = True
        driver = self.driver
        columns = utils.get_var_details()

    def _1_validate_template_name_for_duplication(self):
        """This test case validates Template name field for duplication.
        """
        driver.get(self.base_url + "/home/login")
        driver.find_element_by_id("email").clear()
        driver.find_element_by_id("email").send_keys(columns['email'][1])
        driver.find_element_by_id("password").clear()
        driver.find_element_by_id("password").send_keys(columns['password'][1])
        driver.find_element_by_id("btnLogin").click()
        time.sleep(10)
        driver.find_element_by_id("menuConfigurations").click()
        driver.find_element_by_id("btnAddTemplate").click()
        time.sleep(5)
        driver.find_element_by_id("config_name").clear()
        driver.find_element_by_id("config_name").send_keys(columns['var_business_name'][2])
        driver.find_element_by_id("network_header").click()
        driver.find_element_by_id("ssid_0").clear()
        driver.find_element_by_id("ssid_0").send_keys("SSID_1")
        time.sleep(5)
        print "Clicking passphrase type dropdwon"
        passphrase_dropdown = driver.find_element_by_id("security_0")
        for option in passphrase_dropdown.find_elements_by_tag_name("option"):
            if option.get_attribute('value') == "wpa-psk":
                option.click()
                time.sleep(5)

        driver.find_element_by_id("passphrase_0").clear()
        driver.find_element_by_id("passphrase_0").send_keys("accelera")
        driver.find_element_by_id("submitButton").click()
        time.sleep(3)
        ### Checking for error message while trying to create the config which already exists.
        actual_error_message = driver.find_element_by_id("errorMessage").get_attribute("innerHTML")
        expected_error_message = "Template Name already exists."
        print "Actual error message = " + actual_error_message
        print "Expected error message = " + expected_error_message
        self.assertEqual(actual_error_message, expected_error_message,
                            "Actual error message not matching with the expected error message.!")
        print 'Appropriate error message "%s" is displayed' %  expected_error_message

        
    def _2_validate_ssid_name_for_duplication(self):
        """This test case validates SSID field for duplication.
        """
        self.verificationErrors = []
        ### setting prerequisites for next test case.
        driver.find_element_by_id("system_header").click()
        
        driver.find_element_by_id("config_name").clear()
        template_name = columns['var_business_name'][2] + "_1"
        driver.find_element_by_id("config_name").send_keys(template_name)
        driver.find_element_by_id("network_header").click()
        for i in range(0, 2):
            driver.find_element_by_id("ssid_" + str(i)).clear()
            driver.find_element_by_id("ssid_" + str(i)).send_keys("SSID")
            #time.sleep(5)
            print "Clicking passphrase type dropdwon"
            passphrase_dropdown = driver.find_element_by_id("security_" + str(i))
            for option in passphrase_dropdown.find_elements_by_tag_name("option"):
                if option.get_attribute('value') == "wpa-psk":
                    option.click()
                    time.sleep(5)

            driver.find_element_by_id("passphrase_" + str(i)).clear()
            driver.find_element_by_id("passphrase_" + str(i)).send_keys("accelera")
        print "Checking for the error message when SSID are duplicate."
        ###Checking for the error message comes up on UI side when duplicate SSID's are entered.
        actual_error_message = driver.find_element_by_xpath(
            "//html/body/div[2]/div/div/div/div/div/form/div/div[4]/fieldset/table/tbody/tr[2]/td/label"
            ).get_attribute("innerHTML")
        expected_error_message = "Must be Unique."
        print "Actual error message = " + actual_error_message
        print "Expected error message = " + expected_error_message
        try:
            self.assertEqual(actual_error_message, expected_error_message,
                "Actual error message not matching with the expected error message.!")
        except AssertionError as e: self.verificationErrors.append(str(e))
        print 'Appropriate error message "%s" is displayed' %  expected_error_message
        ###checking for error message comes up from backend API when duplicate SSID's are entered and clicking on
        ###Submit button. 
        driver.find_element_by_id("submitButton").click()
        time.sleep(3)
        result = False
        actual_error_message = driver.find_element_by_id("errorMessage").get_attribute("innerHTML")
        for j in range(0, 2):
            expected_error_message = ("ssid %s: Must be Unique." % str(j+1))
            print "Expected error message = " + expected_error_message
            if expected_error_message in actual_error_message:
                result = True
            else:
                result = False
        try:
            self.assertEqual(result, True,
                "Actual error message not matching with the expected error message.!")
        except AssertionError as e: self.verificationErrors.append(str(e))
        self.assertEqual([], self.verificationErrors)
        print 'Appropriate error message is displayed.'

    def _3_validate_ssid_name_for_spaces(self):
        """This test case validates SSID field for spaces.
        """
        ### setting prerequisites for next test case.
        for i in range(0, 2):
            driver.find_element_by_id("ssid_" + str(i)).clear()
            driver.find_element_by_id("passphrase_" + str(i)).clear()
            
        driver.find_element_by_id("ssid_0").send_keys("SSID 1")
        actual_error_message = driver.find_element_by_xpath(
            "//html/body/div[2]/div/div/div/div/div/form/div/div[4]/fieldset/table/tbody/tr[1]/td/label"
            ).get_attribute("innerHTML")
        expected_error_message = "Spaces not allowed."
        print "Actual error message = " + actual_error_message
        print "Expected error message = " + expected_error_message
        self.assertEqual(actual_error_message, expected_error_message,
                            "Actual error message not matching with the expected error message.!")
        print 'Appropriate error message "%s" is displayed' %  expected_error_message
        
    def _4_validate_passphrase_for_lessthan8_characters(self):
        """This test case validates passphrase field for less than 8 characters.
        """
        self.verificationErrors = []
        driver.find_element_by_id("ssid_0").clear()
        driver.find_element_by_id("ssid_0").send_keys("SSID")
        print "Clicking passphrase type dropdwon"
        passphrase_dropdown = driver.find_element_by_id("security_0")
        for option in passphrase_dropdown.find_elements_by_tag_name("option"):
            if option.get_attribute('value') == "wpa-psk":
                option.click()
                time.sleep(5)
        driver.find_element_by_id("passphrase_0").clear()
        driver.find_element_by_id("passphrase_0").send_keys("welcome")
        driver.find_element_by_id("ssid_1").send_keys("SSID2")
        print "Checking for the error message when passphrase is less than 8 characters."
        ###Checking for the error message comes up on UI side when passphrase less than 8 characters is entered.
        time.sleep(10)
        actual_error_message = driver.find_element_by_xpath(
            "//html/body/div[2]/div/div/div/div/div/form/div/div[4]/fieldset/table/tbody/tr/td[3]/label"
            ).get_attribute("innerHTML")
        expected_error_message = "Min. 8 chars"
        print "Actual error message = " + actual_error_message
        print "Expected error message = " + expected_error_message
        try:
            self.assertEqual(actual_error_message, expected_error_message,
                "Actual error message not matching with the expected error message.!")
        except AssertionError as e: self.verificationErrors.append(str(e))
        print 'Appropriate error message "%s" is displayed' %  expected_error_message
        ###checking for error message comes up from backend API when passphrase less than 8 characters is entered
        ### and clicking on Submit button. 
        driver.find_element_by_id("submitButton").click()
        time.sleep(3)
        actual_error_message = driver.find_element_by_id("errorMessage").get_attribute("innerHTML")
        expected_error_message = "passphrase 1: Minimum 8 characters are required."
        actual_error_message = actual_error_message.replace("<br>", "")
        print "Actual error message = " + actual_error_message
        print "Expected error message = " + expected_error_message
        try:
            self.assertEqual(actual_error_message, expected_error_message,
                            "Actual error message not matching with the expected error message.!")
        except AssertionError as e: self.verificationErrors.append(str(e))
        print 'Appropriate error message "%s" is displayed' %  expected_error_message
        self.assertEqual([], self.verificationErrors)
    
    @classmethod    
    def tearDownClass(self):
        self.driver.quit()
        #self.assertEqual([], self.verificationErrors)
 
#if __name__ == "__main__":
#    unittest.main()
def test_generate_result():    
    suite = unittest.TestSuite()
    suite.addTest(TestValidateAddTemplate("_1_validate_template_name_for_duplication"))
    suite.addTest(TestValidateAddTemplate("_2_validate_ssid_name_for_duplication"))
    suite.addTest(TestValidateAddTemplate("_3_validate_ssid_name_for_spaces"))
    suite.addTest(TestValidateAddTemplate("_4_validate_passphrase_for_lessthan8_characters"))
    print suite
    print __file__
    results.run(suite, __file__)
    
    