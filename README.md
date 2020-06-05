Hi all,

Announcing a very simple new Plugin - 
**LED Simple Effects**

**For Indigo 7**

Supported Devices:
- Fibaro RGBW Controller, 441 Model and 442 Model
- AeonLabs ZW098 bulbs Firmware 1.04, 1.05 and above
- AeonLabs ZW121 Led Strips

Basics of this plugin are to support the various modes, colour cycling of these devices without the need for repeated Z-wave traffic.
This can be done with a modified parameter z-wave command for each device, without this plugin.

The aim of this Plugin is to simplify that process, and enable complicated settings which previous would have needed AeonLabs excel spreadhsheet to calculate

The Plugin - essentially doesn't run unless a action command/group is executed.

The image below are the current options - essentially for the Fibaro RGB only currently (awaiting some fixes to enable the Aeon Labs RGB bulbs in addition.)

![](https://raw.githubusercontent.com/Ghawken/Indigo-SimpleLED/master/Images/Led_Effects.png)

![](https://raw.githubusercontent.com/Ghawken/Indigo-SimpleLED/master/Images/Led_Effects%20(1).png)


These are the pre-programmed Fibaro modes - so there is no Z-wave communication during the light changes - simply this command to start and/or end the process.   
In my mind the various default modes cover most basic usages and limits any Z-wave traffic issues that might occur with other solutions.



As promised support for Aeon Labs RGB Bulbs (ZW098) Firmware 1.04/1.05 and 1.06 above

Similar Modes but also add dialog for colour chooser/selected see below

![](https://raw.githubusercontent.com/Ghawken/Indigo-SimpleLED/master/Images/Rainbow-_Fast.png)

![](https://raw.githubusercontent.com/Ghawken/Indigo-SimpleLED/master/Images/Choose-_Colours-_Fast.png)

You can select all colours or some, with use of the command key to multi-select.



& Finally the complete Full-Options, available for AeonLabs ZW098 and ZW121


![](https://raw.githubusercontent.com/Ghawken/Indigo-SimpleLED/master/Images/AlarmLEDStrip.png)


For example this example rapidly flashes with fading from Red/Blue - Siren type effect


The first section calculates - Parameter 37, 2nd Red/Green/Blue is Parameter 38, and Colour Selector is Parameter 39



Glenn
