from tkinter import Listbox
import style

class ThemedListbox(Listbox):
	def __init__(self,frame, foreground = style.lg, highlightthickness = 0, background = style.primary_color, font = style.largetext, borderwidth = 0, disabledforeground = style.lg):
		Listbox.__init__(self,frame,
			background = background,
			selectbackground = style.secondary_color,
			borderwidth = borderwidth,
			highlightthickness=highlightthickness,
			foreground= foreground,
			font = font,
			activestyle=None,
			exportselection = False,
			disabledforeground = style.llg
		)