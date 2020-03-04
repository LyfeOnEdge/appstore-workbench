from .categoryPage import CategoryPage
import tkinter as tk

class InstalledCategoryPage(CategoryPage):
	def __init__(self,
				 app: tk.Tk,
				 container: tk.Frame,
				 appstore_handler,
				 category_name: str = "",
				 category_packages: list = [],
				 ):
		CategoryPage.__init__(self, app, container, appstore_handler, category_name, category_packages)
		self.packages = category_packages

	def get_current_packages(self):
		packages = self.search_packages(self.current_search)
		packages = [pkg for pkg in packages if self.appstore_handler.get_package_version(pkg["name"])]
		if self.sort_type:
			packages = self.sort_packages(packages, self.sort_type)
		return packages