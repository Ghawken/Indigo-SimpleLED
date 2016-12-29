#! /usr/bin/env python2.6
# -*- coding: utf-8 -*-

"""
Author: GlennNZ

"""

import datetime
import time as t
import urllib2
import os
import shutil
import logging

from ghpu import GitHubPluginUpdater

try:
    import indigo
except:
    pass

# Establish default plugin prefs; create them if they don't already exist.
kDefaultPluginPrefs = {
    u'configMenuPollInterval': "300",  # Frequency of refreshes.
    u'configMenuServerTimeout': "15",  # Server timeout limit.
    # u'refreshFreq': 300,  # Device-specific update frequency
    u'showDebugInfo': False,  # Verbose debug logging?
    u'configUpdaterForceUpdate': False,
    u'configUpdaterInterval': 24,
    u'updaterEmail': "",  # Email to notify of plugin updates.
    u'updaterEmailsEnabled': False  # Notification of plugin updates wanted.
}


class Plugin(indigo.PluginBase):
    def __init__(self, pluginId, pluginDisplayName, pluginVersion, pluginPrefs):
        indigo.PluginBase.__init__(self, pluginId, pluginDisplayName, pluginVersion, pluginPrefs)

        pfmt = logging.Formatter('%(asctime)s.%(msecs)03d\t[%(levelname)8s] %(name)20s.%(funcName)-25s%(msg)s', datefmt='%Y-%m-%d %H:%M:%S')
        self.plugin_file_handler.setFormatter(pfmt)

        try:
            self.logLevel = int(self.pluginPrefs[u"logLevel"])
        except:
            self.logLevel = logging.INFO

        self.indigo_log_handler.setLevel(self.logLevel)
        self.logger.debug(u"logLevel = " + str(self.logLevel))

        self.debugLog(u"Initializing plugin.")

        self.updater = GitHubPluginUpdater(self)
        self.configUpdaterInterval = self.pluginPrefs.get('configUpdaterInterval', 24)
        self.configUpdaterForceUpdate = self.pluginPrefs.get('configUpdaterForceUpdate', False)



    def __del__(self):

        self.debugLog(u"__del__ method called.")
        indigo.PluginBase.__del__(self)

    def closedPrefsConfigUi(self, valuesDict, userCancelled):

        self.debugLog(u"closedPrefsConfigUi() method called.")

        if userCancelled:
            self.debugLog(u"User prefs dialog cancelled.")

        if not userCancelled:

            self.debugLog(u"User prefs saved.")


        return True

    # Start 'em up.
    def deviceStartComm(self, dev):

         self.debugLog(u"deviceStartComm() method called.")


    # Shut 'em down.
    def deviceStopComm(self, dev):

        self.debugLog(u"deviceStopComm() method called.")
        indigo.server.log(u"Stopping device: " + dev.name)

    def forceUpdate(self):
        self.updater.update(currentVersion='0.0.0')

    def checkForUpdates(self):
        if self.updater.checkForUpdate() == False:
            indigo.server.log(u"No Updates are Available")

    def updatePlugin(self):
        self.updater.update()

    def DOESNTEXISTrunConcurrentThread(self):

        try:


            while True:


                self.debugLog(u" ")

                for dev in indigo.devices.itervalues('self'):

                    self.debugLog(u"MainLoop:  {0}:".format(dev.name))


                self.sleep(60)

        except self.StopThread:
            self.debugLog(u'Restarting/or error. Stopping thread.')
            pass

    def shutdown(self):

         self.debugLog(u"shutdown() method called.")

    def startup(self):

        self.debugLog(u"Starting Plugin. startup() method called.")

        # See if there is a plugin update and whether the user wants to be notified.
        try:
            if self.configUpdaterForceUpdate:
                self.updatePlugin()

            else:
                self.checkForUpdates()
            self.sleep(1)
        except Exception as error:
            self.errorLog(u"Update checker error: {0}".format(error))

    def validatePrefsConfigUi(self, valuesDict):

        self.debugLog(u"validatePrefsConfigUi() method called.")

        error_msg_dict = indigo.Dict()

        # self.errorLog(u"Plugin configuration error: ")

        return True, valuesDict



    def setStatestonil(self, dev):

         self.debugLog(u'setStates to nil run')

    def speakCallerNumber(self,pluginAction):

        self.logger.debug(str(pluginAction))

        command = pluginAction.props.get('ledEffect', False)

        devId = pluginAction.deviceId
        dev = indigo.devices[devId]
        zwMajor = int(dev.ownerProps['zwAppVersMajor'])
        zwMinor = int(dev.ownerProps['zwAppVersMinor'])
        self.logger.debug(u'Device Model is:'+str(dev.model))

        self.logger.debug(u'Firmware equals:'+str(zwMajor) + "."+str(zwMinor))

        if not command:
            self.logger.error(u"No Remote Button was specified in action for \"" + dev.name + "\"")
            return False
        if not indigo.zwave.isEnabled():
            self.logger.error(u'Z-Wave Interface has to be enabled')
            return False

        if dev.model == 'RGBW Controller (FGRGBWM)':  #Double check!
            if command=="Rainbow":
                self.logger.debug(u'Rainbow Set on device:'+str(dev.name))
                indigo.zwave.sendConfigParm(device=indigo.devices[devId],paramIndex=72,paramSize=1,paramValue=8)
            if command=="Fireplace":
                self.logger.debug(u'FirePlace Set on device:'+str(dev.name))
                indigo.zwave.sendConfigParm(device=indigo.devices[devId],paramIndex=72,paramSize=1,paramValue=6)
            if command=="Storm":
                self.logger.debug(u'Storm Set on device:'+str(dev.name))
                indigo.zwave.sendConfigParm(device=indigo.devices[devId],paramIndex=72,paramSize=1,paramValue=7)
            if command=="Aurora":
                self.logger.debug(u'Aurora Set on device:'+str(dev.name))
                indigo.zwave.sendConfigParm(device=indigo.devices[devId],paramIndex=72,paramSize=1,paramValue=9)
            if command=="LPD":
                self.logger.debug(u'LPD Set on device:'+str(dev.name))
                indigo.zwave.sendConfigParm(device=indigo.devices[devId],paramIndex=72,paramSize=1,paramValue=10)
            if command=="Default":
                self.logger.debug(u'Default Set on device:'+str(dev.name))
                indigo.zwave.sendConfigParm(device=indigo.devices[devId],paramIndex=72,paramSize=1,paramValue=1)


        if dev.model == 'RGBW LED Bulb (ZW098)':
            if command=="Rainbow-Fast":
                self.logger.debug(u'Rainbow-Fast Set on device:'+str(dev.name))
                indigo.zwave.sendConfigParm(device=indigo.devices[devId],paramIndex=37,paramSize=4,paramValue=65537)
            if command == "Default":
                self.logger.debug(u'Default Set on device:'+str(dev.name))
                indigo.zwave.sendConfigParm(device=indigo.devices[devId],paramIndex=37,paramSize=4,paramValue=3840)

        return

    def uiEffects(self, filter, valuesDict, typeId, deviceId):

        theList = list()
        device = indigo.devices[deviceId]
        #self.logger.debug(u'Device Details'+str(device))
        #self.logger.debug(str(device.model))

        if device.model =='RGBW Controller (FGRGBWM)':
            self.logger.debug(str(device.model))
            theList.append("Rainbow")
            theList.append("Fireplace")
            theList.append("Storm")
            theList.append("Aurora")
            theList.append("LPD")
            theList.append("Default")


        if device.model == 'RGBW LED Bulb (ZW098)':
            self.logger.debug(str(device.model))
            #theList.append("Rainbow-Fast")  #
            theList.append("Default")


        return theList

    def refreshDataAction(self, valuesDict):
        """
        The refreshDataAction() method refreshes data for all devices based on
        a plugin menu call.
        """

        self.debugLog(u"refreshDataAction() method called.")
        self.refreshData()
        return True

    def refreshData(self):
        """
        The refreshData() method controls the updating of all plugin
        devices.
        """

        self.debugLog(u"refreshData() method called.")

        try:
            # Check to see if there have been any devices created.
            if indigo.devices.itervalues(filter="self"):

                self.debugLog(u"Updating data...")

                for dev in indigo.devices.itervalues(filter="self"):
                    self.refreshDataForDev(dev)

            else:
                indigo.server.log(u"No Enphase Client devices have been created.")

            return True

        except Exception as error:
            self.errorLog(u"Error refreshing devices. Please check settings.")
            self.errorLog(unicode(error.message))
            return False

    def refreshDataForDev(self, dev):

        if dev.configured:

            self.debugLog(u"Found configured device: {0}".format(dev.name))

            if dev.enabled:

                self.debugLog(u"   {0} is enabled.".format(dev.name))
                timeDifference = int(t.time() - t.mktime(dev.lastChanged.timetuple()))

            else:

                 self.debugLog(u"    Disabled: {0}".format(dev.name))


    def refreshDataForDevAction(self, valuesDict):
        """
        The refreshDataForDevAction() method refreshes data for a selected device based on
        a plugin menu call.
        """

        self.debugLog(u"refreshDataForDevAction() method called.")

        dev = indigo.devices[valuesDict.deviceId]

        self.refreshDataForDev(dev)
        return True


    def toggleDebugEnabled(self):
        """
        Toggle debug on/off.
        """

        self.debugLog(u"toggleDebugEnabled() method called.")
        if self.logLevel == logging.INFO:
             self.logLevel = logging.DEBUG

             self.indigo_log_handler.setLevel(self.logLevel)
             indigo.server.log(u'Set Logging to DEBUG')
        else:
            self.logLevel = logging.INFO
            indigo.server.log(u'Set Logging to INFO')
            self.indigo_log_handler.setLevel(self.logLevel)

        self.pluginPrefs[u"logLevel"] = self.logLevel
        return
