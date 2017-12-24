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
        self.logger.debug(u"logLevel = " + unicode(self.logLevel))

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

    def setLEDeffect(self,pluginAction):

        self.logger.debug(unicode(pluginAction))

        command = pluginAction.props.get('ledEffect', False)
        # A List of colours exists with ever device sent - so need to check device needs the list
        self.logger.debug(unicode(command))
        #   Get colours list
        # concert to int via map
        # sum to get total - which is parameter 38 for those that need it
        self.logger.debug(u'Setting colorsparam to default 2271560481')
        coloursparam = 2271560481
        if command in ['Choose-Colours-Fast','Choose-Colours-Slow']:
            self.logger.debug(u'Setting Colours and ColourParam based on selected colors')
            colourslist = []
            colourslist = pluginAction.props.get('Selectedcolours', 0)
            colourslist = map(int, colourslist)
            coloursparam = sum(colourslist)
            if coloursparam <= 0:
                coloursparam = 2271560481
            # If no colours selected - shouldn't run parameter 38 change
            # but set it to default in case it does
                self.logger.debug(u'Setting Colours Param to default')
            self.logger.debug(u'Selected Colours Parameter equals:'+unicode(coloursparam))
            self.logger.debug(unicode(colourslist))
        devId = pluginAction.deviceId
        dev = indigo.devices[devId]
        zwMajor = int(dev.ownerProps['zwAppVersMajor'])
        zwMinor = int(dev.ownerProps['zwAppVersMinor'])
        self.logger.debug(u'Device Model is:'+unicode(dev.model))
        self.logger.debug(u'Firmware equals:'+unicode(zwMajor) + "."+unicode(zwMinor))

        if not command:
            self.logger.error(u"No Command to Execute was specified in action for \"" + dev.name + "\"")
            return False
        if not indigo.zwave.isEnabled():
            self.logger.error(u'Z-Wave Interface has to be enabled')
            return False

        if dev.model == 'RGBW Controller (FGRGBWM)':  #Double check!
            if command=="Rainbow":
                self.logger.debug(u'Rainbow Set on device:'+unicode(dev.name))
                indigo.zwave.sendConfigParm(device=indigo.devices[devId],paramIndex=72,paramSize=1,paramValue=8)
            if command=="Fireplace":
                self.logger.debug(u'FirePlace Set on device:'+unicode(dev.name))
                indigo.zwave.sendConfigParm(device=indigo.devices[devId],paramIndex=72,paramSize=1,paramValue=6)
            if command=="Storm":
                self.logger.debug(u'Storm Set on device:'+unicode(dev.name))
                indigo.zwave.sendConfigParm(device=indigo.devices[devId],paramIndex=72,paramSize=1,paramValue=7)
            if command=="Aurora":
                self.logger.debug(u'Aurora Set on device:'+unicode(dev.name))
                indigo.zwave.sendConfigParm(device=indigo.devices[devId],paramIndex=72,paramSize=1,paramValue=9)
            if command=="LPD":
                self.logger.debug(u'LPD Set on device:'+unicode(dev.name))
                indigo.zwave.sendConfigParm(device=indigo.devices[devId],paramIndex=72,paramSize=1,paramValue=10)
            if command=="Default":
                self.logger.debug(u'Default Set on device:'+unicode(dev.name))
                indigo.zwave.sendConfigParm(device=indigo.devices[devId],paramIndex=72,paramSize=1,paramValue=1)

