#!/usr/bin/env python3
# PY test script file name must start with "test" to allow automatic recognition by PyCharm
# import
from unittest import TestCase
from time import sleep
from pythoncommontools.daemonCommon.daemonCommon import start, stop, status, Status, getPidFileName, Action, readPidFile
from test.daemonCommon.dummyDaemon import scriptName, scriptFullPath, statusFileFullPath
from os.path import isfile
from os import remove
# define test
class testDaemonCommon(TestCase):
    waitTime = 2
    pidFileName = getPidFileName(scriptName)
    # test process life cycle
    def testProcessLifeCycle(self):
        # start/status/stop a correct process
        '''INFO : we test 2 commands :
         - tail -f /dev/null
         - top
         '''
        for command in {(("tail", "-f", "/dev/null")),"top"} :
            pid = start(command)
            self.assertGreater(pid,0,"correct process did not start")
            actualStatus = status(pid)
            self.assertIn(actualStatus,{Status.RUNNING.value,Status.SLEEPING.value,Status.ZOMBIE.value},"correct process status not as expected")
            stop(pid)
            sleep(testDaemonCommon.waitTime)
        # status a stopped process
        actualStatus = status(pid)
        self.assertEqual(actualStatus,Status.ZOMBIE.value,"stopped process status not as expected")
        # re-stop a process
        stop(pid)
        # start/status/stop a incorrect process
        pid = start("tail_")
        self.assertGreater(pid,0,"incorrect process did not start")
        sleep(testDaemonCommon.waitTime)
        actualStatus = status(pid)
        self.assertIn(actualStatus,{Status.ZOMBIE.value,Status.SLEEPING.value},"incorrect process status not as expected")
        stop(pid)
        sleep(testDaemonCommon.waitTime)
        # status/stop a wrong PID
        for pid in {-1,0}:
            actualStatus = status(pid)
            self.assertIsNone(actualStatus,"wrong PID process status not as expected")
            stop(pid)
        pass
    # test daemonization
    def testDaemonization(self):
        # WARNING : this package must be installed using pip to run this test
        testDaemonCommon.cleanFiles()
        # (re-)start daemon
        expectedPidsNumber = 2
        _ = 0
        pids = set()
        while (_<expectedPidsNumber):
            start("python3",scriptFullPath, Action.START.value)
            sleep(testDaemonCommon.waitTime)
            self.assertTrue(isfile(testDaemonCommon.pidFileName),"PID file is not written")
            pid = readPidFile(scriptName)
            self.assertGreater(pid, 0, "process did not start")
            pids.add(pid)
            _ += 1
        self.assertEqual(len(pids),expectedPidsNumber,"PID number was not reset")
        # get daemon status
        start("python3", scriptFullPath, Action.STATUS.value)
        sleep(testDaemonCommon.waitTime)
        with open(statusFileFullPath, 'r') as statusFile:
            status = statusFile.read()
        statusFile.closed
        self.assertEqual(status, Status.RUNNING.value, "status is not " + Status.RUNNING.value)
        # (re-)stop daemon
        _ = 0
        while (_<expectedPidsNumber):
            start("python3",scriptFullPath, Action.STOP.value)
            sleep(testDaemonCommon.waitTime)
            self.assertFalse(isfile(testDaemonCommon.pidFileName),"PID file is not erased")
            _ += 1
        # re-get daemon status
        start("python3", scriptFullPath, Action.STATUS.value)
        sleep(testDaemonCommon.waitTime)
        with open(statusFileFullPath, 'r') as statusFile:
            status = statusFile.read()
        statusFile.closed
        self.assertEqual(status, "None", "status is not erased")
        # test wrong daemon
        wrongDaemon = "wrong.pypy"
        start("python3", wrongDaemon, Action.START.value)
        sleep(testDaemonCommon.waitTime)
        self.assertFalse(isfile(testDaemonCommon.pidFileName), "PID file is written")
        start("python3", wrongDaemon, Action.STATUS.value)
        sleep(testDaemonCommon.waitTime)
        with open(statusFileFullPath, 'r') as statusFile:
            status = statusFile.read()
        statusFile.closed
        self.assertEqual(status, "None", "status is " + status)
        start("python3", wrongDaemon, Action.STOP.value)
        sleep(testDaemonCommon.waitTime)
        self.assertFalse(isfile(testDaemonCommon.pidFileName), "PID file is created")
        # remove PID file
        testDaemonCommon.cleanFiles()
        pass
    @staticmethod
    def cleanFiles():
        if (isfile(testDaemonCommon.pidFileName)):
            remove(testDaemonCommon.pidFileName)
        if (isfile(statusFileFullPath)):
            remove(statusFileFullPath)
    pass
pass
