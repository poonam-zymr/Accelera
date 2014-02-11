#import json
import properties
#import config_utils
import pymongo
import utils


#This function returns specific collection data
def retrieve_collection(collection_name):
    mongo_db_ip = properties.mongo_db_ip
    connection = pymongo.MongoClient(mongo_db_ip)
    db_name = properties.db_to_be_used
    mongo_db = connection[db_name]
    mongo_collection = mongo_db[collection_name]
    connection.disconnect()
    return mongo_collection


#This function checks whether AP gets added in ap collection after onboadring
def search_ap_in_ap_collection(ap_jid):
    print ("Searching AP %s in ap collection" % ap_jid)
    mongo_ap_collection = retrieve_collection(properties.ap_collection_name)
    try:
        result = False
        for item in mongo_ap_collection.find({'apid': ap_jid}):
            result = True
            print "Verifying AP: " + item['apid'] + " in database"
            print ap_jid + " registered successfully!"
        if result == False:
            assert result, "AP " + ap_jid + " was not registered!"
    except AssertionError:
        print "AP " + ap_jid + " not registered in database!"
    return ap_jid


def search_manufacturer_model_in_ap_collection(ap_name):
    print ("Searching Manufacturer %s in ap collection" % ap_name)
    mongo_ap_collection = retrieve_collection(properties.ap_collection_name)
    try:
        result = False
        for item in mongo_ap_collection.find({'ap_name': ap_name}):
            result = True
            print "Verifying AP: " + item['ap_name'] + " in database"
            manufacturer = item['manufacturer']
            model = item['model']
        if result == False:
            assert result, "AP " + ap_name + " was not registered!"
    except AssertionError:
        print "AP " + ap_name + " not registered in database!"
    return manufacturer + " " + model


def search_model_in_ap_collection(ap_name):
    print ("Searching Manufacturer %s in ap collection" % ap_name)
    mongo_ap_collection = retrieve_collection(properties.ap_collection_name)
    try:
        result = False
        for item in mongo_ap_collection.find({'ap_name': ap_name}):
            result = True
            print "Verifying AP: " + item['ap_name'] + " in database"
            model = item['model']
        if result == False:
            assert result, "AP " + ap_name + " was not registered!"
    except AssertionError:
        print "AP " + ap_name + " not registered in database!"
    return model


def search_mac_in_ap_collection(ap_name):
    print ("Searching MAC address %s in ap collection" % ap_name)
    mongo_ap_collection = retrieve_collection(properties.ap_collection_name)
    try:
        result = False
        for item in mongo_ap_collection.find({'ap_name': ap_name}):
            result = True
            print "Verifying AP: " + item['ap_name'] + " in database"
            mac = item['wired_mac']
        if result == False:
            assert result, "AP " + ap_name + " was not registered!"
    except AssertionError:
        print "AP " + ap_name + " not registered in database!"
    return mac


def search_ip_in_ap_collection(ap_name):
    print ("Searching IP address %s in ap collection" % ap_name)
    mongo_ap_collection = retrieve_collection(properties.ap_collection_name)
    try:
        result = False
        for item in mongo_ap_collection.find({'ap_name': ap_name}):
            result = True
            print "Verifying AP: " + item['ap_name'] + " in database"
            ip = item['public_ip']
        if result == False:
            assert result, "AP " + ap_name + " was not registered!"
    except AssertionError:
        print "AP " + ap_name + " not registered in database!"
    return ip

def search_ap_in_new_ap_collection(ap_jid):
    print ("Searching AP %s in new_ap collection" % ap_jid)
    mongo_new_ap_collection = retrieve_collection(properties.new_ap_collection_name)
    try:
        result = False
        for item in mongo_new_ap_collection.find({'apid': ap_jid}):
            result = True
            print "Verifying AP: " + item['apid'] + " in database"
            print ap_jid + " registered successfully!"
        if result == False:
            assert result, "AP " + ap_jid + " was not registered!"
    except AssertionError:
        print "AP " + ap_jid + " not registered in database!"
    return ap_jid


#This function will search for a particular var user in the var collection
def search_var_in_var_collection(var_name):
    print ("Searching VAR %s in var collection" % var_name)
    mongo_var_collection = retrieve_collection(properties.var_collection_name)
    try:
        result = False
        for item in mongo_var_collection.find({'name': var_name}):
            result = True
            print "Verifying Var: " + item['name'] + " in database"
            print var_name + " registered successfully!"
        if result == False:
            assert result, "Var " + var_name + " was not registered!"
    except AssertionError:
        print "Var " + var_name + " not registered in database!"
    return var_name


#This function will search for a customer user in the customer collection
def search_cust_in_customer_collection(cust_name):
    print ("Searching Customer %s in customer collection" % cust_name)
    mongo_customer_collection = retrieve_collection(properties.cust_collection_name)
    try:
        result = False
        for item in mongo_customer_collection.find({'name': cust_name}):
            result = True
            print "Verifying Customer: " + item['name'] + " in database"
            print cust_name + " registered successfully!"
        if result == False:
            assert result, "Customer " + cust_name + " was not registered!"
    except AssertionError:
        print "Customer " + cust_name + " not registered in database!"
    return cust_name


