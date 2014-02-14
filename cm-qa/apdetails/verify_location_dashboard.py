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


class TestVerifyLocationDashboard(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.base_url = properties.vm_url
        self.verificationErrors = []
        self.accept_next_alert = True


    def verify_location_dashboard(self):
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
        print "Clickin Customers dropdown"
        dropdown = driver.find_element_by_id("customerFilter")
        for option in dropdown.find_elements_by_tag_name("option"):
            if option.text == columns['var_business_name'][1]:
                option.click()
                time.sleep(5)
        print "Clickin Location dropdown"
        dropdown = driver.find_element_by_id("locationFilter")
        for option in dropdown.find_elements_by_tag_name("option"):
            if option.text == columns['var_business_name'][2]:
                option.click()
                time.sleep(5)
          
        #Verify client count in the client widget
        client_widget = driver.find_element_by_id("client_count_value")
        actual_no_of_clients = client_widget.get_attribute('innerHTML')
        print "Actual no. of clients = " +str(actual_no_of_clients)
        expected_no_of_clients = utils.get_client_count()
        print "Expected no. of clients = " +str(expected_no_of_clients)
        self.assertEqual(actual_no_of_clients, expected_no_of_clients, "Actual no. of clients are not same as expected no. of clients!")
          
        #Verify AP traffic in the traffic guage chart 
        traffic_widget = driver.find_element_by_id("traffic_value")
        actual_ap_traffic = traffic_widget.get_attribute('innerHTML')
        print "Actual AP traffic = " +str(actual_ap_traffic)
        ap_bytes_rx = utils.get_ap_stats("bytes_rx")
        ap_bytes_tx = utils.get_ap_stats("bytes_tx")
        expected_ap_traffic_mbps = utils.caluclate_loc_dashboard_traffic_mbps(ap_bytes_rx, ap_bytes_tx)
        print "Expected AP traffic = " +expected_ap_traffic_mbps
        self.assertEqual(actual_ap_traffic, expected_ap_traffic_mbps, "Actual AP traffic is not same as Expected AP traffic!")
           
        #Verify 2.4G radio chan utilization in the guage chart
        chan_widget_24g = driver.find_element_by_id("utilization24G")
        chan_uti_24g = chan_widget_24g.get_attribute('innerHTML')
        print "Actual channel busy = " +str(chan_uti_24g)
          
         #Verify 5G radio chan utilization in the guage chart
        chan_widget_5g = driver.find_element_by_id("utilization5G")        
        chan_uti_5g = chan_widget_5g.get_attribute('innerHTML')
        print "Actual channel busy = " +str(chan_uti_5g)
           
        channel_busy = utils.get_radio_utilization()
        print "Expected channel_busy = " +channel_busy
           
        self.assertEqual(chan_uti_24g, channel_busy, "Actual 24G channel utilization is not same as Expected 24G channel utilization!")
        self.assertEqual(chan_uti_5g, channel_busy, "Actual 5G channel utilization is not same as Expected 5G channel utilization!")
        time.sleep(2)
        
        for i in range(0, int(actual_no_of_clients)):
            top5_device_id = "top_devices_" + str(i)

            #Retrieve the name of the client mentioned in the static stats file which is in form of mac
            name = utils.get_client_name()
            #Extract last 3 subsets of the mac and compare with that in the Client name griD
            expected_client_substr = name[-8:]
            actual_client_name = driver.find_element_by_css_selector('#' + top5_device_id + ' a').get_attribute('innerHTML').strip()
            print "Actual client name = " +str(actual_client_name) 
            print "Expected Client should contain: " +expected_client_substr
             
            if expected_client_substr in actual_client_name:    
                actual_client_traffic = driver.find_element_by_css_selector('#' + top5_device_id + ' div.overviewTableTextSecondary').get_attribute('innerHTML')
                print "Actual Top 5 Devices traffic = " +str(actual_client_traffic)
                bytes_rx = utils.get_client_stats("bytes_rx")
                bytes_tx = utils.get_client_stats("bytes_tx")
                expected_client_traffic = utils.caluclate_loc_dashboard_top5devices_traffic_kbps(bytes_rx, bytes_tx)
                print "Expected Top 5 Devices traffic =  " +str(expected_client_traffic)
                self.assertEqual(actual_client_traffic, expected_client_traffic, "Actual traffic of the Top 5 Devices is not same as Expected traffic!")
                break
            else:
                continue
            
        for i in range(0, 1):
            top5_ssid_id = "top_ssid_" + str(i)
  
            expected_ssid_name = columns['var_business_name'][2]
            actual_ssid_name = driver.find_element_by_css_selector('#' + top5_ssid_id + ' a').get_attribute('innerHTML').strip()
            print "Actual SSID name = " +str(actual_ssid_name) 
            print "Expected SSID name = " +expected_ssid_name
               
            if expected_ssid_name == actual_ssid_name:    
                actual_ssid_traffic = driver.find_element_by_css_selector('#' + top5_ssid_id + ' div.overviewTableTextSecondary').get_attribute('innerHTML')
                print "Actual Top 5 SSIDs traffic = " +str(actual_ssid_traffic)
                bytes_rx = utils.get_ap_stats("bytes_rx")
                bytes_tx = utils.get_ap_stats("bytes_tx")
                expected_ssid_traffic = utils.caluclate_loc_dashboard_top5ssids_traffic_kbps(bytes_rx, bytes_tx)
                print "Expected Top 5 SSIDs traffic =  " +expected_ssid_traffic
                self.assertEqual(actual_ssid_traffic, expected_ssid_traffic, "Actual traffic of the Top 5 SSIDs is not same as Expected traffic!")
                break
            else:
                continue

        for i in range(0, 1):
            top5_ap_id = "top_ap_" + str(i)
    
            expected_ap_name = properties.ap_name
            actual_ap_name = driver.find_element_by_css_selector('#' + top5_ap_id + ' a').get_attribute('innerHTML').strip()
            print "Actual AP name = " +str(actual_ap_name) 
            print "Expected AP name = " +expected_ap_name
             
            if expected_ap_name == actual_ap_name:    
                actual_ap_traffic = driver.find_element_by_css_selector('#' + top5_ap_id + ' div.overviewTableTextSecondary').get_attribute('innerHTML')
                print "Actual Top 5 APs traffic = " +str(actual_ap_traffic)
                bytes_rx = utils.get_ap_stats("bytes_rx")
                bytes_tx = utils.get_ap_stats("bytes_tx")
                expected_ap_traffic = utils.caluclate_loc_dashboard_top5aps_traffic_kbps(bytes_rx, bytes_tx)
                print "Expected Top 5 APs traffic =  " +expected_ap_traffic
                self.assertEqual(actual_ap_traffic, expected_ap_traffic, "Actual traffic of the Top 5 APs is not same as Expected traffic!")
                break
            else:
                continue


    def tearDown(self):
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)


def test_generate_result():
    suite = unittest.TestSuite()
    suite.addTest(TestVerifyLocationDashboard("verify_location_dashboard"))
    print suite
    print __file__
    results.run(suite, __file__)
