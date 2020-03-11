import os, socket
import tkinter as tk
from gui.widgets import basePlugin, basePage
from asyncthreader import threader
import style

ABOUT = "This is a template."

class Page(basePage.BasePage):
	def __init__(self, app, container, plugin):
		basePage.BasePage.__init__(self, app, container, "PAGE_NAME")
		self.plugin = plugin
		
		self.about_label = tk.Label(self, text = ABOUT, background = style.secondary_color, font = style.smalltext, foreground = style.secondary_text_color)
		self.about_label.place(relx = 0.5, rely = 0.5, width = 500, height = 400, y = - 200, x = - 250)

class Plugin(basePlugin.BasePlugin):
	def __init__(self, app, container):
		basePlugin.BasePlugin.__init__(self, app, "PLUGIN_NAME", container)
		self.app = app
		self.container = container

	def get_pages(self):
		return [Page(self.app, self.container, self)]

	def exit(self):
		pass

def setup(app, container):
	return Plugin(app, container)