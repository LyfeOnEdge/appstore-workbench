Each page comes in the form of a module containing a class called "Page" which is a subclass of the BasePage an object found in ../widgets/basePage.py which is in turn a subclass of a tkinter `Frame` themed with a few colors and sizes from ../config.py
At the bottom of the module is a function called "setup" that gets called externally to init the page.
The setup function is called when the page is loaded and returns a tkinter frame,
the setup function is passed the tkinter root and the container to place the frame
in as a positional argument.

TLDR:
Pages are tk.Frame with a string name and access to the tk.root wi


Example:

```py
import tkinter as tk:
from widgets import basePage
class Page(basePage.BasePage):
	def __init__(self, app, container):
		self.app = app
		self.name = "test"
		basePage.BasePage.__init__(self, container)

def setup(app, container):
	return page(app, container)
```