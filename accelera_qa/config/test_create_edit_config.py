import config_blob
from utils import config_utils, db, results
import unittest


class TestEditConfig(unittest.TestCase):
    """  This test case covers following scenario:
         1. Creates defined config blob(if config blob is already present then creates config blob suffixed with timestamp)
         2. Edit specified parameters of config blob.
         3. Checks whether config blob is edited successfully.
    """

    def setUp(self):
        pass

    def create_edit_config_blob(self):
        config = config_blob.create_blob
        #creating config blob with defined parameters.
        config_name = config_utils.create_config_blob(config)
        #Verifying whether config blob is created and added in configuration collection.
        db.search_config_in_configuration_collection(config_name)
        #Editing a config blob with specified parameter.
        edit_config_blob = config_blob.edit_blob
        edit_config_blob["config_name"] = config_name
        config_utils.edit_config_blob(config_name, edit_config_blob)
        #After editing retrieving a config blob from configuration collection.
        config_blob_db = db.search_config_in_configuration_collection(config_name)
        #Verifying whether config blob is edited successfully.
        print("Verifying config blob %s is edited successfully" % config_name)
        flag = 0
        for each in edit_config_blob['wif_config']:
            for i in range(0, 2):
                if i == 0:
                    each["radio_id"] = "2.4G"
                    if each not in config_blob_db['wif_config']:
                        flag = 1
                elif i == 1:
                    each["radio_id"] = "5G"
                    if each not in config_blob_db['wif_config']:
                        flag = 1
        if edit_config_blob['system_config'] == config_blob_db['system_config'] and flag == 0:
            print("Config blob %s is edited successfully" % config_name)
        else:
            raise AssertionError("Config blob %s is not edited successfully" % config_name)

    def tearDown(self):
        pass


def test_generate_result():
    suite = unittest.TestSuite()
    suite.addTest(TestEditConfig("create_edit_config_blob"))
    print suite
    print __file__
    results.run(suite, __file__)
