import os
import sys
from settings_tool import settings

if __name__ == "__main__":
	sys.exit("This file was not meant to be run, try running appstoreworkbench.py")

WII = "Wii"
WIIU = "WiiU"
SWITCH = "Switch"

CONSOLE = settings.get_setting("console")

if CONSOLE == WII:
	REPO_URL = "http://www.codemii.com/hbb/homebrew_browser/listv035.txt"
	LIBGET_DIR = "wiiu/apps/appstore/.get/packages"

elif CONSOLE == WIIU:
	REPO_URL = "https://www.wiiubru.com/"
	LIBGET_DIR = "wiiu/apps/appstore/.get/packages"

elif CONSOLE == SWITCH:
	REPO_URL = "https://www.switchbru.com/"
	LIBGET_DIR = "switch/appstore/.get/packages" 

if CONSOLE in [WIIU, SWITCH]:
	REPO_JSON_URL = f"{REPO_URL}appstore/repo.json"

elif CONSOLE == WII:
	REPO_JSON_URL = REPO_URL