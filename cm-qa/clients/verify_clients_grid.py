from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
import unittest
import time
import properties
from datetime import datetime
from dateutil import tz
from utils import utils, db, results


class TestVerifyClientsGrid(unittest.TestCase):
    """This class validates Clients grid.
    """
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.base_url = properties.vm_url
        self.verificationErrors = []
        self.accept_next_alert = True

    def _1_verify_clients_grid(self):
        """This test case validates all the information displays on clients grid.
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
        driver.find_element_by_id("menuClients").click()
        time.sleep(10)
        
        i = 0
        for option in driver.find_elements_by_css_selector("#clients_grid_table tbody tr"):
            #print option
            status_id = "Status_" + str(i)
            #print status_id
            description_id = "Description_" + str(i)
            #print description_id
            last_seen_id = "Last_Seen_" + str(i)
            #print last_seen_id
            usage_kbps_id = "Usage__Kbps_" + str(i)
            #print usage_kbps_id
            manufacturer_id = "Manufacturer_" + str(i)
            #print manufacturer_id
            mac_address_id = "MAC_Address_" + str(i)
            #print mac_address_id
            connected_to_id = "Connected_To_" + str(i)
            print connected_to_id
            recent_ssid_id = "Recent_SSID_" + str(i)
            #print recent_ssid_id
            first_seen_id = "First_Seen_" + str(i)
            #print first_seen_id
            wifi_band_id = "WiFi_band_" + str(i)
            client_os_id = "OS_" + str(i)
            client_ip_id = "IP_" + str(i)
            actual_client_name = driver.find_element_by_id(description_id).get_attribute('title')
            client_name = utils.get_client_name()
            expected_client_substr = client_name[-8:]
            print "Actual client name = " + str(actual_client_name) 
            print "Expected client should contain: " + expected_client_substr 
            #If the client matches then verify the clients grid for that client
            if expected_client_substr.lower() in actual_client_name:    
                try:
                    ####Checking for the actual client last seen whether it matches to expected client last seen.
                    last_seen = db.search_field_in_client_last_collection('last_seen', client_name)
                    #print first_seen
                    from_zone = tz.tzutc()
                    to_zone = tz.tzlocal()
                    utc_time = datetime.strptime(str(last_seen), '%Y-%m-%d %H:%M:%S')
                    #print utc_time
                    utc_time = utc_time.replace(tzinfo=from_zone)
                    local_time = utc_time.astimezone(to_zone)
                    expected_client_last_seen = local_time.strftime('%d.%m.%Y %H:%M:%S')
                    actual_client_last_seen = driver.find_element_by_id(last_seen_id).get_attribute('innerHTML')
                    print "Actual client last seen = " + actual_client_last_seen
                    print "Expected client last seen = " + expected_client_last_seen
                    self.assertEqual(actual_client_last_seen, expected_client_last_seen,
                              "Actual client last seen is not same as Expected client last seen!")
                except AssertionError as e: self.verificationErrors.append(str(e))
                try:
                    ####Checking for the actual status of client  whether it matches to expected staus.
                    actual_client_status = driver.find_element_by_css_selector('#' + status_id + ' img').get_attribute('title')
                    print "Actual status of client = " + actual_client_status
                    expected_client_status = 'connected'
                    print "Expected status of client = " + expected_client_status
                    self.assertEqual(actual_client_status, expected_client_status, "Client is in Disconnected status!")
                except AssertionError as e: self.verificationErrors.append(str(e))
                try:
                    #####Checking for the actual client description whether it matches to expected description.
                    expected_client_description = "Intel_Corporate-" + expected_client_substr
                    expected_client_description = expected_client_description.lower()
                    print "Actual client description = " + actual_client_name
                    print "Expected client description = " + expected_client_description
                    self.assertEqual(actual_client_name, expected_client_description,
                             "Actual client name is not same as Expected client name!")
                except AssertionError as e: self.verificationErrors.append(str(e))
                try:
                    #####Checking for the actual client usage kbps whether it matches to expected client usage.
                    actual_client_usage = driver.find_element_by_id(usage_kbps_id).get_attribute('innerHTML')
                    client_bytes_rx = utils.get_bytes_rx_client_stats()
                    client_bytes_tx = utils.get_bytes_tx_client_stats()
                    expected_client_usage = utils.caluclate_apdetails_page_client_usage_kbps(client_bytes_rx, client_bytes_tx)
                    print "Actual client usage = " + actual_client_usage
                    print "Expected client usage = " + str(expected_client_usage)
                    self.assertEqual(actual_client_usage, str(expected_client_usage),
                              "Actual client usage is not same as Expected client usage!")
                except AssertionError as e: self.verificationErrors.append(str(e))
                try:
                    #####Checking for the actual client manufacturer name whether it matches to expected client manufacturer name.
                    actual_client_manufacturer = driver.find_element_by_id(manufacturer_id).get_attribute('innerHTML')
                    expected_client_manufacturer = db.search_field_in_client_last_collection('manufacturer', client_name)
                    print "Actual client manufacturer = " + actual_client_manufacturer
                    print "Expected client manufacturer = " + expected_client_manufacturer
                    self.assertEqual(actual_client_manufacturer, expected_client_manufacturer,
                               "Actual client manufacturer is not same as Expected client manufacturer!")
                except AssertionError as e: self.verificationErrors.append(str(e))
                try:
                    #####Checking for the actual client MAC address whether it matches to expected client MAC address.
                    actual_client_mac = driver.find_element_by_id(mac_address_id).get_attribute('innerHTML')
                    expected_client_mac = client_name
                    print "Actual client MAC address = " + actual_client_mac
                    print "Expected client MAC address = " + expected_client_mac
                    self.assertEqual(actual_client_mac, expected_client_mac,
                               "Actual client MAC address is not same as Expected client MAC address!")
                except AssertionError as e: self.verificationErrors.append(str(e))   
                try:
                    #####Checking for actual ap name the client connected to whether it matches to expected ap name the client connected to.
                    actual_client_connectedto = driver.find_element_by_css_selector('#' + connected_to_id + ' a').get_attribute('innerHTML')
                    expected_client_connectedto = db.search_field_in_client_last_collection('ap_name', client_name)
                    print "Actual client connected to = " + actual_client_connectedto
                    print "Expected client connected to = " + expected_client_connectedto
                    self.assertEqual(actual_client_connectedto, expected_client_connectedto,
                               "Actual ap name the client connected to is not same as Expected ap name the client connected to!")
                except AssertionError as e: self.verificationErrors.append(str(e))
                try:
                    #####Checking for the actual client recent ssid whether it matches to expected client recent ssid.
                    actual_client_recent_ssid = driver.find_element_by_id(recent_ssid_id).get_attribute('innerHTML')
                    expected_client_recent_ssid = db.search_field_in_client_last_collection('ssid', client_name)
                    print "Actual client recent ssid = " + actual_client_recent_ssid
                    print "Expected client recent ssid = " + expected_client_recent_ssid
                    self.assertEqual(actual_client_recent_ssid, expected_client_recent_ssid,
                              "Actual client recent ssid is not same as Expected client recent ssid!")
                except AssertionError as e: self.verificationErrors.append(str(e))
                try:
                    ####Checking for the actual client first seen whether it matches to expected client first seen.
                    actual_client_first_seen = driver.find_element_by_id(first_seen_id).get_attribute('innerHTML')
                    first_seen = db.search_field_in_client_last_collection('first_seen', client_name)
                    #print first_seen
                    from_zone = tz.tzutc()
                    to_zone = tz.tzlocal()
                    utc_time = datetime.strptime(str(first_seen), '%Y-%m-%d %H:%M:%S')
                    #print utc_time
                    utc_time = utc_time.replace(tzinfo=from_zone)
                    local_time = utc_time.astimezone(to_zone)
                    expected_client_first_seen = local_time.strftime('%d.%m.%Y %H:%M:%S')
                    print "Actual client first seen = " + actual_client_first_seen
                    print "Expected client first seen = " + expected_client_first_seen
                    self.assertEqual(actual_client_first_seen, expected_client_first_seen,
                              "Actual client first seen is not same as Expected client first seen!")
                except AssertionError as e: self.verificationErrors.append(str(e))
                try:
                    #####Checking for the actual client WIFI band whether it matches to expected client WIFI band.
                    actual_client_wifi_band = driver.find_element_by_id(wifi_band_id).get_attribute('innerHTML')
                    expected_client_wifi_band = db.search_field_in_client_last_collection('radio', client_name)
                    print "Actual client WIFI band = " + actual_client_wifi_band
                    print "Expected client WIFI band = " + expected_client_wifi_band
                    self.assertEqual(actual_client_wifi_band, expected_client_wifi_band,
                              "Actual client WIFI band is not same as Expected client WIFI band!")
                except AssertionError as e: self.verificationErrors.append(str(e))
                try:
                    #####Checking for the actual client IP address whether it matches to expected client IP address.
                    actual_client_ip = driver.find_element_by_id(client_ip_id).get_attribute('innerHTML')
                    expected_client_ip = db.search_field_in_client_last_collection('ip', client_name)
                    print "Actual client IP address = " + actual_client_ip
                    print "Expected client IP address = " + expected_client_ip
                    self.assertEqual(actual_client_ip, expected_client_ip,
                              "Actual client IP address is not same as Expected client IP address!")
                except AssertionError as e: self.verificationErrors.append(str(e))
            i = i+1
#                 try:
#                     #####Checking for the actual client OS whether it matches to expected client OS.
#                     actual_client_os = driver.find_element_by_id(client_os_id).get_attribute('innerHTML')
#                     expected_client_os = db.search_field_in_client_last_collection('os', client_name)
#                     print "Actual client IP address = " + actual_client_os
#                     print "Expected client IP address = " + expected_client_os
#                     self.assertEqual(actual_client_os, expected_client_os,
#                               "Actual client OS is not same as Expected client OS!")
#                 except AssertionError as e: self.verificationErrors.append(str(e))
               
                    
        
    def tearDown(self):
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)    

        
#if __name__ == "__main__":
#    unittest.main()
def test_generate_result():    
    suite = unittest.TestSuite()
    suite.addTest(TestVerifyClientsGrid("_1_verify_clients_grid"))
    print suite
    print __file__
    results.run(suite, __file__)
