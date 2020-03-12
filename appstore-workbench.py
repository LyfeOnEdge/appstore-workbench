#!/usr/bin/python3
# -*- coding: utf-8 -*-
version = "3.2"

import os
import sys
import platform
import json
import threading
from timeit import default_timer as timer
# print version, exit if minimum version requirements aren't met
if sys.hexversion < 0x03060000:  # Trying to import tkinter in the new syntax after python 2 causes a crash
    sys.exit("Python 3.6 or greater is required to run this program.")
print("Using Python {}.{}".format(sys.version_info[0], sys.version_info[1]))
version_string = f"Appstore Workbench {version}"
# This is called before the below module imports to ensure no exception is
# encountered trying to import tk
try:
    import tkinter as tk
    print("Using tkinter version {}".format(tk.Tcl().eval('info patchlevel')))
except:
    sys.exit("Cannot start: Tkinter not installed, consult the readme for more information.")

try:
    TKVERSION = float(tk.Tcl().eval('info patchlevel')[0:3])
except Exception as e:
    TKVERSION = 0
    print("Failed to get tkinter version ~ {}".format(e))
print(TKVERSION)

# This is called before the below module imports to ensure no exception is
# encountered trying to import pil
try:
    import PIL  # Import pillow library
except:
    sys.exit("Cannot start: Pillow module not installed, try `pip install Pillow` or consult the readme for more information.")

folders_to_init = ["cache", "cache/json", "cache/images", "downloads", "tools", "plugins"]
for folder in folders_to_init:
    if not os.path.isdir(folder):
        print(f"Initializing folder {folder}")
        os.mkdir(folder)

#To be written if there is no config file
config_default = """
#If you have other plugins dirs add them here
plugins_path_list = [
    "./plugins",
]

#True / False
keep_topmost = False

#"fullscreen" / "maximized" / None (windowed)
maximized = False

#True / False
borderless = False
"""
if not os.path.isfile(os.path.join(os.path.dirname(__file__), "config.py")):
    with open(os.path.join(os.path.dirname(__file__), "config.py"), "w+") as configfile:
        configfile.write(config_default)
import config

# Import local modules
from gui.gui import window

# from github_updater import updater

def startGUI(args=None):
    # frameManager serves to load all pages and stack them on top of each other (all 2 of them)
    # also serves to make many important objects and functions easily
    # available to children frames
    app = window(args, geometry = "900x400", version = version)

    # Set title formatted with version
    app.set_version(version_string)
    app.title(version_string)

    app.attributes("-topmost", config.keep_topmost)

    maximized_options = {
        "fullscreen": "-fullscreen",
        "maximized": "-zoomed",
        "windowed": None
    }
    if config.maximized:
        opt = maximized_options[config.maximized]

        if platform.system() == 'Windows':
            try:
                app.statepages(opt.strip("-"))
            except Exception as e:
                print("Error setting window launch type for Windows, this is a bug please report it:\n     {}".format(e))
        else:
            app.attributes(opt, True)

    # Set icon
    favicon = None
    if platform.system() in ['Windows', 'Linux']:
        print("{} detected, setting icon".format(platform.system()))
        favicon = 'gui/assets/favicon.png'
    elif platform.system() == "Darwin":
        print("MacOS detected, not setting icon as it is not supported")

    if favicon:
        if os.path.exists(favicon):
            # Set icon
            app.tk.call('wm', 'iconphoto', app._w, tk.PhotoImage(file=favicon))
        else:
            print("Icon file not found, not setting favicon")

    if config.borderless:
        if platform.system() in ['Windows']:
            app.overrideredirect(1)
        else:
            try:
                if TKVERSION > 8.5:
                    if app.tk.call('tk', 'windowingsystem') == "x11":
                        app.wm_attributes('-type', 'splash')
                else:
                    print("Tkinter version too low to set window to borderless.")
            except:
                print("Failed to set window type to borderless")

    app.mainloop()

if __name__ == '__main__':
    startGUI()