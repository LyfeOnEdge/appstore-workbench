from .categorylistframe import categorylistFrame
import config

if config.CONSOLE in ["WiiU", "Switch"]:
    from appstore import Parser, Store_handler
elif config.CONSOLE == "Wii":
    from wiiappstore import Parser, Store_handler
else:
    raise "Invalid console"

class installedcategorylistFrame(categorylistFrame):
    def __init__(self,parent,controller,framework, packages):
        super().__init__(parent, controller, framework, packages)

    def get_current_packages(self):
        pkgs = self.appstore_handler.get_packages(silent = True)
        if pkgs:
            self.packages =  [Parser.get_package(pkg) for pkg in pkgs]

            packages = self.search_packages(self.current_search)
            if self.sort_type:
                packages = self.sort_packages(packages, self.sort_type)
            return packages