import json
import os
import shutil
import sys

def repo_entry():
	entry = {
		"category": "", 
		"binary": "", 
		"updated": "", 
		"name": "", 
		"license": "N/A", 
		"title": "", 
		"url": "", 
		"description": "", 
		"author": "", 
		"changelog": "", 
		"extracted": "",
		"version": "", 
		"filesize": "", 
		"web_dls": "", 
		"details": "", 
		"app_dls": "", 
	}
	return entry

#python object to hold appstore repo
class parser(object):
	def __init__(self):
		self.init()
	
	def init(self):
		self.all = []
		self.emus = []
		self.games = []
		self.tools = []
		self.misc = []

		self.map = {
			"advanced" : [],
			"concept" : [],
			"emu" : self.emus,
			"game" : self.games,
			"loader" : [],
			"theme" : [],
			"tool" : self.tools,
			"_misc" : [],
			"misc" : self.misc,
			"demo" : self.misc,
			"legacy" : [],
		}

		self.list_list = [self.all, self.emus, self.games, self.tools, self.misc]

	def clear(self):
		self.init()
		
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
		print(f"Loaded {num_entries} packages")
		
	#Loads appstore json as a large list of dicts
	def load_json(self, repo_json):
		if not repo_json:
			raise
		self.clear()
		self.all = repo_json["packages"]
		self.sort()
		num_entries = len(self.all)
		print(f"Loaded {num_entries} package entries")

	def get_package(self, packagename):
		for package in self.all:
			if package["name"] == packagename:
				return package

	#sorts list into smaller chunks
	def sort(self):
		if self.all:
			for entry in self.all:
				try:
					self.map[entry["category"]].append(entry)
				except Exception as e:
					print(e)
					pkg = entry["name"]
					print(f"Error sorting {pkg}")
		else:
			raise




