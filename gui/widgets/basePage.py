import tkinter as tk
import style

class BasePage(tk.Frame):
	def __init__(self, app, container: tk.Frame, name: str = ""):
		tk.Frame.__init__(self, container, background = style.PAGE_BACKGROUND)
		self.app = app
		self.name = name
		self.bind("<<ShowFrame>>", self.on_show_frame) #Bind showframe event so frame reloads when raised

	def show(self):
		self.event_generate("<<ShowFrame>>")
		self.tkraise()
		print(f"Raised - {self.name}")

	def on_show_frame(self, event = None):
		pass