#Search config in configuration collection
def search_config_in_configuration_collection(config_name):
    print ("Searching Config %s in configuration collection" % config_name)
    mongo_config_collection = retrieve_collection(properties.config_collection_name)
    try:
        result = False
        for item in mongo_config_collection.find({'config_name': config_name}):
            result = True
            print "Verifying Config: " + item['config_name'] + " in database"
            print config_name + " created successfully!"
        if result == False:
            assert result, "Config " + config_name + " was not created!"
    except AssertionError:
        print "Config " + config_name + " not created in database!"
    return config_name


#Search location in location collection
def search_location_in_location_collection(location_name):
    print ("Searching Location %s in location collection" % location_name)
    mongo_location_collection = retrieve_collection(properties.location_collection_name)
    try:
        result = False
        for item in mongo_location_collection.find({'name': location_name}):
            result = True
            print "Verifying Location: " + item['name'] + " in database"
            print location_name + " created successfully!"
        if result == False:
            assert result, "Location " + location_name + " was not created!"
    except AssertionError:
        print "Location " + location_name + " not created in database!"
    return location_name


def search_serialno_in_new_ap_collection(ap_jid):
    print ("Searching Serial no for %s in new_ap collection" % ap_jid)
    mongo_newap_collection = retrieve_collection(properties.new_ap_collection_name)
    try:
        result = False
        for item in mongo_newap_collection.find({'apid': ap_jid}):
            result = True
            print "Verifying Serial no for: " + item['apid'] + " in database"
            serial_no = item['serial_number']
            print item['serial_number'] + " Serial no. of the AP!"
        if result == False:
            assert result, "AP " + ap_jid + " was not registered!"
    except AssertionError:
        print "AP " + ap_jid + " not registered in database!"
    return serial_no


def delete_config(config_name):
    mongo_config_collection = retrieve_collection(properties.config_collection_name)
    try:
            result = False
            for item in mongo_config_collection.find({'config_name': config_name}):
                result = True
                mongo_config_collection.remove({'config_name': config_name})
                print "Deleting Config from database"
            if result == False:
                assert result, "Config " + config_name + " was not present in db!"
    except AssertionError:
            print "Config " + config_name + " not created in database!"


def delete_var(var_name):
    mongo_var_collection = retrieve_collection(properties.var_collection_name)
    try:
            result = False
            for item in mongo_var_collection.find({'name': var_name}):
                result = True
                #var_mongo_id = item['_id']
                mongo_var_collection.remove({'name': var_name})
                print "Deleting VAR from database"
            if result == False:
                assert result, "VAR " + var_name + " was not present in db!"
    except AssertionError:
            print "VAR " + var_name + " not created in database!"


def delete_user(user_email):
    mongo_user_collection = retrieve_collection(properties.user_collection_name)
    try:
            result = False
            for item in mongo_user_collection.find({'email': user_email}):
                result = True
                mongo_user_collection.remove({'email': user_email})
                print "Deleting user from database"
            if result == False:
                assert result, "User " + user_email + " was not present in db!"
    except AssertionError:
            print "User " + user_email + " not created in database!"


def delete_customer(cust_name):
    mongo_cust_collection = retrieve_collection(properties.cust_collection_name)
    try:
            result = False
            for item in mongo_cust_collection.find({'name': cust_name}):
                result = True
                #var_mongo_id = item['_id']
                mongo_cust_collection.remove({'name': cust_name})
                print "Deleting Customer from database"
            if result == False:
                assert result, "Customer " + cust_name + " was not present in db!"
    except AssertionError:
            print "Customer " + cust_name + " not created in database!"


def delete_location(loc_name):
    mongo_loc_collection = retrieve_collection(properties.location_collection_name)
    try:
            result = False
            for item in mongo_loc_collection.find({'name': loc_name}):
                result = True
                mongo_loc_collection.remove({'name': loc_name})
                print "Deleting Location from database"
            if result == False:
                assert result, "Location " + loc_name + " was not present in db!"
    except AssertionError:
            print "Location " + loc_name + " not created in database!"


def delete_ap(apid):
    mongo_ap_collection = retrieve_collection(properties.ap_collection_name)
    try:
            result = False
            for item in mongo_ap_collection.find({'apid': apid}):
                result = True
                mongo_ap_collection.remove({'apid': apid})
                print "Deleting AP from database"
            if result == False:
                assert result, "AP " + apid + " was not present in db!"
    except AssertionError:
            print "AP " + apid + " not present in database!"
            
def verify_delete_ap(apname):
    mongo_ap_collection = retrieve_collection(properties.ap_collection_name)
    try:
            result = False
            for item in mongo_ap_collection.find({'ap_name': apname}):
                result = True
            if result == False:
                assert result, "AP " + apname + " was already deleted from db!"
    except AssertionError:
            print "AP " + apname + " not present in database!"

def search_field_in_client_last_collection(search_field, client_mac):
    print ("Searching %s for client %s in client_last_connection collection" % (search_field, client_mac))
    mongo_clientlastconnection_collection = retrieve_collection(properties.client_last_connection_collection_name)
    try:
        result = False
        for item in mongo_clientlastconnection_collection.find({'mac': client_mac}):
            result = True
            print("Verifying %s for client: %s in database" % (search_field, client_mac))
            searched_item = item[search_field]
            print("%s for client %s is = %s" % (search_field, client_mac, searched_item))
        if result == False:
            assert result, "Client " + client_mac + " was not connected!"
    except AssertionError:
        print "Client" + client_mac + " not found in database!"
    return searched_item
    
    
    
