import properties
import os
import time
import subprocess
import sys
import paramiko
from openfire import UserService
from openfire import UserAlreadyExistsException, InvalidResponseException
from openfire import UserNotFoundException, RequestNotAuthorisedException
import csv
from collections import defaultdict
from pyvirtualdisplay import Display


def call_display_headless_browser():
    #os.environ['DISPLAY'] = ':99'
    display = Display(visible=0, size =(800,600))
    display.start()
   
def get_result_folder_name():
    resultpath = properties.Results
    result_file = os.path.join(resultpath, 'result_path.txt')
    f = open(result_file, 'r')
    file_name = f.readline() # always going to be one line only
    return file_name


#This function sets python path
def setpythonpath():
    cm_dir = properties.cm_path
    os.chdir(cm_dir)
    BASEDIR = os.getcwd()
    pythonpathfile = open("setpythonpath", "rb")
    for line in pythonpathfile:
        if "export PYTHONPATH" in line:
            newline = line.replace("$BASEDIR", BASEDIR)
    path = newline.split('=')
    envar = path[1]
    envar = envar.replace("\n", "")
    os.environ["PYTHONPATH"] = envar
    path = os.popen("echo $PYTHONPATH").read()


def add_xmpp_jid(jid):
    #Get xmpp server url from properties.py file
    xmppServer = properties.xmppServerUrl
    #Login to the xmpp server
    api = UserService(xmppServer, "skAljQTm43929-49sdakl")
    try:
        #Add users from the input csv file
        userAddReturnValue = api.add_user(jid, "skAljQTm43929-49sdakl")
        print "User " + jid + " added successfully!!"
        #print userAddReturnValue
    except UserAlreadyExistsException:
        print "User " + jid + " already exists!"
    except UserNotFoundException:
        print "User " + jid + " not found!!"
    except InvalidResponseException:
        print "Invalid request"
    except RequestNotAuthorisedException:
        print "Request is not authorized"


#Function to get ap's jid
def get_ap_jid(ap_ip):
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(ap_ip, username='root',
                    password='password')
        #Get ap jid from its devicename on the ap
        command = ("/opt/accelera/bin/devicename-get | sed 's?:?-?g'")
        (stdin, stdout, stderr) = ssh.exec_command(command)
        ap_jid = stdout.read()
        print "Ap's jid is: " + ap_jid
        ssh.close()
        return ap_jid


def get_var_details():
    columns = defaultdict(list)
    var_file = os.path.join(properties.input_file_path, properties.var_csv_file)
    with open(var_file, "rU") as f:
        reader = csv.DictReader(f)
        for row in reader:
            for (k, v) in row.items():
                columns[k].append(v)

#     print(columns['var_business_name'])
#     print(columns['street_addres_1'])
#     print(columns['street_addres_2'])
#     print(columns['city'])
#     print(columns['state'])
#     print(columns['zip'])
#     print(columns['country'])
#     print(columns['first_name'])
#     print(columns['last_name'])
#     print(columns['email'])
#     print(columns['password'])
#     print(columns['confirm_password'])
    return columns


def get_bytes_rx_client_stats():
    client_stats_path = os.path.join(properties.input_file_path, properties.client_stats_file)
    client_stats_file = open(client_stats_path, 'r')
    for eachLine in client_stats_file:
        if "rx bytes" in eachLine:
            bytes_rx_line = eachLine.split("rx bytes")
            bytes_rx = bytes_rx_line[1]
            bytes_rx = bytes_rx_line[1].split()
            bytes_rx = bytes_rx[1].replace("#", "")
            bytes_rx = bytes_rx.replace("\"", "")
            return bytes_rx 
        

def get_bytes_tx_client_stats():
    client_stats_path = os.path.join(properties.input_file_path, properties.client_stats_file)
    client_stats_file = open(client_stats_path, 'r')
    for eachLine in client_stats_file:
        if "tx bytes" in eachLine:
            bytes_tx_line = eachLine.split("tx bytes")
            bytes_tx = bytes_tx_line[1]
            bytes_tx = bytes_tx_line[1].split()
            bytes_tx = bytes_tx[1].replace("#", "")
            bytes_tx = bytes_tx.replace("\"", "")
            return bytes_tx


def get_rssi_client_stats():
    client_stats_path = os.path.join(properties.input_file_path, properties.client_stats_file)
    client_stats_file = open(client_stats_path, 'r')
    for eachLine in client_stats_file:
        if "signal avg" in eachLine:
            rssi_line = eachLine.split("signal avg")
            rssi = rssi_line[1]
            rssi = rssi_line[1].split()
            return rssi[1]
                            
