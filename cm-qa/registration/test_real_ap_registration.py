import os
import subprocess
import time
import properties
import paramiko
from utils import utils, db, results
import unittest


class TestValidRealAPRegistration(unittest.TestCase):

    def _1_real_ap_registration(self):
        apmanager = properties.apmanager_jid
        utils.add_xmpp_jid(apmanager)
 
        apmanager_path = ("%s%s" % (properties.apmanager_jid,
                                    properties.xmppdomain))
        #Get the ap's jid
        ap_jid = utils.get_ap_jid(properties.real_ap_ip)
        print "AP jid return value is: " + ap_jid
        ap_jid = ap_jid.strip()
 
        utils.add_xmpp_jid(ap_jid)
 
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(properties.real_ap_ip, username='root',
                    password='password')
        xmpp_client_filepath = os.path.join(properties.xmpp_client_path,
                                            "xmpp_client.conf")
        print ("Configuring AP %s with apmanager %s" % (properties.real_ap_ip,
                                                    properties.apmanager_jid))
        command = ("cd %s;sed -i 's/XMPP_REGISTER=.*/XMPP_REGISTER='%s'/g' %s"
                   % (properties.xmpp_client_path,
                    apmanager_path, xmpp_client_filepath))
        ssh.exec_command(command + ' > /dev/null 2>&1 &')
        time.sleep(20)
 
        #Reboot the AP after changing xmpp_client
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(properties.real_ap_ip, username='root',
                    password='password')
        print "Rebooting AP."
        reboot_command = "reboot"
        ssh.exec_command(reboot_command)
        time.sleep(180)
        # Verify if the ap entry is made in the database
        db.search_ap_in_new_ap_collection(ap_jid)
         
        #Enabling wifi on both radios
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(properties.real_ap_ip, username='root', password='password')
        wifi_cmd_0 = 'uci set wireless.@wifi-device[0].disabled=0'                            
        wifi_cmd_1 = 'uci set wireless.@wifi-device[1].disabled=0'
        wifi_commit_cmd = 'uci commit wireless'
        wifi_cmd = 'wifi'
        print "Enabling wifi radios"
        ssh.exec_command(wifi_cmd_0)
        ssh.exec_command(wifi_cmd_1)
        ssh.exec_command(wifi_commit_cmd)
        ssh.exec_command(wifi_cmd)
        time.sleep(10)

def test_generate_result():
    suite = unittest.TestSuite()
    suite.addTest(TestValidRealAPRegistration("_1_real_ap_registration"))
    print suite
    print __file__
    results.run(suite, __file__)
