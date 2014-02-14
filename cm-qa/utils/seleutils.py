from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
import unittest
import time
import re
import properties
import utils, db

def create_config(config_name):
    columns = utils.get_var_details()
    driver = webdriver.Firefox()
    driver.implicitly_wait(30)
    base_url = properties.vm_url
    verificationErrors = []
    accept_next_alert = True 
    driver.get(base_url + "/home/login")
    driver.find_element_by_id("email").clear()
    driver.find_element_by_id("email").send_keys(columns['email'][1])
    driver.find_element_by_id("password").clear()
    driver.find_element_by_id("password").send_keys(columns['password'][1])
    driver.find_element_by_id("btnLogin").click()
    time.sleep(10)
        #print "Clickin Customers dropdown"
        #dropdown = driver.find_element_by_id("customerFilter")
        #for option in dropdown.find_elements_by_tag_name("option"):
        #    if option.text == columns['var_business_name'][1]:
        #        option.click()
        #        time.sleep(5)

    driver.find_element_by_id("menuConfigurations").click()
    driver.find_element_by_id("btnAddTemplate").click()
    time.sleep(5)
    driver.find_element_by_id("config_name").clear()
    driver.find_element_by_id("config_name").send_keys(config_name)
    driver.find_element_by_id("network_header").click()
    driver.find_element_by_id("ssid_0").clear()
    driver.find_element_by_id("ssid_0").send_keys(config_name)
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
    db.search_config_in_configuration_collection(config_name)
    driver.quit()
