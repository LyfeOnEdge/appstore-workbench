#Some basic scripts for grabbing icon and screenshot for packages using the appstore site.
#Copyright LyfeOnEdge 2019
#Licensed under GPL3
import os
import sys
import urllib.request 

import config

opener = urllib.request.build_opener()
opener.addheaders = [('User-agent', 'Mozilla/5.0')]
urllib.request.install_opener(opener)

DOWNLOADSFOLDER = "downloads"

CACHEFOLDER = "cache"
ICON  = "icon.png"
SCREEN = "screen.png"

lib_path = os.path.dirname(os.path.realpath(__file__))
#To blacklist icons
#create a file in the same folder as this on
#Call it icon_blacklist.txt
#Put the package name you'd like to blacklist on it's own line 
blacklist = os.path.join(lib_path, "icon_blacklist.txt")
ICONBLACKLIST = []
if os.path.isdir(blacklist):
    with open(blacklist) as blacklistfile:
        ICONBLACKLIST = blacklistfile.read()
        print("Loaded icon blacklist {}".format(ICONBLACKLIST))

SCREENBUFFER = {}
ICONBUFFER = {}
class appstore_webhandler:
    def __init__(self, repo_url):
        self.repo_url = repo_url
        appstore_url = "{}{}".format(repo_url, "{}")
        self.image_base_url = appstore_url.format("packages/{}/{}")
        self.appstore_package_url = "{}zips/{}.zip".format(repo_url, "{}")

    def download(self, url,file,silent = False):
        try:
            urllib.request.urlretrieve(url,file)
            return file
        except Exception as e:
            if not silent:
                print("failed to download file - {} from url - {}, reason: {}".format(file, url, e)) 
            return None

    #Gets (downloads or grabs from cache) an image of a given type (icon or screenshot) for a given package
    def getImage(self, package, image_type, force = False):
        path = os.path.join(os.path.join(sys.path[0], CACHEFOLDER), package.replace(":",""))
        if not os.path.isdir(path):
            os.mkdir(path)

        image_file = os.path.join(path, image_type)

        if os.path.isfile(image_file) and not force:
            return(image_file)
        else:
            return self.download(self.image_base_url.format(package, image_type), image_file, silent = True)

    def getPackageIcon(self, package, force = False):
        if not package in ICONBLACKLIST:
            if package in ICONBUFFER.keys():
                return ICONBUFFER[package]
            icon = self.getImage(package, ICON, force = force)
            ICONBUFFER.update({package : icon})
            return icon

    def getScreenImage(self, package, force = False):
        if package in SCREENBUFFER.keys():
            return SCREENBUFFER[package]
        screen = self.getImage(package, SCREEN, force = force)
        SCREENBUFFER.update({package : screen})
        return screen

    #Downloads the current zip of a package
    def getPackage(self, package):
        try:
            downloadsfolder = os.path.join(sys.path[0], DOWNLOADSFOLDER)
            packageURL = self.appstore_package_url.format(package)
            packagefile = os.path.join(downloadsfolder, "{}.zip".format(package))
            return self.download(packageURL, packagefile)
        except Exception as e:
            print("Error getting package zip for {} - {}".format(package, e))