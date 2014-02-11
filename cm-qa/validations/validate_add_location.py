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


class TestValidateAddLocation(unittest.TestCase):
    """This class validates Add Location form.
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

    def _1_validate_name_field(self):
        """This test case validates Location Name field.
        """
        driver.get(self.base_url + "/home/login")
        driver.find_element_by_id("email").clear()
        driver.find_element_by_id("email").send_keys(columns['email'][1])
        driver.find_element_by_id("password").clear()
        driver.find_element_by_id("password").send_keys(columns['password'][1])
        driver.find_element_by_id("btnLogin").click()
        time.sleep(10)
        
        driver.find_element_by_id("btnAddLocation").click()
        #time.sleep(5)
        driver.find_element_by_id("name").clear()
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
        driver.find_element_by_id("btnAddLocation").click()
        ######To check for the error message if Location name is not entered.###
        print"Verifying whether appropriate error message gets displayed if location name is not entered."
        errors = driver.find_elements_by_xpath("//html/body/div[3]/div[3]/div/div/div/form/div/div/label[2]")
        if errors != []:
            self.assertEqual("This field is required.", str(errors[0].get_attribute('innerHTML')),
                             "Error message is not appropriate.")
            print "Appropriate error message is displayed."
    
    def _2_validate_streetAddress_field(self):
        """This test case validates Street Address field.
        """
        ######To check for the error message if street address is not entered.###
        driver.find_element_by_id("name").send_keys(columns['var_business_name'][2])
        driver.find_element_by_id("street_addr_line_1").clear()
        driver.find_element_by_id("street_addr_line_2").clear()
        driver.find_element_by_id("btnAddLocation").click()
        print"Verifying whether appropriate error message gets displayed if street address is not entered."
        errors = driver.find_elements_by_xpath("//html/body/div[3]/div[3]/div/div/div/form/div/div[2]/label[2]")
        if errors != []:
            self.assertEqual("This field is required.", str(errors[0].get_attribute('innerHTML')),
                             "Error message is not appropriate.")
            print "Appropriate error message is displayed."
             
    def _3_validate_city_field(self):
        """This test case validates City field.
        """
        ######To check for the error message if city is not entered.###
        driver.find_element_by_id("street_addr_line_1").send_keys(columns['street_addres_1'][2])
        driver.find_element_by_id("street_addr_line_2").send_keys(columns['street_addres_2'][2])
        driver.find_element_by_id("city").clear()
        driver.find_element_by_id("btnAddLocation").click()
        print"Verifying whether appropriate error message gets displayed if city is not entered."
        errors = driver.find_elements_by_xpath("//html/body/div[3]/div[3]/div/div/div/form/div/div[3]/label[2]")
        if errors != []:
            self.assertEqual("This field is required.", str(errors[0].get_attribute('innerHTML')),
                             "Error message is not appropriate.")
            print "Appropriate error message is displayed."
            
    def _4_validate_zipCode_field(self):
        """This test case validates Zip code field.
        """
        ######To check for the error message if zip code is not entered.###
        driver.find_element_by_id("city").send_keys(columns['city'][2])
        driver.find_element_by_id("zip_code").clear()
        driver.find_element_by_id("btnAddLocation").click()
        print"Verifying whether appropriate error message gets displayed if zip code is not entered."
        errors = driver.find_elements_by_xpath("//html/body/div[3]/div[3]/div/div/div/form/div[2]/div[2]/label[2]")
        if errors != []:
            self.assertEqual("This field is required.", str(errors[0].get_attribute('innerHTML')),
                             "Error message is not appropriate.")
            print "Appropriate error message is displayed." 
    
    def _5_validate_configuration_field(self):
        """This test case validates config template field.
        """
        ######To check for the error message if config template is not selected.###
        driver.find_element_by_id("zip_code").send_keys(columns['zip'][2])
        driver.find_element_by_id("btnAddLocation").click()
        print"Verifying whether appropriate error message gets displayed if config template is not selected."
        errors = driver.find_elements_by_xpath("//html/body/div[3]/div[3]/div/div/div/form/div[2]/div[4]/label[2]/label")
        if errors != []:
            self.assertEqual("This field is required.", str(errors[0].get_attribute('innerHTML')),
                             "Error message is not appropriate.")
            print "Appropriate error message is displayed."
            
    def _6_validate_locationName_for_duplication(self):
        """This test case validates Location Name for duplication.
        """
        ##Verifying whether add location fails if location name already exists.
        config_dropdown = driver.find_element_by_id("config_id")
        for option in config_dropdown.find_elements_by_tag_name("option"):
            if option.text == columns['var_business_name'][2]:
                option.click()
                time.sleep(5)
        driver.find_element_by_id("name").clear()
        driver.find_element_by_id("name").send_keys(columns['var_business_name'][2])
        driver.find_element_by_id("btnAddLocation").click()
        print"Verifying error message if trying to create a location which already exists."
        time.sleep(5)
        self.assertEqual(str(driver.find_element_by_id("errorMessageBox").get_attribute("innerHTML")), 
                        "Location Name already exists.", 
                        "Error message is not displayed.")
        print"Appropriate error message is displayed."
        
    def _7_validate_geocode(self):
        """This test case validates whether the geocode is correct.
        """
        ######To check for the error message if the gocode is not valid.###
        driver.find_element_by_id("name").clear()
        location_name = columns['var_business_name'][2] + "_1"
        driver.find_element_by_id("name").send_keys(location_name)
        driver.find_element_by_id("zip_code").clear()
        driver.find_element_by_id("state").clear()
        driver.find_element_by_id("city").clear()
        driver.find_element_by_id("city").send_keys("Mumbai")
        driver.find_element_by_id("zip_code").send_keys("411051")
        driver.find_element_by_id("btnAddLocation").click()
        time.sleep(5)
        print"Verifying whether appropriate error message gets displayed if geocode is invalid."
        errors = driver.find_elements_by_id("errorMessageBox")
        if errors != []:
            self.assertEqual("Invalid ZIP/Postal Code.", str(errors[0].get_attribute('innerHTML')),
                             "Error message is not appropriate.")
            print "Appropriate error message is displayed."
    
    def _8_validate_country_field(self):
        """This test case validates country field.
        """
        ##Check if selecting any option from country drop down that option gets selected and displayed in drop down.
        country_dropdown = driver.find_element_by_name("country")
        for option in country_dropdown.find_elements_by_tag_name("option"):
            if option.text == "India":
                option.click()
                time.sleep(5)
        print"Verifying whether particular option is selected and displayed in country drop down."
        self.assertEqual(str(country_dropdown.get_attribute("value")), "India", "Option is not selected properly.")
        print"Particular option is selected and displayed in drop down"   
        
    @classmethod    
    def tearDownClass(self):
        self.driver.quit()
 
#if __name__ == "__main__":
#    unittest.main()
def test_generate_result():    
    suite = unittest.TestSuite()
    suite.addTest(TestValidateAddLocation("_1_validate_name_field"))
    suite.addTest(TestValidateAddLocation("_2_validate_streetAddress_field"))
    suite.addTest(TestValidateAddLocation("_3_validate_city_field"))
    suite.addTest(TestValidateAddLocation("_4_validate_zipCode_field"))
    suite.addTest(TestValidateAddLocation("_5_validate_configuration_field"))
    suite.addTest(TestValidateAddLocation("_6_validate_locationName_for_duplication"))
    suite.addTest(TestValidateAddLocation("_7_validate_geocode"))
    suite.addTest(TestValidateAddLocation("_8_validate_country_field"))
    print suite
    print __file__
    results.run(suite, __file__)
