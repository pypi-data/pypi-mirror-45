#!/usr/bin/env python3
# import
from pythoncommontools.daemonCommon.daemonCommon import startSingleInstance, stopSingleInstance, statusSingleInstance, daemonize, pidDirectory
from os.path import basename, extsep
# global initialization
scriptFullPath = __file__
scriptName = basename(__file__).split(extsep)[0]
statusFileFullPath = pidDirectory + scriptName + extsep + "status"
# custom methods
def customStart():
    # start single instance
    startSingleInstance(scriptName)
    # dummy infinite loop
    while(True):pass
def customStop():
    stopSingleInstance(scriptName)
def customStatus():
    status = statusSingleInstance(scriptName)
    with open(statusFileFullPath, 'w') as statusFile:
        statusFile.write(str(status))
    statusFile.closed
# run script
if __name__ == "__main__" :
    daemonize(customStart,customStop,customStatus)
    pass
pass
