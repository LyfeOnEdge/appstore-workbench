from gui.widgets import basePlugin, categoryPage, themedFrame, button
import os
from appstore import Appstore
import style
import tkinter as tk

PAYLOAD_REPO = "https://www.brewtools.dev/appstore-workbench-plugins/"
LIBGET_DIR = ".get/packages"

WARNING = "You must restart the app for any\nplugin changes you make to take effect."

class PluginPage(categoryPage.CategoryPage):
	def __init__(self, app, container, handler):
		categoryPage.CategoryPage.__init__(self, app, container, handler, "PLUGINS", handler.all)
		self.warning_acknowledged = False

		self.warningframe = themedFrame.ThemedFrame(self)
		self.warningframe.place(relwidth = 1, relheight = 1)
		self.warning_label = tk.Label(self.warningframe, text = WARNING, background = style.primary_color, font = style.smalltext, foreground = style.primary_text_color)
		self.warning_label.place(relx = 0.5, rely = 0.5, width = 500, height = 50, y = - 25, x = - 250)
		self.ack_button = button.Button(self.warningframe, self.ack, text_string = "OK")
		self.ack_button.place(relx = 0.5, rely = 0.5, width = 100, height = 30, y = 50, x = - 50)

		self.bind("<Configure>", self.configure)

	def configure(self, event = None, force = False):
		if self.picked or force:
			self.rebuild()
		if not self.warning_acknowledged:
			self.warningframe.tkraise()

	def ack(self):
		self.warning_acknowledged = True
		self.warningframe.place_forget()

class Plugin(basePlugin.BasePlugin):
	def __init__(self, app, container):
		basePlugin.BasePlugin.__init__(self, app, "PLUGINS", container)
		self.app = app
		self.container = container
		self.handler = Appstore("plugins", PAYLOAD_REPO, LIBGET_DIR)
		self.handler.set_path("plugins")
		if not self.handler.check_if_get_init(silent = True):
			self.handler.init_get()

	def get_pages(self):
		plugin_page = PluginPage(self.app, self.container, self.handler)
		return [plugin_page]

	def exit(self):
		pass

def setup(app, container):
	return Plugin(app, container)