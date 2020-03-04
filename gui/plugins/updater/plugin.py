import os
from appstore import Appstore
import style
from gui.widgets import basePage, basePlugin, button
import tkinter as tk
from .updater import Updater_tool
class updatePage(basePage.BasePage):
	def __init__(self, app, container, plugin):
		basePage.BasePage.__init__(self, app, container, "UPDATER")
		self.plugin = plugin

		self.label = tk.Label(self, background = style.secondary_color, font = style.smalltext, foreground = style.primary_text_color)
		self.label.place(relx = 0.5, rely = 0.5, width = 500, height = 400, y = - 200, x = - 250)

		self.yesbutton = button.Button(self, callback=self.plugin.update,text_string="Yes",background=style.secondary_color)

		if self.plugin.has_update:
			self.label.configure(text = "An update is available, would you like to update Appstore Workbench?")
			self.yesbutton.place(relx=0.5,rely=0.5,y=100,width=100,x=-50,height=style.buttonsize)
		else:
			self.label.configure(text = "No update for Appstore Workbench found.")

class Plugin(basePlugin.BasePlugin):
	def __init__(self, app, container):
		basePlugin.BasePlugin.__init__(self, app, "UPDATER", container)
		self.app = app
		self.container = container
		self.updater = Updater_tool("Appstore Workbench", "https://api.github.com/repos/LyfeOnEdge/appstore-workbench/releases", ["appstore-workbench", ".zip"])
		self.has_update = self.updater.check_for_update(app.version)

		if self.has_update:
			self.out("Found an update")
		else:
			self.out("No update available")

	def update(self):
		self.updater.update()

	def get_pages(self):
		return [updatePage(self.app, self.container, self)]

	def exit(self):
		pass

def setup(app, container):
	return Plugin(app, container)