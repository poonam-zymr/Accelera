import requests
import json
import properties
import db
import utils
from time import gmtime, strftime
from apis import config_api, common_api


#This function returns list of configurations defined for customer
def get_config_list(cookies):
    customer_id = retrieve_customer_id()
    configrequest = properties.web_ui_baseurl + (config_api.config_list_api % customer_id)
    config_response = requests.get(configrequest, cookies=cookies)
    js = json.loads(config_response.text)
    return js


#This function returns list of customers.
def get_customer_list(cookies):
    customer_request = properties.web_ui_baseurl + common_api.customers_api
    customer_response = requests.get(customer_request, cookies=cookies)
    js2 = json.loads(customer_response.text)
    return js2


#This function creates config blob with defined parametes.
def create_config_blob(config_blob):
    blob = []
    for each in config_blob:
        if isinstance(config_blob[each], dict) and each == 'system_config' or each == 'radio_config':
            for i in config_blob[each]:
                element = ("%s=%s&" % (i, config_blob[each][i]))
                blob.append(element)
        if isinstance(config_blob[each], list) and each == 'wif_config':
            for i in config_blob[each]:
                if isinstance(i, dict):
                    for j in i:
                        element = ("%s[]=%s&" % (j, i[j]))
                        blob.append(element)
        if isinstance(config_blob[each], dict) == False and isinstance(config_blob[each], list) == False:
            if 'config_name' in each:
                login_cookie = utils.login()
                js = get_config_list(login_cookie)
                config_name = config_blob[each]
                print("Creating config blob with name %s" % config_name)
                element = ("%s=%s&" % (each, config_name))
                for i in range(len(js['results'])):
                    ourResult = js['results'][i]['config_name']
                    if config_blob[each] == str(ourResult):
                        print("Config blob %s already exists!" % config_blob[each])
                        timestamp = strftime("_%Y%m%d%H%M%S", gmtime())
                        config_name = config_blob[each] + timestamp
                        print("Creating config blob with name %s" % config_name)
                        element = ("%s=%s&" % (each, config_name))
                        break
            else:
                element = ("%s=%s&" % (each, config_blob[each]))
            blob.append(element)
    request = ''
    for each in blob:
        request = request + each
    customer_id = retrieve_customer_id()
    request = request + ("customer_id=%s" % customer_id)
    createconfig_request = properties.web_ui_baseurl + (config_api.create_config_api % request)
    createconfig_response = requests.get(createconfig_request, cookies=login_cookie)
    js1 = json.loads(createconfig_response.text)
    if 'Template Saved!' in js1['results']['message']:
        print ("Configuration blob %s is created successfully." % (config_name))
    else:
        raise AssertionError("Configuration blob %s is not created successfully." % (config_name))
    return config_name


#This function edit config blob with specified parameters.
def edit_config_blob(config_name, config_blob):
    blob = []
    login_cookie = utils.login()
    print("Editing config blob %s" % config_name)
    for each in config_blob:
        if isinstance(config_blob[each], dict) and each == 'system_config' or each == 'radio_config':
            for i in config_blob[each]:
                element = ("%s=%s&" % (i, config_blob[each][i]))
                blob.append(element)
        if isinstance(config_blob[each], list) and each == 'wif_config':
            for i in config_blob[each]:
                if isinstance(i, dict):
                    for j in i:
                        element = ("%s[]=%s&" % (j, i[j]))
                        blob.append(element)
        if isinstance(config_blob[each], dict) == False and isinstance(config_blob[each], list) == False:
            element = ("%s=%s&" % (each, config_blob[each]))
            blob.append(element)
    request = ''
    for each in blob:
        request = request + each
    config_id = retrieve_config_id(config_name)
    customer_id = retrieve_customer_id()
    request = request + ("config_id=%s&customer_id=%s" % (config_id, customer_id))
    createconfig_request = properties.web_ui_baseurl + (config_api.create_config_api % request)
    createconfig_response = requests.get(createconfig_request, cookies=login_cookie)
    js1 = json.loads(createconfig_response.text)
    if 'Template Updated!' in js1['results']['message']:
        print ("Configuration blob %s is updated successfully." % (config_name))
    else:
        raise AssertionError("Configuration blob %s is not updated successfully." % (config_name))


##This function returns config id for given configuration blob
def retrieve_config_id(config_name):
    login_cookie = utils.login()
    js3 = get_config_list(login_cookie)
    config_id = None
    for i in range(len(js3['results'])):
        ourResult = js3['results'][i]['config_name']
        if config_name == ourResult:
            config_id = js3['results'][i]['id']
    if config_id == None:
        raise AssertionError("Configuration blob %s is not exist" % config_name)
    return config_id


#This function pushes config to customer
def push_config_to_customer():
    config_id = None
    login_cookie = utils.login()
    customer_id = retrieve_customer_id()
    print "Pushing configuration to customer."
    if customer_id != None:
        config_id = retrieve_config_id(properties.configuration_name)
        if config_id != None:
            default_config_request = properties.web_ui_baseurl + (config_api.push_config_to_customer_api % (customer_id, config_id))
            config_update_response = requests.get(default_config_request, cookies=login_cookie)
            js3 = json.loads(config_update_response.text)
            if "Default Configuration of Customer updated" in js3['results']['message']:
                print ("Default config %s is applied to customer %s successfully." % (properties.configuration_name, properties.customer_name))
            else:
                raise AssertionError("Default config %s is not applied to customer %s." % (properties.configuration_name, properties.customer_name))
    return config_id


#This function returns id for customer entryh.
def retrieve_customer_id():
    login_cookie = utils.login()
    customer_id = None
    js2 = get_customer_list(login_cookie)
    for i in range(len(js2['results'])):
        ourResult = js2['results'][i]['name']
        if properties.customer_name == ourResult:
            customer_id = js2['results'][i]['id']
    return customer_id


#This fucntion pushes confgi to AP.
def push_config_to_ap(ap_id, ap_jid, config_name):
    login_cookie = utils.login()
    config_id = retrieve_config_id(config_name)
    print "Pushing config to AP."
    if config_id != None:
        push_config_request = properties.web_ui_baseurl + (config_api.push_config_to_AP_api % (ap_id, config_id, properties.customer_id))
        push_config_response = requests.get(push_config_request, cookies=login_cookie)
        js3 = json.loads(push_config_response.text)
        if "Configuration template change initiated" in js3['results']['message']:
                print ("Config %s is applied to AP %s successfully." % (properties.configuration_name, ap_jid))
        else:
            raise AssertionError("Config %s is not applied to AP %s." % (properties.configuration_name, ap_jid))
    return config_id
