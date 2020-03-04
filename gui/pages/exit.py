import os, sys
import tkinter as tk
from tkinter.constants import *
from gui.widgets import themedLabel, button
from asyncthreader import threader
import style

class exitPage(tk.Frame):
	def __init__(self, app, parent):
		self.name = "EXIT"
		self.app = app
		tk.Frame.__init__(self,parent,background=style.primary_color)
		

		self.usertext = themedLabel.ThemedLabel(self, text="Exit?", font = style.hugeboldtext, anchor = "center", background = style.primary_color, foreground = "white")
		self.usertext.place(relwidth = 1, relheight = 1, height = - (style.buttonsize + 2 * style.offset))

		self.yesnobuttonframe = tk.Frame(self,background=style.primary_color, borderwidth = 0, highlightthickness = 0)
		self.yesnobuttonframe.place(relx=0.5,rely=1,y=- (style.buttonsize + style.offset),width=300,x=-150,height=style.buttonsize)

		self.yesbutton = button.Button(self.yesnobuttonframe, callback=self.on_yes,text_string="Yes",background=style.secondary_color)
		self.yesbutton.place(relx=0.33,relwidth=0.34,relheight=1)

	def on_yes(self):
		print("Exiting...")
		self.app.exit()

def setup(app, container):
	return exitPage(app, container)
