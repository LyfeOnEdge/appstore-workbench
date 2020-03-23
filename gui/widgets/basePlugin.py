# See main readme for info on plugins.

class BasePlugin:
	def __init__(self, app, name, container):
		self.name = name
		self.app = app
		self.container = container #Tk frame to hold any generated pages

	#Should return a list of pages subclassed from the BasePage object found in ../widgets/basePage
	#OK to return an empty list if plugin runs in the background
	def get_pages(self):
		return list()

	def exit(self):
		"""Exit function to stop background tasks, you should re-define this in your subclassed objects"""
		print("Exited the basePlugin")

	def out(self, outobj):
		print(f"[PLUGIN] - {self.name} - {outobj}")