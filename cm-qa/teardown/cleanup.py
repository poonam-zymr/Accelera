import csv
from collections import defaultdict
from utils import utils, db, results
import properties
import pymongo
import unittest


class TestCleanup(unittest.TestCase):

    def cleanup(self):
        columns = utils.get_var_details()

        #Steps to delete a var created from var collection
        var_name = columns['var_business_name'][0]
        var_name = var_name.strip()
        db.delete_var(var_name)

        #Steps to delete var user created from user collection
        var_email = columns['email'][0]
        var_email = var_email.strip()
        db.delete_user(var_email)

        #Steps to delete a customer created from customer collection
        cust_name = columns['var_business_name'][1]
        cust_name = cust_name.strip()
        db.delete_customer(cust_name)

        #Steps to delete customer user created from user collection
        cust_email = columns['email'][1]
        cust_email = cust_email.strip()
        db.delete_user(cust_email)

        #Steps to delete a config created
        config_name = columns['var_business_name'][2]
        config_name = config_name.strip()
        db.delete_config(config_name)

        #Steps to delete a location created
        loc_name = columns['var_business_name'][2]
        loc_name = loc_name.strip()
        db.delete_location(loc_name)


def test_generate_result():
    suite = unittest.TestSuite()
    suite.addTest(TestCleanup("cleanup"))
    print suite
    print __file__
    results.run(suite, __file__)