def get_client_stats(required_stat):
    client_stats_path = os.path.join(properties.input_file_path, properties.client_stats_file)
    client_stats_file = open(client_stats_path, 'r')
    for eachLine in client_stats_file:
        if required_stat == "bytes_rx": 
            if "rx bytes" in eachLine:
                bytes_rx_line = eachLine.split("rx bytes")
                bytes_rx = bytes_rx_line[1]
                bytes_rx = bytes_rx_line[1].split()
                bytes_rx = bytes_rx[1].replace("#", "")
                bytes_rx = bytes_rx.replace("\"", "")
                return bytes_rx 
        
        elif required_stat == "bytes_tx":
            if "tx bytes" in eachLine:
                bytes_tx_line = eachLine.split("tx bytes")
                bytes_tx = bytes_tx_line[1]
                bytes_tx = bytes_tx_line[1].split()
                bytes_tx = bytes_tx[1].replace("#", "")
                bytes_tx = bytes_tx.replace("\"", "")
                return bytes_tx
        
        elif required_stat == "rssi":
            if "signal avg" in eachLine:
                rssi_line = eachLine.split("signal avg")
                rssi = rssi_line[1]
                rssi = rssi_line[1].split()
                return rssi[1]
            
def get_client_name():
    client_stats_path = os.path.join(properties.input_file_path, properties.client_stats_file)
    client_stats_file = open(client_stats_path, 'r')
    for eachLine in client_stats_file:
            if "Station" in eachLine:
                client_name_line = eachLine.split("Station")
                client_name = client_name_line[1]
                client_name = client_name_line[1].split()
                client_name = client_name[0]
                #Client name is stored as upper case with dashes
                #having Intel_Corporate at the beginning by static stats
                client_name = client_name.upper()
                client_name = client_name.replace(':', '-')
                return client_name
 
def get_original_client_name():
    client_stats_path = os.path.join(properties.input_file_path, properties.client_stats_file)
    client_stats_file = open(client_stats_path, 'r')
    for eachLine in client_stats_file:
            if "Station" in eachLine:
                client_name_line = eachLine.split("Station")
                client_name = client_name_line[1]
                client_name = client_name_line[1].split()
                client_name = client_name[0]
                return client_name

def get_client_count():
    essid_stats_path = os.path.join(properties.input_file_path, properties.essid_stats_file)
    essid_stats_file = open(essid_stats_path, 'r')
    for eachLine in essid_stats_file:
        if "Number of Clients" in eachLine:
            client_count_line = eachLine.split("Number of Clients")
            client_count = client_count_line[0]
            client_count = client_count_line[0].split()
            return client_count[1]


def get_ap_stats(required_stat):
    essid_stats_path = os.path.join(properties.input_file_path, properties.essid_stats_file)
    essid_stats_file = open(essid_stats_path, 'r')
    for eachLine in essid_stats_file:
        if required_stat == "bytes_rx": 
            if "Bytes Rx" in eachLine:
                bytes_rx_line = eachLine.split("Bytes Rx")
                bytes_rx = bytes_rx_line[0]
                bytes_rx = bytes_rx_line[0].split()
                return bytes_rx[1] 
        
        elif required_stat == "bytes_tx":
            if "Bytes Tx" in eachLine:
                bytes_tx_line = eachLine.split("Bytes Tx")
                bytes_tx = bytes_tx_line[0]
                bytes_tx = bytes_tx_line[0].split()
                return bytes_tx[1]


def get_radio_utilization():
    radio_stats_path = os.path.join(properties.input_file_path, properties.radio_stats_file)
    radio_stats_file = open(radio_stats_path, 'r')
    for eachLine in radio_stats_file:
        if "Channel Busy" in eachLine:
            channel_busy_line = eachLine.split("Channel Busy")
            channel_busy = channel_busy_line[0]
            channel_busy = channel_busy_line[0].split()
            return str(channel_busy[1]) + ("%")


def caluclate_apdetails_page_client_usage_kbps(bytes_rx, bytes_tx):
    #Usage conversion minutely data and hence for kbps divided by 1000*60
    client_usage_kbps = (int(bytes_rx) + int(bytes_tx))*8/(1000*60)
    return int(client_usage_kbps)


def caluclate_apdetails_page_traffic_mbps(bytes_rx, bytes_tx):
    #Note here we multiplu bytes_rx and bytes_tx by 2 becuase there are 2 radios 24G and 5G
    #Traffic conversion minutely data and hence for mbps divided by 1000*1000*60
    ap_traffic_mbps = 2*(int(bytes_rx) + int(bytes_tx))*8/float(1000*1000*60)
    return str(ap_traffic_mbps) + (" Mbps")


