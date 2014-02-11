from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
import unittest
import time
import re
import os
from utils import utils, db, results
import properties


class TestValidateVarRegistration(unittest.TestCase):    
    """This class validates VAR registration form.
    """
    @classmethod
    def setUpClass(self):
        #display = Display(visible=0, size =(800,600))
        #display.start()
        global driver, columns
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.base_url = properties.vm_url
        self.accept_next_alert = True
        driver = self.driver
        columns = utils.get_var_details()

    def _1_validate_name_field(self):
        """This test case validates Business Name field.
        """
        driver.get(self.base_url + "/home/login")
        time.sleep(5)
        driver.find_element_by_id("SignUpLink").click()
        time.sleep(5)
        driver.find_element_by_id("name").clear()
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
        ###To check for the error message if VAR business name is not entered.###
        print"Verifying whether appropriate error message gets displayed if VAR business name is not entered."
        errors = driver.find_elements_by_xpath("//html/body/div[3]/div[2]/div/div/form/div/div[2]/label[2]")
        if errors != []:
            self.assertEqual("This field is required.", str(errors[0].get_attribute('innerHTML')),
                             "Error message is not appropriate.")
            print "Appropriate error message is displayed."
        
    def _2_validate_streetAddress_field(self):
        """This test case validates Street Address field.
        """
        ###To check for the error message if Street address is not entered.###
        driver.find_element_by_id("name").send_keys(columns['var_business_name'][0])
        driver.find_element_by_id("street_addr_line_1").clear()
        driver.find_element_by_id("street_addr_line_2").clear()
        driver.find_element_by_id("btnSignUp").click()
        print"Verifying whether appropriate error message gets displayed if Street address is not entered."
        errors = driver.find_elements_by_xpath("//html/body/div[3]/div[2]/div/div/form/div/div[3]/label[2]")
        if errors != []:
            self.assertEqual("This field is required.", str(errors[0].get_attribute('innerHTML')),
                             "Error message is not appropriate.")
            print "Appropriate error message is displayed."
            
    def _3_validate_city_field(self):
        """This test case validates City field.
        """
        ###To check for the error message if City is not entered.###
        driver.find_element_by_id("street_addr_line_1").send_keys(columns['street_addres_1'][0])
        driver.find_element_by_id("street_addr_line_2").send_keys(columns['street_addres_2'][0])
        driver.find_element_by_id("city").clear()
        driver.find_element_by_id("btnSignUp").click()
        print"Verifying whether appropriate error message gets displayed if City is not entered."
        errors = driver.find_elements_by_xpath("//html/body/div[3]/div[2]/div/div/form/div/div[4]/label[2]")
        if errors != []:
            self.assertEqual("This field is required.", str(errors[0].get_attribute('innerHTML')),
                             "Error message is not appropriate.")
            print "Appropriate error message is displayed."
        
    def _4_validate_zipCode_field(self):
        """This test case validates Zip code field.
        """
        ###To check for the error message if Zip code is not entered.###
        driver.find_element_by_id("city").send_keys(columns['city'][0])
        driver.find_element_by_id("zip_code").clear()
        driver.find_element_by_id("btnSignUp").click()
        print"Verifying whether appropriate error message gets displayed if Zip code is not entered."
        errors = driver.find_elements_by_xpath("//html/body/div[3]/div[2]/div/div/form/div/div[6]/label[2]")
        if errors != []:
            self.assertEqual("This field is required.", str(errors[0].get_attribute('innerHTML')),
                             "Error message is not appropriate.")
            print "Appropriate error message is displayed."
        
    def _5_validate_firstName_field(self):
        """This test case validates First Name field.
        """
        ###To check for the error message if First Name is not entered.###
        driver.find_element_by_id("zip_code").send_keys(columns['zip'][0])
        driver.find_element_by_id("first_name").clear()
        driver.find_element_by_id("btnSignUp").click()
        print"Verifying whether appropriate error message gets displayed if First Name is not entered."
        errors = driver.find_elements_by_xpath("//html/body/div[3]/div[2]/div/div/form/div[2]/div[2]/label[2]")
        if errors != []:
            self.assertEqual("This field is required.", str(errors[0].get_attribute('innerHTML')),
                             "Error message is not appropriate.")
            print "Appropriate error message is displayed."
        
    def _6_validate_lastName_field(self):
        """This test case validates Last Name field.
        """
        ###To check for the error message if Last Name is not entered.###
        driver.find_element_by_id("first_name").send_keys(columns['first_name'][0])
        driver.find_element_by_id("last_name").clear()
        driver.find_element_by_id("btnSignUp").click()
        print"Verifying whether appropriate error message gets displayed if Last Name is not entered."
        errors = driver.find_elements_by_xpath("//html/body/div[3]/div[2]/div/div/form/div[2]/div[3]/label[2]")
        if errors != []:
            self.assertEqual("This field is required.", str(errors[0].get_attribute('innerHTML')),
                             "Error message is not appropriate.")
            print "Appropriate error message is displayed."
        
    def _7_validate_email_field(self):
        """This test case validates Email field.
        """
        ###To check for the error message if Email address is not entered.###
        self.verificationErrors = []
        driver.find_element_by_id("last_name").send_keys(columns['last_name'][0])
        driver.find_element_by_id("email").clear()
        driver.find_element_by_id("btnSignUp").click()
        try:
            print"Verifying whether appropriate error message gets displayed if Email is not entered."
            errors = driver.find_elements_by_xpath("//html/body/div[3]/div[2]/div/div/form/div[2]/div[4]/label[2]")
            if errors != []:
                self.assertEqual("This field is required.", str(errors[0].get_attribute('innerHTML')),
                                 "Error message is not appropriate.")
                print "Appropriate error message is displayed."
        except AssertionError as e: self.verificationErrors.append(str(e))
        ###To check for the error message if invalid email address is entered.###
        ###Checking with test data jenny.alan,jenny.alan@,jenny.alan.com####
        print"Verifying whether appropriate error message gets displayed if invalid Email is entered."
        driver.find_element_by_id("email").send_keys("jenny.alan")
        driver.find_element_by_id("btnSignUp").click()
        try:
            print"Checking with test data 'jenny.alan'"
            errors = driver.find_elements_by_xpath("//html/body/div[3]/div[2]/div/div/form/div[2]/div[4]/label[2]")
            if errors != []:
                self.assertEqual("Please enter a valid email address.", str(errors[0].get_attribute('innerHTML')),
                                 "Error message is not appropriate.")
                print "Appropriate error message is displayed."
        except AssertionError as e: self.verificationErrors.append(str(e))
        driver.find_element_by_id("email").clear()
        driver.find_element_by_id("email").send_keys("jenny.alan@")
        driver.find_element_by_id("btnSignUp").click()
        try:
            print"Checking with test data 'jenny.alan@'"
            errors = driver.find_elements_by_xpath("//html/body/div[3]/div[2]/div/div/form/div[2]/div[4]/label[2]")
            if errors != []:
                self.assertEqual("Please enter a valid email address.", str(errors[0].get_attribute('innerHTML')),
                                 "Error message is not appropriate.")
                print "Appropriate error message is displayed."
        except AssertionError as e: self.verificationErrors.append(str(e))
        driver.find_element_by_id("email").clear()
        driver.find_element_by_id("email").send_keys("jenny.alan.com")
        driver.find_element_by_id("btnSignUp").click()
        try:
            print"Checking with test data 'jenny.alan.com'"
            errors = driver.find_elements_by_xpath("//html/body/div[3]/div[2]/div/div/form/div[2]/div[4]/label[2]")
            if errors != []:
                self.assertEqual("Please enter a valid email address.", str(errors[0].get_attribute('innerHTML')),
                                 "Error message is not appropriate.")
                print "Appropriate error message is displayed."
        except AssertionError as e: self.verificationErrors.append(str(e))
        self.assertEqual([], self.verificationErrors)
        
    def _8_validate_password_field(self):
        """This test case validates Password field.
        """
        ###To check for the error message if password is not entered.###
        self.verificationErrors = []
        driver.find_element_by_id("email").clear()
        driver.find_element_by_id("email").send_keys(columns['email'][0])
        driver.find_element_by_id("password").clear()
        driver.find_element_by_id("btnSignUp").click()
        try:
            print"Verifying whether appropriate error message gets displayed if password is not entered."
            errors = driver.find_elements_by_xpath("//html/body/div[3]/div[2]/div/div/form/div[2]/div[5]/label[2]")
            if errors != []:
                self.assertEqual("This field is required.", str(errors[0].get_attribute('innerHTML')),
                                 "Error message is not appropriate.")
                print "Appropriate error message is displayed."
        except AssertionError as e: self.verificationErrors.append(str(e))
        ###Check for the error message if less than 5 characters
        driver.find_element_by_id("password").send_keys("pass")
        driver.find_element_by_id("btnSignUp").click()
        try:
            print"Verifying whether appropriate error message gets displayed if the password less than 5 characters is entered."
            errors = driver.find_elements_by_xpath("//html/body/div[3]/div[2]/div/div/form/div[2]/div[5]/label[2]")
            if errors != []:
                self.assertEqual("Please enter at least 5 characters.", str(errors[0].get_attribute('innerHTML')),
                                 "Error message is not appropriate.")
                print "Appropriate error message is displayed."
        except AssertionError as e: self.verificationErrors.append(str(e))
        self.assertEqual([], self.verificationErrors)
        
    def _9_validate_confirmPassword_field(self):
        """This test case validates Confirm Password field.
        """
        ###To check for the error message if confirm password is not entered.##
        self.verificationErrors = []
        driver.find_element_by_id("password").clear()
        driver.find_element_by_id("password").send_keys(columns['password'][0])
        driver.find_element_by_id("confirm_password").clear()
        driver.find_element_by_id("btnSignUp").click()
        try:
            print"Verifying whether appropriate error message gets displayed if confirm password is not entered."
            errors = driver.find_elements_by_xpath("//html/body/div[3]/div[2]/div/div/form/div[2]/div[6]/label[2]")
            if errors != []:
                self.assertEqual("This field is required.", str(errors[0].get_attribute('innerHTML')),
                                 "Error message is not appropriate.")
                print "Appropriate error message is displayed."
        except AssertionError as e: self.verificationErrors.append(str(e))
        ###To check for the error message if confirm password is not matching with password.###
        driver.find_element_by_id("confirm_password").send_keys("welcome123")
        driver.find_element_by_id("btnSignUp").click()
        try:
            print"Verifying whether appropriate error message gets displayed if confirm password is not matching with password."
            errors = driver.find_elements_by_xpath("//html/body/div[3]/div[2]/div/div/form/div[2]/div[6]/label[2]")
            if errors != []:
                self.assertEqual("The value should match with password.", str(errors[0].get_attribute('innerHTML')),
                                 "Error message is not appropriate.")
                print "Appropriate error message is displayed."
        except AssertionError as e: self.verificationErrors.append(str(e))
        driver.find_element_by_id("confirm_password").clear()
        driver.find_element_by_id("confirm_password").send_keys(columns['confirm_password'][0])
        self.assertEqual([], self.verificationErrors)
        
    def _10_validate_country_field(self):
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
        print"Particular option is selcted and displayed in drop down" 
    
    def _11_validate_uploadLogo_field(self):
        """This test case validates Upload Logo field.
        """
        self.verificationErrors = []
        #Check whether file with .jpg extenstion uploads properly.
        parentdir = os.path.split(os.getcwd())
        image_file_path = os.path.join(parentdir[0], "test_data", "logo.jpg") 
        driver.find_element_by_name("logo").send_keys(image_file_path)
        print driver.find_element_by_name("logo").get_attribute("value")
        try:
            print"Verifying image file with .jpg extension is uploaded correctly."
            self.assertEqual(str(driver.find_element_by_name("logo").get_attribute("value")), "logo.jpg",
                             "File is not uploaded correctly.")
            print"Image file with .jpg extension is uploaded correctly."
        except AssertionError as e: self.verificationErrors.append(str(e))
        ##Check whether file with .jpeg extenstion uploads properly.
        image_file_path = os.path.join(parentdir[0], "test_data", "logo2.jpeg") 
        driver.find_element_by_name("logo").send_keys(image_file_path)
        try:
            print"Verifying image file with .jepg extension is uploaded correctly."
            self.assertEqual(str(driver.find_element_by_name("logo").get_attribute("value")), "logo2.jpeg",
                             "File is not uploaded correctly.")
            print"Image file with .jpeg extension is uploaded correctly."
        except AssertionError as e: self.verificationErrors.append(str(e))
        ##Check whether file with .png extenstion uploads properly.
        image_file_path = os.path.join(parentdir[0], "test_data", "logo1.png") 
        driver.find_element_by_name("logo").send_keys(image_file_path)
        try:
            print"Verifying image file with .png extension is uploaded correctly."
            self.assertEqual(str(driver.find_element_by_name("logo").get_attribute("value")), "logo1.png",
                             "File is not uploaded correctly.")
            print"Image file with .png extension is uploaded correctly."
        except AssertionError as e: self.verificationErrors.append(str(e))
        #Check whether file with invalid extension(.bmp) doesn't upload.
        image_file_path = os.path.join(parentdir[0], "test_data", "logo4.bmp") 
        driver.find_element_by_name("logo").send_keys(image_file_path)
        driver.find_element_by_id("btnSignUp").click()
        try:
            print"Verifying error messgae if image file with invalid extension(.bmp) is uploaded."
            self.assertEqual(str(driver.find_element_by_xpath(
                  "/html/body/div[3]/div[2]/div/div/form/div/div[8]/label[2]").get_attribute("innerHTML")), 
                               "Please enter a value with a valid extension.",
                               "File with .bmp extension is uploaded.")
            print"Image file with .bmp extension is not uploaded."
        except AssertionError as e: self.verificationErrors.append(str(e))
