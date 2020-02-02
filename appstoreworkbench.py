#!/usr/bin/python3
# -*- coding: utf-8 -*-
version = "2.0"
version_string = f"Appstore Workbench {version}"

import os
import sys
import platform
import json
import threading
import argparse
from timeit import default_timer as timer
# print version, exit if minimum version requirements aren't met
print("Using Python {}.{}".format(sys.version_info[0], sys.version_info[1]))
if sys.hexversion < 0x03060000:  # Trying to import tkinter in the new syntax after python 2 causes a crash
    sys.exit("Python 3.6 or greater is required to run this program.")

# This is called before the below module imports to ensure no exception is
# encountered trying to import tk
try:
    import tkinter as tk
    print("Using tkinter version {}".format(tk.Tcl().eval('info patchlevel')))
except:
    # Input is called to prevent the cli from closing until the user has seen
    # the message
    input("Cannot start: Tkinter not installed, consult the readme for more information. Press enter to exit program.")
    sys.exit()

try:
    TKVERSION = float(tk.Tcl().eval('info patchlevel')[0:3])
except Exception as e:
    TKVERSION = 0
    print("Failed to get tkinter version ~ {}".format(e))
print(TKVERSION)

# This is called before the below module imports to ensure no exception is
# encountered trying to import pil after stuff has loaded
try:
    import PIL  # Import pillow library
except:
    input("Cannot start: Pillow module not installed, try `pip install Pillow` or consult the readme for more information. Press enter to exit program.")
    sys.exit()

# Import local modules
from widgets import frameManager
from appstore import Parser, appstore_handler, getPackageIcon
from webhandler import getJson, getCachedJson
from locations import update_url
from github_updater import updater
from settings_tool import settings
from pages import pagelist

print("Checking for updates...")
if updater.check_for_update(version):
    print("Update detected.")
else:
    print("Up to date.")

def create_arg_parser():
    parser = argparse.ArgumentParser(
        description='pass a repo.json to load a local one instead of one downloaded from github')
    parser.add_argument('repo',
                        help='repo.json path')
    return parser

def startGUI(args=None):
    # frameManager serves to load all pages and stack them on top of each other (all 2 of them)
    # also serves to make many important objects and functions easily
    # available to children frames
    gui = frameManager(
    	pagelist, 
    	args, 
    	{
	    	"width": settings.get_setting("width"),
	    	"height": settings.get_setting("height")
    	}
    )

    # Set title formatted with version
    gui.set_version(version_string)
    gui.title(version_string)
    # Wheteher to keep window topmost
    gui.attributes(
        "-topmost", True if settings.get_setting("keep_topmost") == "true" else False)

    maximized_options = {
        "fullscreen": "-fullscreen",
        "maximized": "-zoomed",
        "windowed": None
    }
    if maximized_options[settings.get_setting("maximized")]:
        opt = maximized_options[settings.get_setting("maximized")]

        if platform.system() == 'Windows':
            try:
                gui.state(opt.strip("-"))
            except Exception as e:
                print(
                    "Error setting window launch type for Windows, this is a bug please report it:\n     {}".format(e))
        else:
            gui.attributes(opt, True)

    # Set icon
    favicon = None
    if platform.system() in ['Windows', 'Linux']:
        print("{} detected, setting icon".format(platform.system()))
        favicon = 'assets/favicon.png'
    elif platform.system() == "Darwin":
        print("MacOS detected, not setting icon as it is not supported")

    if favicon:
        if os.path.exists(favicon):
            # Set icon
            gui.tk.call('wm', 'iconphoto', gui._w, tk.PhotoImage(file=favicon))
        else:
            print("Icon file not found, not setting favicon")

    if (True if settings.get_setting("borderless") == "true" else False):
        if platform.system() in ['Windows']:
            gui.overrideredirect(1)
        else:
            try:
                if TKVERSION > 8.5:
                    if gui.tk.call('tk', 'windowingsystem') == "x11":
                        gui.wm_attributes('-type', 'splash')
            except:
                print("Failed to set window type to borderless")

    gui.mainloop()

parsed_args = None
if len(sys.argv) > 1:
    arg_parser = create_arg_parser()
    parsed_args = arg_parser.parse_args(sys.argv[1:])

if not parsed_args:
    # Launch normally, get updated repo file
    print("Getting updated homebrew repository file")
    packages_json = getJson(
        "repos", "https://www.switchbru.com/appstore/repo.json")
    if not packages_json:
        print("Failed to download packages json repo file, falling back on cached version")
        raise
else:
    # Launching with `python3 script.py test` will allow
    # you to test gui changes without hitting the repo
    # uses cached json
    if parsed_args.repo.lower() == "test":
        print("Using local json")
        packages_json = getCachedJson("repos")
    else:
        print("Using passed repo json {}".format(parsed_args.repo))
        packages_json = parsed_args.repo

# Parse the json into categories
Parser.load_file(packages_json)

if __name__ == '__main__':
    startGUI(parsed_args)
