from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
import unittest
import time
import properties
import paramiko
from utils import utils, db, results


class TestEditConfig(unittest.TestCase):
    """This class verifies edit config functionality.
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

    def _1_edit_config(self):
        """This test case verifies whether config is edited successfully.
        """
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
                Select(driver.find_element_by_name("radio_50g_status")).select_by_visible_text("Off")
                driver.find_element_by_id("network_header").click()
                for j in range(0, 2):
                    driver.find_element_by_id("ssid_" + str(j)).clear()
                    if j == 0:
                        ssid = columns['var_business_name'][2].replace(" ", "_")
                    else:
                        ssid = columns['var_business_name'][2].replace(" ", "_") + "_1"
                    driver.find_element_by_id("ssid_" + str(j)).send_keys(ssid)
                    time.sleep(5)
                    print "Clicking passphrase type dropdwon"
                    passphrase_dropdown = driver.find_element_by_id("security_" + str(j))
                    for option in passphrase_dropdown.find_elements_by_tag_name("option"):
                        if option.get_attribute('value') == "wpa-psk":
                            option.click()
                            time.sleep(5)
                    driver.find_element_by_id("passphrase_" + str(j)).clear()
                    driver.find_element_by_id("passphrase_" + str(j)).send_keys("accelera") 
                driver.find_element_by_id("submitButton").click()
                time.sleep(5)
                try:
                    ####Checking for the message which comes up after saving the config successfully.
                    actual_message = driver.find_element_by_id("successMessage").get_attribute("innerHTML")
                    print "Actual message = " + actual_message
                    expected_message = 'Template Saved successfully.'
                    print "Expected message = " + expected_message
                    self.assertEqual(actual_message, expected_message, "Configuration is not saved!")
                except AssertionError as e: self.verificationErrors.append(str(e)) 
    
    def _2_Verify_config_repushed_to_AP(self):
        """This test case verifies whether edited config is repushed to AP.
        """
        self.verificationErrors = []
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
        ssid1 = columns['var_business_name'][2].replace(" ", "_")
        ssid2 = columns['var_business_name'][2].replace(" ", "_") + "_1"
        cnt = 0
        result = False
        for num, each in enumerate(ssid_output):
            each = each.replace("\n", "")
            if num == cnt:
                if cnt < 2:
                    parameter = ("wireless.@wifi-iface[%s].ssid=%s" % (cnt, ssid1))
                elif cnt > 2:
                    parameter = ("wireless.@wifi-iface[%s].ssid=%s" % (cnt, ssid2))
            if parameter == each:
                result = True
            else:
                result = False
        try:
            self.assertEqual(result, False, "SSID's are not re-pushed correctly to AP.")
        except AssertionError as e: self.verificationErrors.append(str(e))
        print "SSID's are correctly re-pushed to AP." 
        ssh.close()
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(properties.real_ap_ip, username='root',
                    password='password')
        try:
            #To get the wifi radio settings running on AP
            (stdin, stdout, stderr) = ssh.exec_command("uci show | grep disabled")
        except SSHException, e:
            print e
        result = False
        wifi_radio_output = stdout.readlines()
        for num, each in enumerate(wifi_radio_output):
            each = each.replace("\n", "") 
            if num == 0:
                radio = "wireless.radio0.disabled=0"
            elif num == 1:
                radio = "wireless.radio0.disabled=1"
            if radio == each:
                result = True
            else:
                result = False
        try:
            self.assertEqual(result, False, "Radio settings are not re-pushed correctly to AP.")
        except AssertionError as e: self.verificationErrors.append(str(e))
        print "Radio settings are correctly re-pushed to AP." 
        ssh.close()
        self.assertEqual([], self.verificationErrors)
        
    @classmethod    
    def tearDownClass(self):
        self.driver.quit()    

        
#if __name__ == "__main__":
#    unittest.main()
def test_generate_result():    
    suite = unittest.TestSuite()
    suite.addTest(TestEditConfig("_1_edit_config"))
    suite.addTest(TestEditConfig("_2_Verify_config_repushed_to_AP"))
    print suite
    print __file__
    results.run(suite, __file__)
