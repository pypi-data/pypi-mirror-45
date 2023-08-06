#!/usr/bin/env python
import plistlib
import public

PLIST = "/Library/Preferences/Audio/com.apple.audio.SystemSettings.plist"

"""
OSX High Sierra+:
device.AppleHDAEngineOutput:1B,0,1,2:0 = Dict {
seed = 0 (default), seed = 25 (headphones)
old MacOS:
cat "$plist" | grep "time" | grep -v "time = 0"
"""

@public.add
def isplugged():
    """return True if headphones are plugged, else False"""
    plist = plistlib.readPlist(PLIST)
    for key, value in plist.items():
        if "AppleHDAEngineOutput" in key:
            seed = plist[key]["global.arrival"]["seed"]
            return seed > 0
