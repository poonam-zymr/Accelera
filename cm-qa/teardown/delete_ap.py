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
import paramiko
import os
import subprocess


class TestDeleteAP(unittest.TestCase):
    def setUp(self):
        utils.call_display_headless_browser()
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.base_url = properties.vm_url
        self.verificationErrors = []
        self.accept_next_alert = True

    def delete_ap(self):
        columns = utils.get_var_details()
        driver = self.driver
 
        driver.get(self.base_url + "/home/login")
        driver.find_element_by_id("email").clear()
        driver.find_element_by_id("email").send_keys(columns['email'][0])
        driver.find_element_by_id("password").clear()
        driver.find_element_by_id("password").send_keys(columns['password'][0])
        driver.find_element_by_id("btnLogin").click()
        time.sleep(10)
        print "Clickin Customers dropdown"
        dropdown = driver.find_element_by_id("customerFilter")
        for option in dropdown.find_elements_by_tag_name("option"):
            if option.text == columns['var_business_name'][1]:
                option.click()
                time.sleep(5)
                break
            else:
                continue
        driver.find_element_by_id("menuAccessPoints").click()
        time.sleep(5)
         
        i = 0
        for option in driver.find_elements_by_css_selector("#ap_grid_table tbody tr"):
            client_name_id = "AP_Name_" + str(i)
            select_checkbox_id = "_" + str(i)
            if properties.ap_name == str(driver.find_element_by_css_selector("#" + client_name_id + " a").get_attribute('innerHTML')):
                print "AP Name = " + str(driver.find_element_by_css_selector('#' + client_name_id + ' a').get_attribute('innerHTML'))
                driver.find_element_by_css_selector("#" + select_checkbox_id + " div").click()
                time.sleep(5)
                driver.find_element_by_id("deleteApBtn").click()
                time.sleep(5)
                alert_text = driver.find_element_by_id("dialog-confirm").get_attribute("innerHTML")
                dialog_header = driver.find_element_by_id("ui-id-1").get_attribute("innerHTML").strip()
                self.assertEqual(dialog_header, "Delete the selected APs", "Delete AP Confirmation dialog not present!")
                driver.find_element_by_xpath("(//button[@type='button'])[1]").click()
                print "AP " + properties.ap_name + " deleted successfully!"
                 
                #Verify if AP was deleted from ap collection
                db.verify_delete_ap(properties.ap_name)
                time.sleep(130)
                 
                ap_jid = utils.get_ap_jid(properties.real_ap_ip)
                ap_jid = ap_jid.strip()
                #Verify if AP was added to new_ap collection
                db.search_ap_in_new_ap_collection(ap_jid)
                time.sleep(2)
                 
                #Verify if radios are disabled on the AP
                ssh = paramiko.SSHClient()
                ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                ssh.connect(properties.real_ap_ip, username='root',
                    password='password')
                
                stdin, stdout, stderr = ssh.exec_command("uci show | grep disabled")
                data = stdout.readlines()
                for eachLine in data:
                    if "radio0" in eachLine:
                            radio_line = eachLine.split("\n")
                            radio_state = radio_line[0]
                            print "Actual Radio0 state is: " + radio_state
                            expected_radio_state = "wireless.radio" + "0" + ".disabled=1"
                            print "Expected radio state is: " + expected_radio_state 
                            self.assertEqual(radio_state.strip(), expected_radio_state, "After deleting AP Radio0 was not disabled")

                for eachLine in data:
                    if "radio1" in eachLine:
                            radio_line = eachLine.split("\n")
                            radio_state = radio_line[0]
                            print "Actual Radio1 state is:  " + radio_state
                            expected_radio_state = "wireless.radio" + "1" + ".disabled=1"
                            print "Expected radio state is: " + expected_radio_state
                            self.assertEqual(radio_state.strip(), expected_radio_state, "After deleting AP Radio1 was not disabled")
                break
            else:
                continue
            i = i+1

    def tearDown(self):
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)

def test_generate_result():
    suite = unittest.TestSuite()
    suite.addTest(TestDeleteAP("delete_ap"))
    print suite
    print __file__
    results.run(suite, __file__)
