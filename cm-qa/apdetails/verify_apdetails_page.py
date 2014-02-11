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


class TestVerifyApDetailsPage(unittest.TestCase):
    def setUp(self):
        utils.call_display_headless_browser()
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.base_url = properties.vm_url
        self.verificationErrors = []
        self.accept_next_alert = True

    def verify_apdetails_page(self):
        columns = utils.get_var_details()
        driver = self.driver
        driver.get(self.base_url + "/home/login")
        driver.find_element_by_id("email").clear()
        driver.find_element_by_id("email").send_keys(columns['email'][0])
        driver.find_element_by_id("password").clear()
        driver.find_element_by_id("password").send_keys(columns['password'][0])
        driver.find_element_by_id("btnLogin").click()
        time.sleep(30)
        print "Clickin Customers dropdown"
        dropdown = driver.find_element_by_id("customerFilter")
        for option in dropdown.find_elements_by_tag_name("option"):
            if option.text == columns['var_business_name'][1]:
                option.click()
                time.sleep(5)

        driver.find_element_by_id("menuAccessPoints").click()
        time.sleep(30)
        driver.find_element_by_link_text(properties.ap_name).click()
        time.sleep(10)
        
        #Verify VAR and Locaiton names on AP details page
        cust_location_name = driver.find_element_by_id("location").get_attribute('innerHTML')
        #Remove the <br> from the var and location name string for the AP
        cust_location_name = re.sub('<[^>]*>', '', cust_location_name)
        print "Actual Customer and Location name = " +str(cust_location_name)
        expected_cust_name = columns['var_business_name'][1]
        expected_location_name = columns['var_business_name'][2]
        expected_cust_location_name = expected_cust_name + expected_location_name
        print "Expected Var and Location name = " +str(expected_cust_location_name)
        self.assertEqual(cust_location_name, expected_cust_location_name, "Actual Customer and Location name is not same as expected!")

        #Verify AP name on the AP details page
        actual_ap_name = driver.find_element_by_id("apName").get_attribute('innerHTML')
        print "Actual AP Name = " +str(actual_ap_name)
        expected_ap_name = properties.ap_name
        self.assertEqual(actual_ap_name, expected_ap_name, "Actual AP name is not same as expected AP Name!")
        
        #Verify manufacturer name on AP details page
        manufacturer_name = driver.find_element_by_id("manufacture").get_attribute('innerHTML')
        print "Actual manufacturer of AP = " +str(manufacturer_name)
        expected_manufacturer = db.search_manufacturer_model_in_ap_collection(properties.ap_name)
        print "Expected manufacturer of AP = " +str(expected_manufacturer)
        self.assertEqual(manufacturer_name, expected_manufacturer, "Actual AP manufacturer is not same as expected AP manufacturer!")
  
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
        expected_ap_traffic_mbps = utils.caluclate_apdetails_page_traffic_mbps(ap_bytes_rx, ap_bytes_tx)
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
            client_name_id = "CLIENT_NAME_" + str(i)
            ssid_id = "SSID_" + str(i)
            usage_id = "USAGE_DATA__Kbps_" + str(i)
            rssi_id = "SIGNAL_STRENGTH__dBm_" + str(i)
            
            #Retrieve the name of the client mentioned in the static stats file which is in form of mac
            name = utils.get_client_name()
            #Extract last 3 subsets of the mac and compare with that in the Client name griD
            expected_client_substr = name[-8:]
            actual_client_name = driver.find_element_by_id(client_name_id).get_attribute('innerHTML')
            print "Actual client name = " +str(actual_client_name) 
            print "Expected Client should contain: " +expected_client_substr
            
            #If the client matches get the client's rssi, usage and other values and verify them
            if expected_client_substr in actual_client_name:    
                #Verify Rssi values of client
                actual_rssi = driver.find_element_by_css_selector("#" + rssi_id + " div").get_attribute('innerHTML')
                print "Actual Rssi value of the client = " +str(actual_rssi)
                expected_rssi = utils.get_client_stats("rssi")
                print "Expected Rssi value of the client =  " +expected_rssi
                self.assertEqual(actual_rssi, expected_rssi, "Actual rssi of the client is not same as Expected rssi!")
         
                #Verify Essid values of client
                actual_essid = driver.find_element_by_id(ssid_id).get_attribute('innerHTML')
                print "Actual essid of the client = " +str(actual_essid)
                expected_essid = columns['var_business_name'][2]
                print "Expected essid of the client = " +str(expected_essid)
                self.assertEqual(actual_essid, expected_essid, "Actual essid of the client is not same as Expected essid!")
         
                #Verify Usage values of client
                actual_usage = driver.find_element_by_id(usage_id).get_attribute('innerHTML')
                print "Actual usage of the client = " +str(actual_usage)
                bytes_rx = utils.get_client_stats("bytes_rx")
                bytes_tx = utils.get_client_stats("bytes_tx")
                expected_usage = utils.caluclate_apdetails_page_client_usage_kbps(bytes_rx, bytes_tx)
                print "Expected usage of the client = " +str(expected_usage)
                self.assertEqual(int(actual_usage), int(expected_usage), "Actual usage of the client is not same as Expected usage!")
#             else:
#                 self.assertIn(expected_client_substr, actual_client_name, "Client not present on UI")

        
    def tearDown(self):
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)


def test_generate_result():
    suite = unittest.TestSuite()
    suite.addTest(TestVerifyApDetailsPage("verify_apdetails_page"))
    print suite
    print __file__
    results.run(suite, __file__)
