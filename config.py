import os
import sys
from settings_tool import settings

if __name__ == "__main__":
	sys.exit("This file was not meant to be run, try running appstoreworkbench.py")

WII = "Wii - alpha - spinnarak (brewtools.dev)"
WII_OSC = "Wii - beta - osc-redist (brewtools.dev)"
WIIU = "WiiU - (wiiubru.com)"
SWITCH = "Switch - (switchbru.com)"

CONSOLE = settings.get_setting("console")

if CONSOLE == WII_OSC:
	REPO_URL = "http://brewtools.dev/osc-redist/" #LyfeOnEdges Temporary Site
	LIBGET_DIR = "wii/apps/appstore/.get/packages"

elif CONSOLE == WII:
	REPO_URL = "http://www.brewtools.dev/wii-spinarak/" #LyfeOnEdges Temporary Site
	LIBGET_DIR = "wii/apps/appstore/.get/packages"

elif CONSOLE == WIIU:
	REPO_URL = "http://wiiubru.com/appstore/"
	LIBGET_DIR = "wiiu/apps/appstore/.get/packages"

elif CONSOLE == SWITCH:
	REPO_URL = "https://www.switchbru.com/appstore/"
	LIBGET_DIR = "switch/appstore/.get/packages" 

if CONSOLE in [WII, WII_OSC, WIIU, SWITCH]:
	REPO_JSON_URL = f"{REPO_URL}repo.json"