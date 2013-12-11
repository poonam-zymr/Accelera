import properties
import pymongo


#This function returns specific collection data
def retrieve_collection(collection_name):
    mongo_db_ip = properties.mongo_ip
    connection = pymongo.MongoClient(mongo_db_ip)
    db_name = properties.db_to_be_used
    mongo_db = connection[db_name]
    mongo_collection = mongo_db[collection_name]
    connection.disconnect()
    return mongo_collection


#This function verifies whether default config is applied to customer
def verify_customer_default_id(config_id, customer_id):
    mongo_collection = retrieve_collection(properties.customer_collection_name)
    mongo_document = mongo_collection.find_one({
        "name": properties.customer_name}, {"default_config_id": 1})
    if str(mongo_document['_id']) == str(customer_id):
        if not str(mongo_document['default_config_id']) == str(config_id):
            raise AssertionError("Default config %s is not assigned to \
            customer %s." % (config_id, properties.customer_name))
        else:
            print ("Default config %s is assigned to customer %s."
                    (config_id, properties.customer_name))


#This function checks whether AP gets added
# in new_ap collection after registration
def search_ap_in_new_ap_collection(ap_jid):
    print ("Searching AP %s in new_ap collection" % ap_jid)
    mongo_newap_collection = retrieve_collection(
                    properties.new_ap_collection_name)
    mongo_newap_document = mongo_newap_collection.find_one({
                    "apid": ap_jid}, {"serial_number": 1})
    ap_serial_number = str(mongo_newap_document['serial_number'])
    if mongo_newap_document != None:
        print ("AP %s is registered successfully and added\
    in new_ap collection." % ap_jid)
    else:
        raise AssertionError("AP %s is not added in new_ap\
        collection." % ap_jid)
    return ap_serial_number


#This function checks whether AP gets added in ap collection after onboadring
def search_ap_in_ap_collection(ap_jid):
    print ("Searching AP %s in ap collection" % ap_jid)
    mongo_ap_collection = retrieve_collection(properties.ap_collection_name)
    mongo_ap_document = mongo_ap_collection.find_one({
                            "apid": ap_jid}, {"ap_name": 1})
    ap_name = str(mongo_ap_document['ap_name'])
    ap_id = str(mongo_ap_document['_id'])
    if ap_name == properties.apjid:
        print ("AP %s is found in ap collection." % ap_jid)
    else:
        raise AssertionError("AP %s is not found in ap collection." % ap_jid)
    return ap_id


#This function searches given config blob in configuration collection.
def search_config_in_configuration_collection(config_name):
    print ("Searching config blob %s in configuration \
    collection" % config_name)
    mongo_ap_collection = retrieve_collection(
                        properties.configuration_collection_name)
    mongo_ap_document = mongo_ap_collection.find_one
    ({"config_name": config_name})
    mongo_ap_document = (mongo_ap_document)
    if mongo_ap_document != None:
        print ("Config %s is found in configuration\
         collection." % config_name)
    else:
        raise AssertionError("Config %s is not found in \
        configuration collection." % config_name)
    return mongo_ap_document


#This function verifies running config on AP.
def verify_ap_running_config_id(ap_jid, config_id):
    print "Validating AP config."
    mongo_ap_collection = retrieve_collection(properties.ap_collection_name)
    mongo_ap_document = mongo_ap_collection.find_one({"apid": ap_jid})
    running_config_id = str(mongo_ap_document['running_config_id'])
    if running_config_id == str(config_id):
        print ("Config %s is pushed to AP %s successfully."
               % (properties.configuration_name, ap_jid))
    else:
        raise AssertionError("Config %s is not pushed to AP %s."
                             % (properties.configuration_name, ap_jid))


#This function verifies running config on customer.
def verify_customer_default_config_id(config_id):
    mongo_customer_collection = retrieve_collection(
                                properties.customer_collection_name)
    mongo_customer_document = mongo_customer_collection.find_one({
            "name": properties.customer_name}, {"default_config_id": 1})
    default_config_id = str(mongo_customer_document['default_config_id'])
    if default_config_id == str(config_id):
        print ("Config %s is pushed to customer %s successfully."
                % (properties.configuration_name, properties.customer_name))
    else:
        raise AssertionError("Config %s is not pushed to customer %s."
                % (properties.configuration_name, properties.customer_name))
