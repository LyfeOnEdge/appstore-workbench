from gui.plugins import basePlugin
import os
import tkinter as tk


class Plugin(basePlugin.BasePlugin):
	def __init__(self, app, container):
		basePlugin.BasePlugin.__init__(self, app, "PLUGINS", container)
		self.app = app
		self.container = container

	def get_pages(self):
		return []

	def exit(self):
		pass

def setup(app, container):
	return Plugin(app, container)
