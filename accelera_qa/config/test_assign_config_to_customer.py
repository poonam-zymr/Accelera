from utils import config_utils, db, results
import pymongo
import unittest
import properties
import requests
import json
import time


class TestPushConfigToCustomer(unittest.TestCase):
    """  This test case covers following scenario"""
    """1. Pushing config to customer./n2. Verifying config is applied to customer.
    """

    def setUp(self):
        pass

    def assign_config_to_customer(self):
        config_id = config_utils.push_config_to_customer()
        db.verify_customer_default_config_id(config_id)

    def tearDown(self):
        pass


def test_generate_result():
    suite = unittest.TestSuite()
    suite.addTest(TestPushConfigToCustomer("assign_config_to_customer"))
    #print suite
    #print __file__
    results.run(suite, __file__)
