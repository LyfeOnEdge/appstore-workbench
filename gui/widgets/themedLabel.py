from tkinter import Label
import style

#themed author/ etc label
class ThemedLabel(Label):
	def __init__(self,frame,text="",font=style.smalltext,text_variable=None,background = style.primary_color,foreground=style.lg,anchor="w",wraplength = None):
		Label.__init__(self,frame,
			background = background,
			highlightthickness=0,
			anchor=anchor,
			text = text,
			font=font,
			foreground= foreground,
			textvariable = text_variable,
			)
		if not wraplength == None:
			self.configure(wraplength=wraplength)
	def set(self,text):
		self.configure(text=text)