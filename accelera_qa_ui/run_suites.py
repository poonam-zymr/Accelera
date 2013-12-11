import unittest
import sys
import os
import properties
import shutil
from utils import results

def run_suite():
    resultdir = properties.Results 
    curdir = os.getcwd()
    suitefile = os.path.join(curdir, 'suite.conf')
    suites = []
    if os.path.exists(suitefile):
        fh = open(suitefile, 'r')
        for line in fh:
            if " " not in line and "#" not in line:
                print line
                line = line.replace("\n", "")
                line = line.replace("\t", "")
                line = line.replace("\r", "")
                line = line.replace(" ", "")
                line = line.lower()
                suites.append(line)
    configfiles = [0]*(len(suites))
    for dirname,dirs,files in os.walk(curdir):
        for file in files:
            if 'config.ini' in file:
                suitepath = os.path.split(dirname)
                suitename = suitepath[1]   
                suitename = suitename.lower()
                if suitename in suites:
                    index = suites.index(suitename)
                    configpath = os.path.join(dirname,file)
                    configfiles.pop(index)
                    configfiles.insert(index, configpath)
    for each in configfiles:
        sourcedir = os.path.dirname(each)
        os.chdir(sourcedir)
        command = ("nosetests -c %s" % each)
        print command
        os.system(command)
    os.chdir(curdir)
run_suite()
