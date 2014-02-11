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

def var_login():
#     self.driver = webdriver.Firefox()
#     self.driver.implicitly_wait(30)
#     self.base_url = properties.vm_url
#     self.verificationErrors = []
#     self.accept_next_alert = True
    columns = utils.get_var_details()
    driver = self.driver

    driver.get(self.base_url + "/home/login")
    driver.find_element_by_id("email").clear()
    driver.find_element_by_id("email").send_keys(columns['email'][0])
    driver.find_element_by_id("password").clear()
    driver.find_element_by_id("password").send_keys(columns['password'][0])
    driver.find_element_by_id("btnLogin").click()