#         ##Check for the error messgae if the image file more than 1 MB is uploaded.
#         image_file_path = os.path.join(parentdir[0], "test_data", "logo5.jpg") 
#         driver.find_element_by_name("logo").click()
#         app = application.Application()
#         app.connect_(title_re = "File Upload")
#         app.file_upload.TypeKeys(image_file_path)
#         app.file_upload.Open.Click()
#         driver.find_element_by_id("btnSignUp").click()
#         try:
#             print"Verifying error messgae if image file of size more than 1 MB is uploaded."
#             self.assertEqual(str(driver.find_element_by_xpath(
#                 "/html/body/div[3]/div[2]/div/div/form/div/div[8]/label[2]").get_attribute("innerHTML")), 
#                 "Please enter a value with a valid extension.", "File with .bmp extension is uploaded.")
#             print"Image file with .bmp extension is not uploaded."
#         except AssertionError as e: self.verificationErrors.append(str(e))
        driver.find_element_by_name("logo").send_keys("")
        self.assertEqual([], self.verificationErrors)
        
    def _12_validate_VARName_for_duplication(self):
        """This test case validates VAR Name for duplication.
        """
        ##Verifying whether VAR registration fails if VAR business name already exists.
        driver.find_element_by_id("name").clear()
        driver.find_element_by_id("name").send_keys(columns['var_business_name'][0])
        driver.find_element_by_id("email").clear()
        driver.find_element_by_id("email").send_keys("tata@acceleramb.com")
        driver.find_element_by_id("btnSignUp").click()
        print"Verifying error message if trying to create a VAR user which already exists."
        time.sleep(5)
        self.assertEqual(str(driver.find_element_by_id("errorMessageBox").get_attribute("innerHTML")), 
                        "SignUp Failed. Reason: 'VAR Name already exists.'", 
                        "Error message is not displayed.")
        print"Appropriate error message is displayed."
    