# add firmware check for Aeon Bulbs
        if dev.model == 'RGBW LED Bulb (ZW098)':
            if int(zwMinor)==4:   # select firmware 1.4
                if command=="Rainbow-Fast":
                    self.logger.debug(u'Rainbow-Fast Set on device:'+unicode(dev.name))
                    indigo.zwave.sendConfigParm(device=indigo.devices[devId],paramIndex=37,paramSize=4,paramValue=16782386)
                    # send the selected colours - so mode above and colour choice below.
                    indigo.zwave.sendConfigParm(device=indigo.devices[devId], paramIndex=38, paramSize=4,paramValue=coloursparam)
                if command == "Rainbow-Slow":
                    self.logger.debug(u'Rainbow-Slower Set on device:' + unicode(dev.name))
                    indigo.zwave.sendConfigParm(device=indigo.devices[devId],paramIndex=37,paramSize=4,paramValue=16782436)
                    #indigo.zwave.sendConfigParm(device=indigo.devices[devId], paramIndex=38, paramSize=4,paramValue=6291457)
                    # send the selected colours - so mode above and colour choice below.
                    indigo.zwave.sendConfigParm(device=indigo.devices[devId], paramIndex=38, paramSize=4, paramValue=coloursparam)
                if command == "Random-Fast":
                    self.logger.debug(u'Random-fast Set on device:' + unicode(dev.name))
                    indigo.zwave.sendConfigParm(device=indigo.devices[devId], paramIndex=37, paramSize=4,paramValue=50336818 )
                    # send the selected colours - so mode above and colour choice below.
                    indigo.zwave.sendConfigParm(device=indigo.devices[devId], paramIndex=38, paramSize=4,paramValue=coloursparam)
                if command == "Random-Slow":
                    self.logger.debug(u'Random-fast Set on device:' + unicode(dev.name))
                    indigo.zwave.sendConfigParm(device=indigo.devices[devId], paramIndex=37, paramSize=4, paramValue=50336868 )
                    #send the selected colours - so mode above and colour choice below.
                    indigo.zwave.sendConfigParm(device=indigo.devices[devId], paramIndex=38, paramSize=4,paramValue=coloursparam)
                if command == "Choose-Colours-Fast":
                    self.logger.debug(u'Random-fast Set on device:' + unicode(dev.name))
                    indigo.zwave.sendConfigParm(device=indigo.devices[devId], paramIndex=37, paramSize=4,paramValue=33559602  )
                    # send the selected colours - so mode above and colour choice below.
                    indigo.zwave.sendConfigParm(device=indigo.devices[devId], paramIndex=38, paramSize=4,paramValue=coloursparam)
                if command == "Choose-Colours-Slow":
                    self.logger.debug(u'Random-fast Set on device:' + unicode(dev.name))
                    indigo.zwave.sendConfigParm(device=indigo.devices[devId], paramIndex=37, paramSize=4, paramValue=33559652 )
                    #send the selected colours - so mode above and colour choice below.
                    indigo.zwave.sendConfigParm(device=indigo.devices[devId], paramIndex=38, paramSize=4,paramValue=coloursparam)

                if command == "Default":
                    self.logger.debug(u'Default Set on device:'+unicode(dev.name))
                    indigo.zwave.sendConfigParm(device=indigo.devices[devId],paramIndex=37,paramSize=4,paramValue=3840)
                    indigo.zwave.sendConfigParm(device=indigo.devices[devId], paramIndex=38, paramSize=4,paramValue=2271560481)
            if int(zwMinor)==5:   # select firmware 1.5 ?
                if command=="Rainbow-Fast":
                    self.logger.debug(u'Rainbow-Fast Set on device:'+unicode(dev.name))
                    indigo.zwave.sendConfigParm(device=indigo.devices[devId],paramIndex=37,paramSize=4,paramValue=23265374 )
                    # send the selected colours - so mode above and colour choice below.
                if command == "Rainbow-Slow":
                    self.logger.debug(u'Rainbow-Slower Set on device:' + unicode(dev.name))
                    indigo.zwave.sendConfigParm(device=indigo.devices[devId],paramIndex=37,paramSize=4,paramValue=23265310)
                if command == "Default":
                    self.logger.debug(u'Default Set on device:'+unicode(dev.name))
                    indigo.zwave.sendConfigParm(device=indigo.devices[devId],paramIndex=37,paramSize=4,paramValue=6488064)

        return

    def uiEffects(self, filter, valuesDict, typeId, deviceId):

        theList = []
        device = indigo.devices[deviceId]
        #self.logger.debug(u'Device Details'+unicode(device))
        #self.logger.debug(unicode(device.model))
        zwMajor = int(device.ownerProps['zwAppVersMajor'])
        zwMinor = int(device.ownerProps['zwAppVersMinor'])

        self.logger.debug(u'Device Model is:'+unicode(device.model))
        self.logger.debug(u'Firmware equals:'+unicode(zwMajor) + "."+unicode(zwMinor))

        if device.model =='RGBW Controller (FGRGBWM)':
            self.logger.debug(unicode(device.model))
            theList.append(("Rainbow","Rainbow"))
            theList.append(("Fireplace","Fireplace"))
            theList.append(("Storm","Storm"))
            theList.append(("Aurora","Aurora"))
            theList.append(("LPD","LPD"))
            theList.append(("Default","Default"))


        if device.model == 'RGBW LED Bulb (ZW098)':
            if int(zwMinor) == 4:  # only for firmware 1.4 versions
                self.logger.debug(unicode(device.model))
                theList.append(("Rainbow-Fast","Rainbow-Fast"))
                theList.append(("Rainbow-Slow","Rainbow-Slow"))
                theList.append(('Random-Fast','Random-Fast'))
                theList.append(('Random-Slow','Random-Slow'))
                theList.append(('Choose-Colours-Fast','Choose-Colours-Fast'))
                theList.append(('Choose-Colours-Slow','Choose-Colours-Slow'))
                theList.append(("Default","Default"))
            if int(zwMinor) == 5:  # only for firmware 1.6 versions
                self.logger.debug(unicode(device.model))
                theList.append(("colours","Rainbow-Fast"))  #
                theList.append(("colours","Rainbow-Slow"))
                theList.append(("Default","Default"))

        return theList

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
