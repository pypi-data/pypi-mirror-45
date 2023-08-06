# coding=utf-8
# imports
from argparse import ArgumentParser
from enum import unique, Enum
from os import kill, P_NOWAIT, spawnlp, getpid, remove
from os.path import sep, extsep, isfile
from signal import SIGTERM
from psutil import Process , pid_exists
from tempfile import gettempdir
# global initialization
pidExtension = extsep + "pid"
pidDirectory = gettempdir() + sep
# action
@unique
class Action(Enum):
    START = "start"
    STOP = "stop"
    STATUS = "status"
# status
@unique
class Status(Enum):
    RUNNING = "running"
    SLEEPING = "sleeping"
    ZOMBIE = "zombie"
    # TODO : populate if needed, see 'ps' command help for detailed value list
# common daemon
def startSingleInstance(scriptName):
    # write & return PID
    pid = writePidFile(scriptName)
    return pid
def stopSingleInstance(scriptName):
    pid = readPidFile(scriptName)
    stop(pid)
    pidFileName = getPidFileName(scriptName)
    if (isfile(pidFileName)):
        remove(pidFileName)
def statusSingleInstance(scriptName):
    pid = readPidFile(scriptName)
    pidStatus = status(pid)
    return pidStatus
def readPidFile(scriptName):
    pid = 0
    pidFileName = getPidFileName(scriptName)
    if (isfile(pidFileName)) :
        with open(pidFileName, 'r') as pidFile:
            pid = pidFile.read()
        pidFile.closed
        pid = int(pid)
    return pid
def writePidFile(scriptName):
    pidFileName = getPidFileName(scriptName)
    pid = getpid()
    with open(pidFileName, 'w') as pidFile:
        pidFile.write(str(pid))
    pidFile.closed
    return pid
def getPidFileName(scriptName):
    pidFileName = pidDirectory + scriptName + pidExtension
    return pidFileName
'''
manage a python script as a daemon
3 action are possible : start, stop and status
just give :
 - a function for each action
 - the current action as parameter
'''
def daemonize ( customStart, customStop, customStatus ):
    # parse parameters
    parser = ArgumentParser()
    parser.add_argument( "action", help = "start|stop|status", type = str )
    args = parser.parse_args()
    # start
    if args.action == Action.START.value:
        # stop running instance be fore start
        customStop()
        customStart()
    # stop
    elif args.action == Action.STOP.value:
        customStop()
    # status
    elif args.action == Action.STATUS.value:
        customStatus()
    # bad action
    else:
        raise Exception ( "Unknown command" )
    pass
'''
start a process regarding command (& arguments) and return PID
example :
 - call : start("tail", "-f", "/dev/null") # for the command : tail -f /dev/null
 - return : pid=123
'''
def start ( commandName, *commandArguments ):
    # parse arguments
    pid = spawnlp(P_NOWAIT, commandName, commandName, *commandArguments)
    return pid
'''
stop a process with given PID
example :
 - call : stop(123)
'''
def stop( pid ):
    if pid  and pid_exists(pid):
        kill(pid, SIGTERM)
'''
get a process status with given PID
example :
 - call : status(123)
 - return : runnable (see 'ps' command help for detailed value list)
'''
def status( pid ):
    # initialize state set
    status = None
    if pid  and pid_exists(pid):
        process = Process(pid)
        status = process.status()
    return status
