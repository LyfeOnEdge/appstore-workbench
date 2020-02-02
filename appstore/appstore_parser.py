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
        self.blacklisted_categories_list = []

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
            "misc" : self.misc,
            "legacy" : self.legacy,
        }

        self.list_list = [self.all, self.advanced, self.emus, self.games, self.loaders, self.themes, self.tools, self.misc, self.legacy]

    #Allows you to prevent certain categories in the map from being added to self.all[]
    def blacklist_categories(self, categories_list):
        self.blacklisted_categories_list = categories_list

    def clear_blacklist(self):
        self.blacklisted_categories_list = []

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
            if self.blacklisted_categories_list:
                for entry in self.all:
                    for category in self.blacklisted_categories_list:
                        if entry in self.map[category]:
                            self.all.remove(entry)
                            break
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
        if self.blacklisted_categories_list:
            for entry in self.all:
                for category in self.blacklisted_categories_list:
                    if entry in self.map[category]:
                        self.all.remove(entry)
                        break
        num_entries = len(self.all)
        print(f"Loaded {num_entries} appstore entries")

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
                except:
                    pkg = entry["name"]
                    print(f"Error sorting {pkg}")
        else:
            raise