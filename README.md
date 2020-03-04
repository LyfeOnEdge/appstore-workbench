# Appstore Workbench
[![Appstore-workbench](https://cdn.discordapp.com/attachments/616331814021103674/684187810353512488/unknown.png)]()

[![License](https://img.shields.io/badge/License-GPLv3-blue.svg)]() [![Releases](https://img.shields.io/github/downloads/LyfeOnEdge/appstore-workbench/total.svg)]() [![LatestVer](https://img.shields.io/github/release-pre/LyfeOnEdge/appstore-workbench.svg)]() 

![[Brew Tools](https://discord.gg/de7tdqe)](https://github.com/LyfeOnEdge/appstore-workbench/blob/master/docu/SwitchToolsDiscordBanner.png?raw=true)
### What is it?
Appstore Workbench began as an attempt to provide a desktop alternative to 4TU's Homebrew Appstore, but moved to using a plugin system to provide more tools than just homebrew management, serving as a basis to many projects that would otherwise not warrant a gui. Appstore Workbench is welcome to community plugin submissions for any console. Appstore Workbench is a Mac/Windows/Linux compatible python app.

#### Features:
- Homebrew plugins for Wii, WiiU, and Nintendo Switch. Over 500 packages
  - Homebrew management tool that doesn't require target platforms to have access to the internet
  - Dynamic Search
  - Categories
  - Compatible with the Homebrew Appstore package manager
  - Easily open project pages in browser
  - Threaded operations mean the app stays responsive with big downloads
- Plugin Support
- Scalable Window

#### Notable plugins:
- Nintendo Switch, WiiU, and Wii homebrew
- Switch Serial Number Checker
- Switch Payload Injector
- WiiU Web Exploit Hoster

#### Requirements:
    Works on: macOS, Windows, Linux
    Python 3.6 or greater
    Dependencies vary by OS, see below.

##### Windows:
- Extract appstore-workbench.zip
- Install [python](https://www.python.org/downloads/release/python-373/)
  - You *must* restart your pc after installing python for the first time.
  - If you do a custom installation remember to install tcl/tk, add python to the path, and include pip
- In a command prompt navigate to the dir you extracted the app to and type ```pip install -r requirements``` to install dependencies
- Type `python appstore-workbench`

##### Macintosh:
- Extract appstore-workbench.zip
- Mac users may already have a compatible version of python installed, try double-clicking appstoreworkbench.py
- In a command prompt navigate to the dir you extracted the app to and type ```pip3 install -r requirements``` to install dependencies
  - If the file opens in a text reader, close the reader and right-click the file and open it with pylauncher
- If this still doesn't work, install [python](https://www.python.org/downloads/release/python-373/)
- To run the app: double-click `appstore-workbench.py`

##### Linux:
- Extract appstore-workbench.zip
- Navigate to the directory in a terminal
- Type ```pip3 install -r requirements``` to install dependencies
- Type `python appstoreworkbench.py`
  - If you are missing dependencies do the following:
  - `sudo apt install python3 python3-pip python3-tk python3-pil.imagetk`
- If you don't know how to do this you should probably be using Windows.
- Finally type `python3 appstore-workbench.py`

## Troubleshooting:
##### Mac:
- Error:
  - ```ssl.SSLCertVerificationError: [SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: unable to get local issuer certificate (_ssl.c:1056)```
  - Solution: Macintosh HD > Applications > Python3.6 folder (or whatever version of python you're using) > double click on "Install Certificates.command" file

## Plugin System

###  Plugins
Plugins form the basis of appstore-workbench. On it's own appstore-workbench serves only to download plugins. This allows appstore-workbench to serve a variety of consoles without becoming bloated - being able to be tailored to the user's needs.
Plugins can either run in the background, add pages, or both. Pages are derived from tkinter tk.Frame objects so you can use them to build anything you could build in a normal tkinter Frame.

Plugins can also added manually by placing them in the `plugins` folder of appstore-workbench.
Single-file plugins can be named `anything.py`, plugins with assets must be in folders, and must be called plugin.py
The plugin system is non-recursive, meaning a plugin in `./plugins/plugin_folder/plugin_subfolder/plugin.py` would not be seen.

##### Example plugin folder layout:
```
_appstore-workbench
 |_plugins
   |_pluginA.py
   |_pluginB.py
   |_pluginC
   | |_plugin.py
   |_pluginD
     |_plugin.py
```

##### Example Usage:
```py
from gui.widgets import basePlugin
import os

class Plugin(basePlugin.BasePlugin):
  def __init__(self, app, container):
    super().__init__(self, app, "PLUGIN_NAME", container)
    self.app = app #gui object
    self.container = container #Parent frame for pages, classed from tk.Frame()
    #Declare any values you want available throughout your pages here

  def get_pages(self):
    #If your plugin does more than run in the background,
    #this function will need to return a list of pages
    #derived from 
    #See README section on 
    return []

  def exit(self):
    #If your widgets needs to do things to exit gracefully
    #you need to do them here.
    pass

#Setup function called on each plugin, must return object
#derived from basePlugin.BasePlugin
def setup(app, container):
  #Do stuff you need done before the plugin loads here
  return Plugin(app, container)
```
## Pages
##### Example Usage:
```py
from gui.widgets import basePage
import tkinter as tk #Basepage is derived from tk.Frame so tk widgets work
import style #style.py is used to keep app colors and sizes consistent

class Page(basePage.BasePage):
    def __init__(self, app, container, plugin):
        super().__init__(self, app, container, "NAME")
        
    about_label = tk.Label(self, 
        text = "Hello!", 
        background = style.primary_color, 
        foreground = style.primary_text_color, 
        font = style.smalltext
      ).place(
        relx = 0.5,
        x = - 50,
        width = 100,
        rely = 0.5,
        y = - 20
        height = - 50 
      )
```
## Threading
Also included in this project is a worker thread tool I made
that works with tkinter (calling threads from within the gui 
normally doesn't work). Threads must be procedural (they can't
return something), but they are incredibly useful for updating
elements of the gui without blocking everything else.
##### Example Usage:
```py
from gui.widgets import basePage
from asyncthreader import threader #Import thread

class Page(basePage.BasePage):
    def __init__(self, app, container, plugin):
        super().__init__(self, app, container, "NAME")

  #Let's say this gets called when a button on the page is pushed
  def on_button_push(self):
    #Calling something blocking here would freeze everything
    #Instead call it as a thread
    threader.do_async(self.load_big_file_async)
    
  def load_big_file_async(self):
    #When called above by the threader anything here will run without blocking
    pass
```
Additionally threads can be called with args:
```py
from asyncthreader import threader

def callback(arg1, arg2, ...):
  pass

threader.do_async(callback, [arg1, ar2, ...])
```

## Libget
### lib
Appstore Workbench contains a python module for interacting with libget-style repos. It was written to be objective so multiple instances of it could be used at once, allowing the management of multiple consoles on the same sd card. This is useful in some cases, for example people using both WiiU and Wii (through vwii) homebrew. It also means the libget standard can be used locally for package management within the app, examples being payload injectors, and its the apps own plugin system.

### Compatibility
Appstore Workbench is mostly compatible with 4TU's Homebrew Appstore there are still a few small things to tweak like checking asset modes when updating.

## Special Thanks:
- pwscind
  - Answered all sorts of questions about the appstore repos
- vgmoose
  - <3
- The rest of the 4TU team for being gorgeous
- CrafterPika
  - Helped me get the app working with the WiiU since I don't have a one.
  - Helped with WiiUExploit plugin
- Archbox
  - Fellow Turtle
  - Wii Testing
- Circuit10
  - HTML friend
