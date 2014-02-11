from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
import time
import unittest
import properties
from utils import utils, results

class TestTeardown(unittest.TestCase):

    def reset_original_config_to_ap(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.base_url = properties.vm_url
        columns = utils.get_var_details()
        driver = self.driver
        driver.get(self.base_url + "/home/login")
        driver.find_element_by_id("email").clear()
        driver.find_element_by_id("email").send_keys(columns['email'][1])
        driver.find_element_by_id("password").clear()
        driver.find_element_by_id("password").send_keys(columns['password'][1])
        driver.find_element_by_id("btnLogin").click()
        time.sleep(10)
        driver.find_element_by_id("menuConfigurations").click()
        time.sleep(10)
        i = 0
        for option in driver.find_elements_by_css_selector("#config_grid_table tbody tr"):
            template_name_id = "Template_Name_" + str(i)
            edit_button_id = "Edit_" + str(i)
            template_name = driver.find_element_by_id(template_name_id).get_attribute('innerHTML')
            if template_name == columns['var_business_name'][2]:
                driver.find_element_by_css_selector("#" + edit_button_id + " img").click() 
                    #driver.find_element_by_id("btnAddTemplate").click()
                time.sleep(5)
                driver.find_element_by_id("config_name").clear()
                driver.find_element_by_id("config_name").send_keys(columns['var_business_name'][2])
                driver.find_element_by_id("radio_header").click()
                Select(driver.find_element_by_name("radio_50g_status")).select_by_visible_text("On")
                driver.find_element_by_id("network_header").click()
                driver.find_element_by_id("ssid_1").clear()
                driver.find_element_by_id("submitButton").click()
        driver.quit()   
                    
def test_generate_result():
    suite = unittest.TestSuite()
    suite.addTest(TestTeardown("reset_original_config_to_ap"))
    print suite
    print __file__
    results.run(suite, __file__)              
