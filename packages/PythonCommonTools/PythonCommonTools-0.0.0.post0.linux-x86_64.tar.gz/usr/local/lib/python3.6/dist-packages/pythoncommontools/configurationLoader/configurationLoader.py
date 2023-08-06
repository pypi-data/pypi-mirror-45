# coding=utf-8
# imports
from configparser import ConfigParser
'''
HELP : to use this feature :
 - create a configuration file
   an example is available at : pythoncommontools/logger/pythoncommontools.conf.sample
   generic format :
      [SECTION]
      KEY = VALUE
   example :
      [default]
      ServerAliveInterval = 45
 - code to use :
   from pythoncommontools.configurationLoader import configurationLoader
   loadedConfiguration = configurationLoader.loadConfiguration(CONFIGURATION_FILE)
   #loadedConfiguration[SECTION].get(KEY)
   loadedConfiguration[default].get(ServerAliveInterval) == "45"
 - other methods : getint(), getfloat() and getboolean()
 - see : https://docs.python.org/3/library/configparser.html
'''
# read configuration
def loadConfiguration(configurationFilePath):
    loadedConfiguration = ConfigParser()
    loadedConfiguration.read(configurationFilePath)
    return loadedConfiguration
