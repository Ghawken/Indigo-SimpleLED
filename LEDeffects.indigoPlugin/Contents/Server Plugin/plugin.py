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
import struct

#from ghpu import GitHubPluginUpdater

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

    #    self.updater = GitHubPluginUpdater(self)
     #   self.configUpdaterInterval = self.pluginPrefs.get('configUpdaterInterval', 24)
    #    self.configUpdaterForceUpdate = self.pluginPrefs.get('configUpdaterForceUpdate', False)



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


    def shutdown(self):

         self.debugLog(u"shutdown() method called.")

    def startup(self):

        self.debugLog(u"Starting Plugin. startup() method called.  Doing nothing until action Group called.")


    def validatePrefsConfigUi(self, valuesDict):

        self.debugLog(u"validatePrefsConfigUi() method called.")

        error_msg_dict = indigo.Dict()

        # self.errorLog(u"Plugin configuration error: ")

        return True, valuesDict


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

        if command in ['Choose-Colours-Fast','Choose-Colours-Slow','Full-Options']:
            self.logger.debug(u'Setting Colours and ColourParam based on selected colors')
            colourslist = []
            colourslist = pluginAction.props.get('Selectedcolours', 0)
            colourslist = map(int, colourslist)
            coloursparam = sum(colourslist)
            if coloursparam <= 0:
                coloursparam = 2271560481
            # If no colours selected - shouldn't run parameter 38 change
            # but set it to default in case it does
                self.logger.debug(u'Setting Colours Param Variable to default'+unicode(coloursparam))
            self.logger.debug(u'Selected Colours Parameter equals:'+unicode(coloursparam))
            self.logger.debug(unicode(colourslist))
        # Now for LED Strip

        if command in ['Full-Options']:  # This is for firmware 1.04 ZW098 Bulbs Only
            self.logger.debug('Setting up Parameter 37')
            Value1a = int(pluginAction.props.get('Parameter37-Value1a', 0))
            Value1b = int(pluginAction.props.get('Parameter37-Value1b', 0))
            Value2 = int(pluginAction.props.get('Parameter37-Value2', 0))
            Value3 = int(pluginAction.props.get('Parameter37-Value3', 0))
            Value4 = int(pluginAction.props.get('Parameter37-Value4', 0))
            self.logger.debug('Full-Options: Value1a'+unicode(Value1a))

            stringvalue1a = bin(Value1a)[2:].zfill(2)
            self.logger.debug('Full-Options:  Value1b:'+unicode(stringvalue1a))
            stringvalue1b = bin(Value1b)[2:].zfill(4)
            self.logger.debug('Full-Options:  Value1b:'+unicode(stringvalue1b))
            stringvalue1 = stringvalue1a+'00'+stringvalue1b
            self.logger.debug('Full-Options:  Value1:' + unicode(stringvalue1))
            HexValue1 ='%0*X' % ((len(stringvalue1) + 3) // 4, int(stringvalue1, 2))
            self.logger.debug('Full-Options: HexValue1:'+unicode(HexValue1))

            stringvalue2 = bin(Value2)[2:].zfill(8)
            self.logger.debug('Full-Options:  Value2:' + unicode(stringvalue2))
            HexValue2 = '%0*X' % ((len(stringvalue2) + 3) // 4, int(stringvalue2, 2))
            self.logger.debug('Full-Options: HexValue2:' + unicode(HexValue2))

            stringvalue3 = bin(Value3)[2:].zfill(8)
            self.logger.debug('Full-Options:  Value2:' + unicode(stringvalue3))
            HexValue3 = '%0*X' % ((len(stringvalue3) + 3) // 4, int(stringvalue3, 2))
            self.logger.debug('Full-Options: HexValue3:' + unicode(HexValue3))

            stringvalue4 = bin(Value4)[2:].zfill(8)
            self.logger.debug('Full-Options:  Value2:' + unicode(stringvalue4))
            HexValue4 = '%0*X' % ((len(stringvalue4) + 3) // 4, int(stringvalue4, 2))
            self.logger.debug('Full-Options: HexValue4:' + unicode(HexValue4))
            Parameter37= HexValue1+HexValue2+HexValue3+HexValue4
            Parameter37 = int(Parameter37,16)
            self.logger.debug('Full-Options: Parameter 37: ' + unicode(Parameter37))

        if command in ['All-Options']:  # This is for firmware 1.05 ZW098 Bulbs and ZW121 Strips

            self.logger.debug('Setting up Parameter 37')
            Value1a = int(pluginAction.props.get('BParameter37-Value1a', 0))
            Value1b = int(pluginAction.props.get('BParameter37-Value1b', 0))
            Value2 = int(pluginAction.props.get('BParameter37-Value2', 0))

            if Value2>99:
                Value2=99

            Value3 = int(pluginAction.props.get('BParameter37-Value3', 0))
            Value4a = int(pluginAction.props.get('BParameter37-Value4a', 0))
            Value4b = int(pluginAction.props.get('BParameter37-Value4b', 0))

            para381 = int(pluginAction.props.get('BParameter38-Value1', 0))
            para382 = int(pluginAction.props.get('BParameter38-Value2', 0))
            para383 = int(pluginAction.props.get('BParameter38-Value3', 0))
            para384 = int(pluginAction.props.get('BParameter38-Value4', 0))

            para39Red = int(pluginAction.props.get('BParameter39-Red', 0))
            para39Green = int(pluginAction.props.get('BParameter39-Green', 0))
            para39Blue = int(pluginAction.props.get('BParameter39-Blue', 0))

            self.logger.debug('Full-Options: Value1a' + unicode(Value1a))
            stringvalue1a = bin(Value1a)[2:].zfill(2)

            self.logger.debug('Full-Options:  Value1a:' + unicode(stringvalue1a))

            stringvalue1b = bin(Value1b)[2:].zfill(3)
            self.logger.debug('Full-Options:  Value1b:' + unicode(stringvalue1b))

            stringvalue1 = stringvalue1a + '000' + stringvalue1b

            self.logger.debug('Full-Options:  Value1:' + unicode(stringvalue1))
            HexValue1 = '%0*X' % ((len(stringvalue1) + 3) // 4, int(stringvalue1, 2))
            self.logger.debug('Full-Options: HexValue1:' + unicode(HexValue1))

            stringvalue2 = bin(Value2)[2:].zfill(8)
            self.logger.debug('Full-Options:  Value2:' + unicode(stringvalue2))

            HexValue2 = '%0*X' % ((len(stringvalue2) + 3) // 4, int(stringvalue2, 2))
            self.logger.debug('Full-Options: HexValue2:' + unicode(HexValue2))

            stringvalue3 = bin(Value3)[2:].zfill(8)
            self.logger.debug('Full-Options:  Value2:' + unicode(stringvalue3))
            HexValue3 = '%0*X' % ((len(stringvalue3) + 3) // 4, int(stringvalue3, 2))
            self.logger.debug('Full-Options: HexValue3:' + unicode(HexValue3))

            stringvalue4a = bin(Value4a)[2:].zfill(3)
            self.logger.debug('Full-Options:  Value4a:' + unicode(stringvalue4a))

            stringvalue4b = bin(Value4b)[2:].zfill(5)
            self.logger.debug('Full-Options:  Value4b:' + unicode(stringvalue4b))
            stringvalue4 = stringvalue4a +  stringvalue4b
            self.logger.debug('Full-Options:  Value4:' + unicode(stringvalue4))

            HexValue4 = '%0*X' % ((len(stringvalue4) + 3) // 4, int(stringvalue4, 2))
            self.logger.debug('Full-Options: HexValue4:' + unicode(HexValue4))
            Parameter37 = HexValue1 + HexValue2 + HexValue3 + HexValue4
            Parameter37 = int(Parameter37, 16)
            self.logger.debug('Full-Options: Parameter 37: ' + unicode(Parameter37))

            self.logger.debug('Full-Options: Parameter 38-1:' + unicode(para381))
            stringpara381 = hex(para381)[2:].zfill(2)
            self.logger.debug('Full-Options:  Parameter 38-1:' + unicode(stringpara381))

            self.logger.debug('Full-Options: Parameter 38-2:' + unicode(para382))
            stringpara382 = hex(para382)[2:].zfill(2)
            self.logger.debug('Full-Options:  Parameter 38-1:' + unicode(stringpara382))

            self.logger.debug('Full-Options: Parameter 38-3:' + unicode(para383))
            stringpara383 = hex(para383)[2:].zfill(2)
            self.logger.debug('Full-Options:  Parameter 38-3:' + unicode(stringpara383))

            self.logger.debug('Full-Options: Parameter 38-4:' + unicode(para384))
            stringpara384 = hex(para384)[2:].zfill(2)
            self.logger.debug('Full-Options:  Parameter 38-4:' + unicode(stringpara384))

            Parameter38 = int(stringpara381+stringpara382+stringpara383+stringpara384,16)
            self.logger.debug('Full-Options:  Parameter 38:' + unicode(Parameter38))

            if Value1b==4:  ## Single Colour Mode
                self.logger.debug('Full-Options: Parameter 39-Red:' + unicode(para39Red))
                stringpara39Red = hex(para39Red)[2:].zfill(2)
                self.logger.debug('Full-Options:  Parameter 38-Red:' + unicode(stringpara39Red))

                self.logger.debug('Full-Options: Parameter 39-Green:' + unicode(para39Green))
                stringpara39Green = hex(para39Green)[2:].zfill(2)
                self.logger.debug('Full-Options:  Parameter 38-Green:' + unicode(stringpara39Green))

                self.logger.debug('Full-Options: Parameter 39-Blue:' + unicode(para39Blue))
                stringpara39Blue = hex(para39Blue)[2:].zfill(2)
                self.logger.debug('Full-Options:  Parameter 39-Blue:' + unicode(stringpara39Blue))

                Parameter39 = stringpara39Red + stringpara39Green + stringpara39Blue + '00'
                Parameter39 = int(Parameter39, 16)
                self.logger.debug('Full-Options:  Parameter 39 Hex:' + unicode(Parameter39))
            elif Value1b==2:
                self.logger.debug(u'Full Options : Setting Colours and ColourParam based on selected colors')
                colourslist = []
                colourslist = pluginAction.props.get('Stripcolours', 0)
                colourslist = map(int, colourslist)
                colourstring = ''
                # coloursparam = sum(colourslist)
                # No not sum here - construct hex and pad out to 8 digits then convert
                for item in colourslist:
                    colourstring = str(colourstring) + str(item)
                colourstring = colourstring.ljust(8, '0');
                self.logger.debug('ColourString Equals:' + unicode(colourstring))
                Parameter39 = int(colourstring, 16)
                if Parameter39 <= 0:
                    Parameter39 = 805306368
                    # If no colours selected - shouldn't run parameter 38 change
                    # but set it to default in case it does
                    self.logger.debug(u'Setting Colours Param Variable to default' + unicode(Parameter39))
                self.logger.debug(u'Selected Colours Parameter 39 equals:' + unicode(Parameter39))
                self.logger.debug(unicode(colourslist))
            elif Value1b==3: ## Randon Mode set Random Seed
                self.logger.debug(u'Full Options : Setting Random Seed: Using Red/Green/blue')
                self.logger.debug('Full-Options: Parameter 39-Random1:' + unicode(para39Red))
                stringpara39Red = hex(para39Red)[2:].zfill(2)
                self.logger.debug('Full-Options:  Parameter 38-Random1:' + unicode(stringpara39Red))

                self.logger.debug('Full-Options: Parameter 39-Random2:' + unicode(para39Green))
                stringpara39Green = hex(para39Green)[2:].zfill(2)
                self.logger.debug('Full-Options:  Parameter 38-Random2:' + unicode(stringpara39Green))

                self.logger.debug('Full-Options: Parameter 39-Random3:' + unicode(para39Blue))
                stringpara39Blue = hex(para39Blue)[2:].zfill(2)
                self.logger.debug('Full-Options:  Parameter 39-Random3:' + unicode(stringpara39Blue))

                Parameter39 = stringpara39Red + stringpara39Green + stringpara39Blue + '00'
                Parameter39 = int(Parameter39, 16)
                self.logger.debug('Full-Options:  Parameter 39 Hex:' + unicode(Parameter39))
            else:
                Parameter39 = 805306368
                # If no colours selected - shouldn't run parameter 38 change
                # but set it to default in case it does
                self.logger.debug(u'Setting Colours Param Variable to default' + unicode(Parameter39))

        if command in ["Choose-Colour-Options" ,'Choose-Colours-Smooth' ,'Choose-Colours-Fade']:

            # Hexadecimal colour chooser
            # 12300000 = Red/Orange/Yellow
            # 14700000 = Red/Green/Colour Number 7
            self.logger.debug(u'Choose Colours Options : Setting Colours and ColourParam based on selected colors')
            colourslist = []
            colourslist = pluginAction.props.get('Stripcolours', 0)
            colourslist = map(int, colourslist)

            colourstring =''
            #coloursparam = sum(colourslist)
            # No not sum here - construct hex and pad out to 8 digits then convert
            for item in colourslist:
                colourstring = str(colourstring) + str(item)
            colourstring = colourstring.ljust(8,'0');
            self.logger.debug('ColourString Equals:'+unicode(colourstring))

            coloursparam = int(colourstring,16)

            if coloursparam <= 0:
                coloursparam = 805306368
                # If no colours selected - shouldn't run parameter 38 change
                # but set it to default in case it does
                self.logger.debug(u'Setting Colours Param Variable to default' + unicode(coloursparam))
            self.logger.debug(u'Selected Colours Parameter equals:' + unicode(coloursparam))
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

        if dev.model == 'RGBW Controller (FGRGBWM)' or dev.model=="RGBW Controller (FGRGBWM441)":  #Double check!
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
        elif dev.model == "RGBW Controller (FGRGBW442)":   # Double check!
            if command == "Rainbow":
                self.logger.debug(u'Rainbow Set on device:' + unicode(dev.name))
                indigo.zwave.sendConfigParm(device=indigo.devices[devId], paramIndex=157, paramSize=1, paramValue=8)
            if command == "Fireplace":
                self.logger.debug(u'FirePlace Set on device:' + unicode(dev.name))
                indigo.zwave.sendConfigParm(device=indigo.devices[devId], paramIndex=157, paramSize=1, paramValue=6)
            if command == "Storm":
                self.logger.debug(u'Storm Set on device:' + unicode(dev.name))
                indigo.zwave.sendConfigParm(device=indigo.devices[devId], paramIndex=157, paramSize=1, paramValue=7)
            if command == "Aurora":
                self.logger.debug(u'Aurora Set on device:' + unicode(dev.name))
                indigo.zwave.sendConfigParm(device=indigo.devices[devId], paramIndex=157, paramSize=1, paramValue=9)
            if command == "LPD":
                self.logger.debug(u'LPD Set on device:' + unicode(dev.name))
                indigo.zwave.sendConfigParm(device=indigo.devices[devId], paramIndex=157, paramSize=1, paramValue=10)
            if command == "Default":
                self.logger.debug(u'Default Set on device:' + unicode(dev.name))
                indigo.zwave.sendConfigParm(device=indigo.devices[devId], paramIndex=157, paramSize=1, paramValue=0)

        elif dev.model == "RGBW Controller (FGRGBWM442)":   # Double check!
            if command == "Rainbow":
                self.logger.debug(u'Rainbow Set on device:' + unicode(dev.name))
                indigo.zwave.sendConfigParm(device=indigo.devices[devId], paramIndex=157, paramSize=1, paramValue=8)
            if command == "Fireplace":
                self.logger.debug(u'FirePlace Set on device:' + unicode(dev.name))
                indigo.zwave.sendConfigParm(device=indigo.devices[devId], paramIndex=157, paramSize=1, paramValue=6)
            if command == "Storm":
                self.logger.debug(u'Storm Set on device:' + unicode(dev.name))
                indigo.zwave.sendConfigParm(device=indigo.devices[devId], paramIndex=157, paramSize=1, paramValue=7)
            if command == "Aurora":
                self.logger.debug(u'Aurora Set on device:' + unicode(dev.name))
                indigo.zwave.sendConfigParm(device=indigo.devices[devId], paramIndex=157, paramSize=1, paramValue=9)
            if command == "LPD":
                self.logger.debug(u'LPD Set on device:' + unicode(dev.name))
                indigo.zwave.sendConfigParm(device=indigo.devices[devId], paramIndex=157, paramSize=1, paramValue=10)
            if command == "Default":
                self.logger.debug(u'Default Set on device:' + unicode(dev.name))
                indigo.zwave.sendConfigParm(device=indigo.devices[devId], paramIndex=157, paramSize=1, paramValue=0)

        elif dev.model == 'RGBW LED Strip (ZW121)':
            if command=="Rainbow":
                self.logger.debug(u'Rainbow Set on device:'+unicode(dev.name))
                indigo.zwave.sendConfigParm(device=indigo.devices[devId],paramIndex=40,paramSize=1,paramValue=1)
            if command == "All-Options":
                self.logger.debug(u'Setting all Options Set on device:'+unicode(dev.name))
                indigo.zwave.sendConfigParm(device=indigo.devices[devId],paramIndex=37,paramSize=4,paramValue=Parameter37)
                indigo.zwave.sendConfigParm(device=indigo.devices[devId], paramIndex=38, paramSize=4, paramValue=Parameter38)
                indigo.zwave.sendConfigParm(device=indigo.devices[devId], paramIndex=39, paramSize=4,paramValue=Parameter39)
            if command == "Choose-Colour-Options":
                self.logger.debug(u'Choose Colours Set on device:' + unicode(dev.name))
                #coloursparam = struct.unpack('<H', struct.pack('>H',coloursparam))[0]
                self.logger.debug(u'ColoursParam is now:'+unicode(coloursparam))
                indigo.zwave.sendConfigParm(device=indigo.devices[devId], paramIndex=37, paramSize=4,paramValue=1241514063)
                self.sleep(1)
                # send the selected colours - so mode above and colour choice below.
                indigo.zwave.sendConfigParm(device=indigo.devices[devId], paramIndex=39, paramSize=4,paramValue=coloursparam)
                #indigo.zwave.sendConfigParm(device=indigo.devices[devId], paramIndex=40, paramSize=1,paramValue=2)
            if command == "Rainbow-2":
                self.logger.debug(u'"Rainbow-2 & Turn On" Set on device:' + unicode(dev.name))
                #coloursparam = struct.unpack('<H', struct.pack('>H',coloursparam))[0]
                self.logger.debug(u'ColoursParam is :'+unicode(coloursparam))
                indigo.zwave.sendConfigParm(device=indigo.devices[devId], paramIndex=37, paramSize=4,paramValue=150994944 )
                self.sleep(1)
            if command == "Rainbow-Slow Fade":
                self.logger.debug(u'Rainbow-Slow Fade Set on device:' + unicode(dev.name))
                #coloursparam = struct.unpack('<H', struct.pack('>H',coloursparam))[0]
                self.logger.debug(u'ColoursParam is now:'+unicode(coloursparam))
                indigo.zwave.sendConfigParm(device=indigo.devices[devId], paramIndex=37, paramSize=4,paramValue=1224736847 )
                self.sleep(1)
            if command == "Rainbow-Medium Fade":
                self.logger.debug(u'Rainbow-Medium Fade Set on device:' + unicode(dev.name))
                #coloursparam = struct.unpack('<H', struct.pack('>H',coloursparam))[0]
                self.logger.debug(u'ColoursParam is now:'+unicode(coloursparam))
                indigo.zwave.sendConfigParm(device=indigo.devices[devId], paramIndex=37, paramSize=4,paramValue=1224736815)
                self.sleep(1)
            if command=="Default":
                self.logger.debug(u'Default Set on device:'+unicode(dev.name))
                indigo.zwave.sendConfigParm(device=indigo.devices[devId],paramIndex=40,paramSize=1,paramValue=0)
                indigo.zwave.sendConfigParm(device=indigo.devices[devId], paramIndex=37, paramSize=4, paramValue=157483008)
                #indigo.zwave.sendConfigParm(device=indigo.devices[devId], paramIndex=38, paramSize=4, paramValue=50332416)
                indigo.zwave.sendConfigParm(device=indigo.devices[devId], paramIndex=39, paramSize=4,paramValue=805306368)
                indigo.device.turnOff(device=indigo.devices[devId])
            # add firmware check for Aeon Bulbs
        elif dev.model == 'RGBW LED Bulb (ZW098)':
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
                if command == "Full-Options":
                    self.logger.debug(u'Setting all Options Set on device:'+unicode(dev.name))
                    indigo.zwave.sendConfigParm(device=indigo.devices[devId],paramIndex=37,paramSize=4,paramValue=Parameter37)
                    indigo.zwave.sendConfigParm(device=indigo.devices[devId], paramIndex=38, paramSize=4,paramValue=coloursparam)
            elif int(zwMinor)>=5:   # select firmware 1.5 ?
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
                if command == "Choose-Colours-Smooth":
                    self.logger.debug(u'Random-fast Set on device:' + unicode(dev.name))
                    indigo.zwave.sendConfigParm(device=indigo.devices[devId], paramIndex=37, paramSize=4, paramValue=40042528 )
                    #send the selected colours - so mode above and colour choice below.
                    indigo.zwave.sendConfigParm(device=indigo.devices[devId], paramIndex=38, paramSize=4,paramValue=50593791)
                    indigo.zwave.sendConfigParm(device=indigo.devices[devId], paramIndex=39, paramSize=4,paramValue=coloursparam)
                if command == "Choose-Colours-Fade":
                    self.logger.debug(u'Random-fast Set on device:' + unicode(dev.name))
                    indigo.zwave.sendConfigParm(device=indigo.devices[devId], paramIndex=37, paramSize=4, paramValue= 42630020 )
                    # send the selected colours - so mode above and colour choice below.
                    indigo.zwave.sendConfigParm(device=indigo.devices[devId], paramIndex=38, paramSize=4, paramValue=50593791)
                    indigo.zwave.sendConfigParm(device=indigo.devices[devId], paramIndex=39, paramSize=4,  paramValue=coloursparam)
                if command == "All-Options":
                    self.logger.debug(u'Setting all Options Set on device:'+unicode(dev.name))
                    indigo.zwave.sendConfigParm(device=indigo.devices[devId],paramIndex=37,paramSize=4,paramValue=Parameter37)
                    indigo.zwave.sendConfigParm(device=indigo.devices[devId], paramIndex=38, paramSize=4, paramValue=Parameter38)
                    indigo.zwave.sendConfigParm(device=indigo.devices[devId], paramIndex=39, paramSize=4,paramValue=Parameter39)

        return

    def uiEffects(self, filter, valuesDict, typeId, deviceId):

        theList = []
        device = indigo.devices[deviceId]
        #self.logger.debug(u'Device Details'+unicode(device))
        #self.logger.debug(unicode(device.model))
        zwMajor = int(device.ownerProps['zwAppVersMajor'])
        zwMinor = int(device.ownerProps['zwAppVersMinor'])
## testing below TODO remove when done!
        #theList.append(('All-Options', 'All-Options'))

        self.logger.debug(u'Device Model is:'+unicode(device.model))
        self.logger.debug(u'Firmware equals:'+unicode(zwMajor) + "."+unicode(zwMinor))

        if 'RGBW Controller (FGRGBWM)' in device.model:  ## old version reported by Indigo of 441 Fibaro RGB
            self.logger.debug(unicode(device.model))
            theList.append(("Rainbow","Rainbow"))
            theList.append(("Fireplace","Fireplace"))
            theList.append(("Storm","Storm"))
            theList.append(("Aurora","Aurora"))
            theList.append(("LPD","LPD"))
            theList.append(("Default","Default"))
        elif 'RGBW Controller (FGRGBWM441)' in device.model:  ## new version reported by Indigo of 441 Fibaro RGB
            self.logger.debug(unicode(device.model))
            theList.append(("Rainbow","Rainbow"))
            theList.append(("Fireplace","Fireplace"))
            theList.append(("Storm","Storm"))
            theList.append(("Aurora","Aurora"))
            theList.append(("LPD","LPD"))
            theList.append(("Default","Default"))
        elif 'RGBW Controller (FGRGBW442)' in device.model:  ## new 442 version reported by Indigo of 442 Fibaro RGB
            self.logger.debug(unicode(device.model))
            theList.append(("Rainbow","Rainbow"))
            theList.append(("Fireplace","Fireplace"))
            theList.append(("Storm","Storm"))
            theList.append(("Aurora","Aurora"))
            theList.append(("LPD","LPD"))
            theList.append(("Default","Default"))
        elif 'RGBW Controller (FGRGBWM442)' in device.model:  ## new 442 version reported by Indigo of 442 Fibaro RGB
            self.logger.debug(unicode(device.model))
            theList.append(("Rainbow","Rainbow"))
            theList.append(("Fireplace","Fireplace"))
            theList.append(("Storm","Storm"))
            theList.append(("Aurora","Aurora"))
            theList.append(("LPD","LPD"))
            theList.append(("Default","Default"))
        elif device.model == 'RGBW LED Strip (ZW121)':
            self.logger.debug(unicode(device.model))
            theList.append(("Rainbow","Rainbow & Turn On"))
            theList.append(("Rainbow-2", "Rainbow-2 & Turn On"))
            theList.append(("Rainbow-Slow Fade", "Rainbow-Slow Fade & Turn On"))
            theList.append(("Rainbow-Medium Fade", "Rainbow-Medium Fade & Turn On"))
            theList.append(('Choose-Colour-Options', 'Choose-Colour-Options'))
            theList.append(('All-Options','All-Options'))
            theList.append(("Default","Default & Turn Off"))
        elif device.model == 'RGBW LED Bulb (ZW098)':
            if int(zwMinor) == 4:  # only for firmware 1.4 versions
                self.logger.debug(unicode(device.model))
                theList.append(("Rainbow-Fast","Rainbow-Fast"))
                theList.append(("Rainbow-Slow","Rainbow-Slow"))
                theList.append(('Random-Fast','Random-Fast'))
                theList.append(('Random-Slow','Random-Slow'))
                theList.append(('Choose-Colours-Fast','Choose-Colours-Fast'))
                theList.append(('Choose-Colours-Slow','Choose-Colours-Slow'))
                theList.append(('Full-Options','Full-Options'))
                theList.append(("Default","Default"))
            if int(zwMinor) >= 5:  # only for firmware 1.6 versions
                self.logger.debug(unicode(device.model))
                theList.append(("Rainbow-Fast","Rainbow-Fast"))  #
                theList.append(("Rainbow-Slow","Rainbow-Slow"))
                theList.append(('Choose-Colours-Smooth','Choose-Colours-Smooth'))
                theList.append(('Choose-Colours-Smooth', 'Choose-Colours-Smooth'))
                theList.append(('All-Options','All-Options'))
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
