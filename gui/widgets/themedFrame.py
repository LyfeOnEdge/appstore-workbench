from tkinter import Frame
import style

class ThemedFrame(Frame):
	"""A themed tkinter frame"""
	def __init__(self, frame, background=style.primary_color):
		Frame.__init__(
			self,
			frame,
			background=background,
			highlightcolor="white",
			highlightthickness=0,
			highlightbackground="grey",
			borderwidth=0
		)
