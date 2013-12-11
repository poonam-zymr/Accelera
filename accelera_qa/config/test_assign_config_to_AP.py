from utils import utils, results, db
import unittest
import properties
import requests


class TestPushConfigToAP(unittest.TestCase):
    """  This test case covers following scenario:
         1. Starting services.
         2. Starting apmanager.
         3. Register AP with apmanager.
         4. Onboarding of AP.
         5. Pushing config to AP.
    """

    def setUp(self):
        #Starting services.
        utils.start_runworkers()
        #starting apmanager
        utils.start_apmanager()
        #Configuring AP with apmanager
        utils.real_ap_registration(properties.real_ap)

    def assign_config_to_ap(self):
        ap_jid = properties.apjid
        # Verify if the ap entry is made in new_ap collection.
        ap_serial_number = db.search_ap_in_new_ap_collection(ap_jid)
        #Onboarding AP.
        utils.ap_onboarding(ap_jid, ap_serial_number)
        #Searching AP in ap collection after onboarding.
        ap_id = db.search_ap_in_ap_collection(ap_jid)

    def tearDown(self):
        pass


def test_generate_result():
    suite = unittest.TestSuite()
    suite.addTest(TestPushConfigToAP("assign_config_to_ap"))
    print suite
    print __file__
    results.run(suite, __file__)
