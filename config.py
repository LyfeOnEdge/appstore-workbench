import os
import sys
from settings_tool import settings

if __name__ == "__main__":
	sys.exit("This file was not meant to be run, try running appstoreworkbench.py")

WIIU = "WiiU"
SWITCH = "Switch"

CONSOLE = settings.get_setting("console")

if CONSOLE == WIIU:
	REPO_URL = "https://www.wiiubru.com/"
	LIBGET_DIR = "wiiu/apps/appstore/.get/packages"

elif CONSOLE == SWITCH:
	REPO_URL = "https://www.switchbru.com/"
	LIBGET_DIR = "switch/appstore/.get/packages" 

else:
	raise

REPO_JSON_URL = f"{REPO_URL}appstore/repo.json"