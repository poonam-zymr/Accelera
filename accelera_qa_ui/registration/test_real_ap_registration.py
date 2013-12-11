import os
import subprocess
import time
import properties
import paramiko
from utils import utils, db, results
import unittest


class TestValidRealAPRegistration(unittest.TestCase):

    def _1_start_runworkers(self):
        utils.setpythonpath()
        time.sleep(5)
        workerstdoutfile = os.path.join(properties.outputFileLocation,
                                        "realap-runworkerstdout.txt")
        workerstderrfile = os.path.join(properties.outputFileLocation,
                                        "realap-runworkerstderr.txt")
        stdout = open(workerstdoutfile, "wb")
        stderr = open(workerstderrfile, "wb")
        # Navigate to the mom directory
        mom_dir = properties.mom_path
        os.chdir(mom_dir)
        print os.getcwd()
        print "Starting workers"
        # Start the runwokers process
        subprocess.Popen(['./runworkers'], stdout=stdout, stderr=stderr)
        time.sleep(120)

    def _2_start_apmanager(self):
        utils.setpythonpath()
        time.sleep(5)
        apmanagerstdoutfile = os.path.join(properties.outputFileLocation,
                                           "realap-apmanagerstdout.txt")
        apmanagerstderrfile = os.path.join(properties.outputFileLocation,
                                           "realap-apmanagerstderr.txt")
        stdout = open(apmanagerstdoutfile, "wb")
        stderr = open(apmanagerstderrfile, "wb")

        # Navigate to the apmanager directory
        apmanager_dir = properties.apmanager_path
        os.chdir(apmanager_dir)
        print os.getcwd()
        print "Starting apmanager"
        apmanager = properties.apmanager
        subprocess.Popen(['./apmctl.py', apmanager, 'start'], stdout=stdout,
                         stderr=stderr)
        time.sleep(120)

    def _3_real_ap_registration(self):
        apmanager_path = ("%s%s" % (properties.apmanager,
                                    properties.xmppdomain))
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(properties.real_ap, username='root', password='password')
        xmpp_client_filepath = os.path.join(properties.xmpp_client_path,
                                            "xmpp_client.conf")
        print ("Configuring AP %s with apmanager %s" % (properties.real_ap,
                                                         properties.apmanager))
        command = ("cd %s;sed -i 's/XMPP_REGISTER=.*/XMPP_REGISTER='%s'/g' %s"
                   % (properties.xmpp_client_path, apmanager_path,
                      xmpp_client_filepath))
        ssh.exec_command(command + ' > /dev/null 2>&1 &')
        time.sleep(20)
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(properties.real_ap, username='root', password='password')
        print "Rebooting AP."
        reboot_command = "reboot"
        ssh.exec_command(reboot_command)
        time.sleep(180)
        # Verify if the ap entry is made in the database
        db.search_ap_in_new_ap_collection(properties.apjid)


def test_generate_result():
    suite = unittest.TestSuite()
    suite.addTest(TestValidRealAPRegistration("_1_start_runworkers"))
    suite.addTest(TestValidRealAPRegistration("_2_start_apmanager"))
    suite.addTest(TestValidRealAPRegistration("_3_real_ap_registration"))
    print suite
    print __file__
    results.run(suite, __file__)
