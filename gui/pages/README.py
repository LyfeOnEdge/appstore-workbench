import tkinter as tk
import style
from gui.widgets.scrollingWidgets import ScrolledThemedText

class page(tk.Frame):
	def __init__(self, app, container):
		self.app = app
		self.name = "README"
		tk.Frame.__init__(self, container, background = "black")
		self.text = ScrolledThemedText(self, string = "", font = style.mediumtext)
		self.text.place(relwidth=1, relheight =1)
		with open("README.md") as README:
			self.text.set(README.read())

	def configure(self, event, force = False):
		pass

def setup(app, container):
	return page(app, container)