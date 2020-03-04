#A basic python object for parsing the appstore json into lists per category
#Copyright LyfeOnEdge 2019
#Licensed under GPL3

import json
import asyncio

#python object to hold appstore repo
class parser(object):
    def __init__(self):
        self.init()
    
    def init(self):
        self.all = []
        self.advanced = []
        self.emus = []
        self.games = []
        self.loaders = []
        self.themes = []
        self.tools = []
        self.misc = []
        self.legacy = []

        self.map = {
            "advanced" : self.advanced,
            "concept" : self.misc,
            "emu" : self.emus,
            "game" : self.games,
            "loader" : self.loaders,
            "theme" : self.themes,
            "tool" : self.tools,
            "_misc" : self.misc,
            "media" : self.misc,
            "misc" : self.misc,
            "legacy" : self.legacy,
        }

        self.list_list = [self.all, self.advanced, self.emus, self.games, self.loaders, self.themes, self.tools, self.misc, self.legacy]

    def clear(self):
        self.init()
        
    #Loads appstore json as a large list of dicts
    def load_file(self, repo_json):
        if not repo_json:
            raise
        self.clear()
        try:
            with open(repo_json, encoding="utf-8") as repojson:
                self.all = json.load(repojson)["packages"]
            self.sort()
        except Exception as e:
            print(f"Exception loading appstore json {e}")
        num_entries = len(self.all)
        print(f"Loaded {num_entries} appstore entries")

    #Loads appstore json as a large list of dicts
    def load_json(self, repo_json):
        if not repo_json:
            raise
        self.clear()
        self.all = repo_json["packages"]
        self.sort()
        num_entries = len(self.all)
        print(f"Loaded {num_entries} appstore entries")

    def get_package_dict(self, packagename: str):
        for package in self.all:
            if package["name"] == packagename:
                return package

    #sorts list into smaller chunks
    def sort(self):
        if self.all:
            for entry in self.all:
                try:
                    self.map[entry["category"]].append(entry)
                except:
                    pkg = entry["name"]
                    print(f"Error sorting {pkg}")
        else:
            raise


#A basic python object for parsing the appstore json into lists per category
#Copyright LyfeOnEdge 2019
#Licensed under GPL3

# import json

# #python object to hold appstore repo
# class parser(object):
# 	def __init__(self):
# 		self.init()
	
# 	def init(self):
# 		self.all = []
# 		self.categories = {}

# 	def clear(self):
# 		self.init()
		
# 	#Loads appstore json as a large list of dicts
# 	def load_file(self, repo_json):
# 		if not repo_json:
# 			raise
# 		self.clear()
# 		try:
# 			with open(repo_json, encoding="utf-8") as repojson:
# 				self.all = json.load(repojson)["packages"]
# 			self.sort()
# 			num_entries = len(self.all)
# 			print(f"Loaded {num_entries} appstore entries")
# 		except Exception as e:
# 			print(f"Exception loading appstore json {e}")
		
# 	#Loads appstore json as a large list of dicts
# 	def load_json(self, repo_json):
# 		if not repo_json:
# 			raise
# 		self.clear()
# 		self.all = repo_json["packages"]
# 		self.sort()
# 		num_entries = len(self.all)
# 		print(f"Loaded {num_entries} appstore entries")

# 	def get_package(self, packagename):
# 		for package in self.all:
# 			if package["name"] == packagename:
# 				return package

# 	#sorts list into smaller chunks
# 	def sort(self):
# 		if self.all:
# 			for entry in self.all:
# 				try:
# 					if entry["category"] in self.categories.keys():
# 						self.categories[entry["category"]].append(entry)
# 					else:
# 						self.categories[entry["category"]] = entry
# 				except:
# 					pkg = entry["name"]
# 					print(f"Error sorting {pkg}")
# 				print(f"Found {len(self.categories.keys())} categories")
# 		else:
# 			raise