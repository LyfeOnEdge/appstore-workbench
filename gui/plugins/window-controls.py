from gui.widgets import basePlugin

"""keyboard shortcuts for the app"""
class Plugin(basePlugin.BasePlugin):
	def __init__(self, app, container):
		basePlugin.BasePlugin.__init__(self, app, "window-controls", container)
		self.app = app
		self.container = container
		self.fullScreenState = False,
		self.zoomedScreenState = False,
		self.topmostScreenState = False,

		self.screen_attributes = {
			"-topmost",
			"-zoomed",
			"fullscreen"
		}
		
		self.app.bind("<F9>", self.toggle_topmost_screen)
		self.app.bind("<F10>", self.toggle_zoomed_screen)
		self.app.bind("<F11>", self.toggle_full_screen)
		self.app.bind("<Escape>", self.on_escape)

	def toggle_topmost_screen(self, event):
		self.topmostScreenState = not self.topmostScreenState
		self.app.attributes("-topmost", self.topmostScreenState)
		
	def toggle_zoomed_screen(self, event):
		self.zoomedScreenState = not self.zoomedScreenState
		self.app.attributes("-zoomed", self.zoomedScreenState)

	def toggle_full_screen(self, event):
		self.fullScreenState = not self.fullScreenState
		self.app.attributes("-fullscreen", self.fullScreenState)

	def on_escape(self, event):
		self.fullScreenState = False
		self.app.attributes("-fullscreen", self.fullScreenState)

	def get_pages(self):
		return []

	def exit(self):
		pass

def setup(app, container):
	return Plugin(app, container)