###This function is commented as there is a bug reported for this verification point
#    def _13_validate_customerEmail_for_duplication(self):
#         ##Verifying whether VAR registration fails if email address already exists.
#         driver.find_element_by_id("name").clear()
#         driver.find_element_by_id("name").send_keys("Tata Communications1")
#         driver.find_element_by_id("email").clear()
#         driver.find_element_by_id("email").send_keys(columns['email'][0])
#         driver.find_element_by_id("btnSignUp").click()
#         try:
#             print"Verifying error messgae if trying to create a VAR user with email address which already exists."
#             self.assertEqual(str(driver.find_element_by_id("errorMessageBox").get_attribute("innerHTML")), 
#                               "SignUp Failed. Reason: 'VAR Name already exists.'", 
#                               "Error message is not displayed.")
#             print"Appropriate error message is displayed."
#         except AssertionError as e: self.verificationErrors.append(str(e))


    @classmethod    
    def tearDownClass(self):
        self.driver.quit()

 
#if __name__ == "__main__":
#    unittest.main()
def test_generate_result():    
    suite = unittest.TestSuite()
    suite.addTest(TestValidateVarRegistration("_1_validate_name_field"))
    suite.addTest(TestValidateVarRegistration("_2_validate_streetAddress_field"))
    suite.addTest(TestValidateVarRegistration("_3_validate_city_field"))
    suite.addTest(TestValidateVarRegistration("_4_validate_zipCode_field"))
    suite.addTest(TestValidateVarRegistration("_5_validate_firstName_field"))
    suite.addTest(TestValidateVarRegistration("_6_validate_lastName_field"))
    suite.addTest(TestValidateVarRegistration("_7_validate_email_field"))
    suite.addTest(TestValidateVarRegistration("_8_validate_password_field"))
    suite.addTest(TestValidateVarRegistration("_9_validate_confirmPassword_field"))
    suite.addTest(TestValidateVarRegistration("_10_validate_country_field"))
    suite.addTest(TestValidateVarRegistration("_11_validate_uploadLogo_field"))
    suite.addTest(TestValidateVarRegistration("_12_validate_VARName_for_duplication"))
    #suite.addTest(TestValidateVarRegistration("_13_validate_customerEmail_for_duplication"))
    print suite
    print __file__
    results.run(suite, __file__)    
    
