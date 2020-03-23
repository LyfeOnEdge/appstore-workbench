from tkinter import Entry, StringVar
from style import *

class ThemedEntry(Entry):
	def __init__(self, frame, text = None, font = mediumtext, foreground = secondary_text_color, background = secondary_color, anchor = "w"):
		self.text_var = StringVar()
		Entry.__init__(self, frame, 
			font = font,
			foreground = foreground,
			background = background,
			borderwidth = 0,
			highlightthickness = 0,
			exportselection = False,
			textvariable = self.text_var
		)
		self.set(text)

	def clear(self):
		self.text_var.set("")

	def set(self, string):
		self.text_var.set(string)

	def get_var(self):
		return self.text_var

	def get(self):
		return self.text_var.get()