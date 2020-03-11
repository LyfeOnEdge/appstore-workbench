from tkinter import Text
from style import *

class ThemedText(Text):
	def __init__(self, frame, string = "", font = mediumtext, foreground = primary_text_color, background = primary_color):
		Text.__init__(self, frame, wrap = "word", font = font, foreground = foreground, background = background, borderwidth = 0, highlightthickness = 0)
		self.set(string)

	def clear(self):
		self.configure(state="normal")
		self.delete('1.0', "end")
		self.configure(state="disabled")

	def set(self, string):
		self.configure(state="normal")
		self.delete('1.0', "end")
		self.insert("1.0", string)
		self.configure(state="disabled")

	def set_entry(self, string):
		self.configure(state="normal")
		self.delete('1.0', "end")
		self.insert("1.0", string)

	def get(self):
		return self.get("1.0","end")