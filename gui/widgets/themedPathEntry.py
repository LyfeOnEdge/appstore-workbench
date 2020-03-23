# from .themedEntry import ThemedEntry
import tkinter as tk

from .themedFrame import ThemedFrame 
from .button import Button
import style

class ThemedPathEntry(tk.Entry):
	def __init__(self, frame, *args, **kw):
		container = ThemedFrame(frame)
		Button(container, self.set_path, text_string = "...").place(relheight = 1, relx = 1, x = - style.buttonsize, width = style.buttonsize)
		tk.Entry.__init__(self, container, *args, **kw)
		self.text_var = tk.StringVar()
		self.configure(textvariable = self.text_var)
		super().place(relwidth = 1, relheight = 1, width = - style.buttonsize)
		self.container = container

	def clear(self):
		self.text_var.set("")

	def set(self, string):
		self.text_var.set(string)

	def get_var(self):
		return self.text_var

	def get(self):
		return self.text_var.get()

	def place(self, **kw):
		self.container.place(**kw)

	def set_path(self):
		self.set(tk.filedialog.askopenfilename())