def caluclate_loc_dashboard_top5devices_traffic_kbps(bytes_rx, bytes_tx):
    #Usage conversion minutely data and hence for kbps divided by 1000*60
    top5devices_traffic_kbps = (int(bytes_rx) + int(bytes_tx))*8/(1000*60)
    return str(top5devices_traffic_kbps)+ (" Kbps")


def caluclate_loc_dashboard_top5ssids_traffic_kbps(bytes_rx, bytes_tx):
    #Note here we multiplu bytes_rx and bytes_tx by 2 becuase there are 2 radios 24G and 5G
    #Usage conversion minutely data and hence for kbps divided by 1000*60
    top5ssids_traffic_kbps = (int(bytes_rx) + int(bytes_tx))*8*60*2/(1000*3600)
    return str(top5ssids_traffic_kbps)+ (" Kbps")


def caluclate_loc_dashboard_top5aps_traffic_kbps(bytes_rx, bytes_tx):
    #Note here we multiplu bytes_rx and bytes_tx by 2 becuase there are 2 radios 24G and 5G
    #Usage conversion minutely data and hence for kbps divided by 1000*60
    top5aps_traffic_kbps = (int(bytes_rx) + int(bytes_tx))*8*60*2/(1000*3600)
    return str(top5aps_traffic_kbps)+ (" Kbps")


def caluclate_loc_dashboard_traffic_mbps(bytes_rx, bytes_tx):
    #Note here we multiplu bytes_rx and bytes_tx by 2 becuase there are 2 radios 24G and 5G
    #Traffic conversion minutely data and hence for mbps divided by 1000*1000*60
    ap_traffic_mbps = 2*(int(bytes_rx) + int(bytes_tx))*8*60/float(1000*1000*3600)
    return str(ap_traffic_mbps) + (" Mbps")


def caluclate_cust_dashboard_top5devices_traffic_kbps(bytes_rx, bytes_tx):
    #Usage conversion minutely data and hence for kbps divided by 1000*60
    top5devices_traffic_kbps = (int(bytes_rx) + int(bytes_tx))*8/(1000*60)
    return str(top5devices_traffic_kbps)+ (" Kbps")


def caluclate_cust_dashboard_top5ssids_traffic_kbps(bytes_rx, bytes_tx):
    #Note here we multiplu bytes_rx and bytes_tx by 2 becuase there are 2 radios 24G and 5G
    #Usage conversion minutely data and hence for kbps divided by 1000*60
    top5ssids_traffic_kbps = (int(bytes_rx) + int(bytes_tx))*8*60*2/(1000*3600)
    return str(top5ssids_traffic_kbps)+ (" Kbps")


def caluclate_cust_dashboard_top5aps_traffic_kbps(bytes_rx, bytes_tx):
    #Note here we multiplu bytes_rx and bytes_tx by 2 becuase there are 2 radios 24G and 5G
    #Usage conversion minutely data and hence for kbps divided by 1000*60
    top5aps_traffic_kbps = (int(bytes_rx) + int(bytes_tx))*8*60*2/(1000*3600)
    return str(top5aps_traffic_kbps)+ (" Kbps")


def get_no_of_virtual_ap():
    virtual_ap_file = os.path.join(properties.input_file_path, properties.virtual_ap_csv_file)
    with open(virtual_ap_file, 'rb') as f:
        reader = csv.reader(f)
        rownum = 0
        for row in reader:
            #print row
            rownum +=1
            #print "no, of rows " +str(rownum)
        return rownum
    
    
def caluclate_cust_dashboard_top5ssids_virtualAPs_traffic_kbps(bytes_rx, bytes_tx):
    #Note here we multiplu bytes_rx and bytes_tx by 2 becuase there are 2 radios 24G and 5G
    #Usage conversion minutely data and hence for kbps divided by 1000*60
    expected_no_aps = get_no_of_virtual_ap()
    top5ssids_traffic_kbps = (int(bytes_rx) + int(bytes_tx))*8*60*2/(1000*3600)
    top5ssids_traffic_kbps = top5ssids_traffic_kbps*expected_no_aps
    return str(top5ssids_traffic_kbps)+ (" Kbps")


def caluclate_loc_dashboard_virtualAps_traffic_mbps(bytes_rx, bytes_tx):
    #Note here we multiplu bytes_rx and bytes_tx by 2 becuase there are 2 radios 24G and 5G
    #Traffic conversion minutely data and hence for mbps divided by 1000*1000*60
    ap_traffic_mbps = 2*(int(bytes_rx) + int(bytes_tx))*8*60/float(1000*1000*3600)
    expected_no_aps = get_no_of_virtual_ap()
    ap_traffic_mbps = ap_traffic_mbps*expected_no_aps
    return str(ap_traffic_mbps) + (" Mbps")