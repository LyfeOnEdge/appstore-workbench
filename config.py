import os
import sys
from settings_tool import settings

if __name__ == "__main__":
	sys.exit("This file was not meant to be run, try running appstoreworkbench.py")

WII = "Wii"
WIIU = "WiiU - (wiiubru.com)"
SWITCH = "Switch - (switchbru.com)"

CONSOLE = settings.get_setting("console")

if CONSOLE == WII:
	REPO_URL = "http://brewtools.dev/appstore/" #LyfeOnEdges Temporary Site
	LIBGET_DIR = "wii/apps/appstore/.get/packages"

elif CONSOLE == WIIU:
	REPO_URL = "http://wiiubru.com/appstore/"
	LIBGET_DIR = "wiiu/apps/appstore/.get/packages"

elif CONSOLE == SWITCH:
	REPO_URL = "https://www.switchbru.com/appstore/"
	LIBGET_DIR = "switch/appstore/.get/packages" 

if CONSOLE in [WII, WIIU, SWITCH]:
	REPO_JSON_URL = f"{REPO_URL}repo.json"