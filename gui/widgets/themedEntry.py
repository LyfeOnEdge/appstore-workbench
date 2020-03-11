from tkinter import Entry, StringVar
from style import *

class ThemedEntry(Entry):
	def __init__(self, frame, font = mediumtext, foreground = secondary_text_color, background = secondary_color, anchor = "w"):
		Entry.__init__(self, frame, 
			font = font,
			foreground = foreground,
			background = background,
			borderwidth = 0,
			highlightthickness = 0,
			exportselection = False
		)
		self.text_var = StringVar()
		self.configure(textvariable = self.text_var)

	def clear(self):
		self.text_var.set("")

	def set(self, string):
		self.text_var.set(string)

	def get_var(self):
		return self.text_var

	def get(self):
		return self.text_var.get()