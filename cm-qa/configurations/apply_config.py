from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
import unittest
import time
import paramiko
import properties
from utils import utils, db, results, seleutils
from registration import create_config

class TestApplyConfig(unittest.TestCase):
    """This class verifies apply config functionality.
    """
    def setUp(self):
        self.config_name = properties.config_name
        seleutils.create_config(self.config_name)
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.base_url = properties.vm_url
        self.verificationErrors = []
        self.accept_next_alert = True

    def _1_apply_config(self):
        """This test case verifies whether config is applied to AP successfully.
        """
        
        columns = utils.get_var_details()
        driver = self.driver
        config_name = self.config_name
        driver.get(self.base_url + "/home/login")
        driver.find_element_by_id("email").clear()
        driver.find_element_by_id("email").send_keys(columns['email'][1])
        driver.find_element_by_id("password").clear()
        driver.find_element_by_id("password").send_keys(columns['password'][1])
        driver.find_element_by_id("btnLogin").click()
        time.sleep(10)
        
        driver.find_element_by_id("menuAccessPoints").click()
        time.sleep(5)
        
        i = 0
        for option in driver.find_elements_by_css_selector("#ap_grid_table tbody tr"):
            client_name_id = "AP_Name_" + str(i)
            status_id = "Status_" + str(i)
            select_checkbox_id = "_" + str(i)
            if properties.ap_name == str(driver.find_element_by_css_selector("#" + client_name_id + " a").get_attribute(
                 'innerHTML')) and driver.find_element_by_css_selector('#' + status_id + ' img').get_attribute(
                 'title') == 'available':
                #print "pass"
                driver.find_element_by_css_selector("#" + select_checkbox_id + " div").click()
                time.sleep(5)
                driver.find_element_by_id("applyTemplateBtn").click()
                j = 0
                for option1 in driver.find_elements_by_css_selector("#config_list_table tbody tr"):
                    template_name_id = "Template_name_" + str(j)
                    select_radiobutton_id = "__" + str(j)
                    #print select_radiobutton_id
                    if config_name == driver.find_element_by_id(template_name_id).get_attribute('innerHTML'):
                        driver.find_element_by_css_selector("#" + select_radiobutton_id + " input").click()
                        driver.find_element_by_xpath("//html/body/div[2]/div/div/div/div[2]/div[2]/a").click()
                        #driver.find_element_by_id("btnApply").click()
                    j = j + 1
                time.sleep(5)
                
                ##Checking for API response message which comes up after applying config to AP.
                try:
                    actual_message = driver.find_element_by_xpath('//*[@id="deleteSuccessMessage"]').get_attribute('innerHTML')
                    expected_message = "Configuration template change initiated for AP(s)."
                    print "Actual message = " + actual_message
                    print "Expected message = " + expected_message
                    #self.assertEqual(actual_message, expected_message, "Appropriate message '%s' is not displayed" % expected_message)
                except AssertionError as e: self.verificationErrors.append(str(e))
                time.sleep(40)
                
                ####Checking for the default config running on AP.
                ssid = config_name
                expected_running_config_id = db.search_field_in_configuration_collection('_id', config_name)
                #Get the ap's jid
                ap_jid = utils.get_ap_jid(properties.real_ap_ip)
                print "AP jid return value is: " + ap_jid
                ap_jid = ap_jid.strip()
                actual_running_config_id = db.search_field_in_ap_collection('running_config_id', ap_jid)
                print "Actual running config id of AP is:" + str(actual_running_config_id) 
                print "Expected running config id of AP is:" + str(expected_running_config_id)
                try:
                    self.assertEqual(str(actual_running_config_id), str(expected_running_config_id),
                                "Expected configuration %s is not running on %s AP." % (ssid, ap_jid))
                except AssertionError as e: self.verificationErrors.append(str(e)) 
                
                
                #Verify if radios are enabled on the AP
                ssh = paramiko.SSHClient()
                ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                ssh.connect(properties.real_ap_ip, username='root',
                    password='password')
                
                try:
                    stdin, stdout, stderr = ssh.exec_command("uci show | grep disabled")
                except SSHException, e:
                    print e
                data = stdout.readlines()
                for eachLine in data:
                    if "radio0" in eachLine:
                            radio_line = eachLine.split("\n")
                            radio_state = radio_line[0]
                            print "Actual Radio0 state is: " + radio_state
                            expected_radio_state = "wireless.radio" + "0" + ".disabled=0"
                            print "Expected radio state is: " + expected_radio_state
                            try:
                                self.assertEqual(radio_state.strip(), expected_radio_state,
                                             "After applying config to AP Radio0 was not disabled")
                            except AssertionError as e: self.verificationErrors.append(str(e))
                    elif "radio1" in eachLine:
                            radio_line = eachLine.split("\n")
                            radio_state = radio_line[0]
                            print "Actual Radio1 state is:  " + radio_state
                            expected_radio_state = "wireless.radio" + "1" + ".disabled=0"
                            print "Expected radio state is: " + expected_radio_state
                            try:
                                self.assertEqual(radio_state.strip(), expected_radio_state,
                                             "After applying config to AP Radio1 was not disabled")
                            except AssertionError as e: self.verificationErrors.append(str(e))
                            
                ###Checking for the SSID running on AP            
                ssh = paramiko.SSHClient()
                ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                ssh.connect(properties.real_ap_ip, username='root',
                    password='password')
                try:
                #To get the ssids running on AP
                    (stdin, stdout, stderr) = ssh.exec_command("uci show | grep ssid")
                except SSHException, e:
                    print e
                ssid_output = stdout.readlines()
                result = False
                cnt = 0
                for num, each in enumerate(ssid_output):
                    each = each.replace("\n", "")
                    if cnt == 0:
                        expected_ssid = ("wireless.@wifi-iface[%s].ssid=%s" % (cnt, ssid))
                    elif cnt == 1:
                        expected_ssid = ("wireless.@wifi-iface[%s].ssid=%s" % (cnt, ssid))
                    cnt = cnt + 1
                    if expected_ssid == each:
                        result = True
                        print "Expected SSID is:" + expected_ssid
                        print "Actual SSID is:" + each
                    else:
                        result = False
                        print "Expected SSID is:" + expected_ssid
                        print "Actual SSID is:" + each
                try:
                    self.assertEqual(result, True, "Expected SSID %s is not running on AP." % ssid)
                except AssertionError as e: self.verificationErrors.append(str(e))
                #print ("Expected SSID %s is running on AP." % ssid)
            i = i + 1    
                
    
    def tearDown(self):
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)    

        
#if __name__ == "__main__":
#    unittest.main()
def test_generate_result():
    suite = unittest.TestSuite()
    suite.addTest(TestApplyConfig("_1_apply_config"))
    print suite
    print __file__
    results.run(suite, __file__)

