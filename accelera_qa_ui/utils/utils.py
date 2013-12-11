import properties
import os
import time
import subprocess
import paramiko


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
