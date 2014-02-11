import os
import subprocess
import time
import properties
import paramiko
import unittest
from utils import utils, db, results

class TestEnableTestModeAP(unittest.TestCase):

    def enable_mode_ap(self):
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(properties.real_ap_ip, username='root',
                    password='password')
        print "Enabling test mode"
        stats_file_path = os.path.join(properties.xmpp_client_path,
                                            "stats_test_mode")
        try:
            #To enable test mode "stats_test_mode file on AP needs to have 1
            (stdin, stdout, stderr) = ssh.exec_command("echo 1 > %s" % (stats_file_path))
            #stdin, stdout, stderr = ssh.exec_command("stats_test_mode_enable")
        except SSHException, e:
            print e
        print stdout.readlines()
        ssh.close()
        time.sleep(5)
         
        client_stats_path = os.path.join(properties.input_file_path, properties.client_stats_file)
        radio_stats_path = os.path.join(properties.input_file_path, properties.radio_stats_file)
        essid_stats_path = os.path.join(properties.input_file_path, properties.essid_stats_file)
  
        server = properties.real_ap_ip
        username = "root"
        remotepath = properties.xmpp_client_path
        
        #Copy Test Stat files to AP
        ssh_cmd = 'sshpass -p password scp "%s" "%s@%s:%s"' % (client_stats_path, username, server, remotepath)
        os.system(ssh_cmd)
        ssh_cmd = 'sshpass -p password scp "%s" "%s@%s:%s"' % (radio_stats_path, username, server, remotepath)
        os.system(ssh_cmd)
        ssh_cmd = 'sshpass -p password scp "%s" "%s@%s:%s"' % (essid_stats_path, username, server, remotepath)
        os.system(ssh_cmd)
#         os.system('scp "%s" "%s@%s:%s"' % (client_stats_path, username, server, remotepath) )
#         os.system('scp "%s" "%s@%s:%s"' % (radio_stats_path, username, server, remotepath) )           
#         os.system('scp "%s" "%s@%s:%s"' % (essid_stats_path, username, server, remotepath) )
          
        time.sleep(15)


def test_generate_result():
    suite = unittest.TestSuite()
    suite.addTest(TestEnableTestModeAP("enable_mode_ap"))
    print suite
    print __file__
    results.run(suite, __file__)
