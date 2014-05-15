#-*- coding: utf-8 -*
"""
@author: Jia Shi
@email: j5shi@live.com
@data: 2014-05-15 8:29:49 AM 
@version: 0.1
@license: GNU GPL v2
=====================
Usage:

    1. clone the repository to your local machine.
    2. put  ./pybookkeeper.py to ./Launchy/plugins/python 
    3. put  ./icon/pybookkeeper.png to ./Launchy/plugins/icons 
    4. start Launchy and rebuild the catalog.
"""
import launchy
import subprocess
import os

#================== DEBUG BEGIN ==========================
DEBUG = False 
FH = None

if DEBUG:
    import atexit
    import time


def BOOKKEEPPER_DEBUG(log=None):
    global DEBUG
    global FH
    if DEBUG:
        if FH is None:
            logpath = os.path.join(os.environ["APPDATA"], "Launchy/pybookkeeper.log")
            FH = open(logpath, 'w', 1)
            atexit.register(FH.close)
        if log:
            FH.write("%s - %s\n" % (time.asctime(), log))
#================== DEBUG ENDS ==========================


class pybookkeeper(launchy.Plugin):
    global BOOKKEEPPER_DEBUG

    def __init__(self):
        launchy.Plugin.__init__(self)
        self.name = "pybookkeeper"
        self.hash = launchy.hash(self.name)
        self.icon = os.path.join(launchy.getIconsPath(), "pybookkeeper.png")
        self.bookmarks = {}

        BOOKKEEPPER_DEBUG("instance created: %s" % self)
        BOOKKEEPPER_DEBUG("name: %s" % self.name)
        BOOKKEEPPER_DEBUG("hash: %s" % self.hash)
        BOOKKEEPPER_DEBUG("icon: %s" % self.icon)

    def init(self):
        """Function to do initializations.
        """
        BOOKKEEPPER_DEBUG("init() is executed successfully!")

    def getID(self):
        return self.hash

    def getName(self):
        return self.name

    def getIcon(self):
        return self.icon

    def getLabels(self, inputDataList):
        """Callback function to asks the plugin if it 
        would like to apply a label to the current search query.
        """
        BOOKKEEPPER_DEBUG("getLabels() is executed successfully!")

    def getResults(self, inputDataList, resultsList):
        """Callback function to ask the plugin for any results
        to a query.
        """
        BOOKKEEPPER_DEBUG("getResults() is executed successfully!")

    def getCatalog(self, resultsList):
        """Callback function to ask the plugin for a static catalog 
        to be added to the primary catalog. 
        
        It will be called when the primary catalog is rebuilt.
        """
        bookmarkFile = os.path.join(os.environ["localappdata"], "Google/Chrome/User Data/Default/Bookmarks")
        bookmarkManager = eval(open(bookmarkFile, 'r').read())
        bookmarkBar = bookmarkManager.get("roots", None).get("bookmark_bar", None).get("children", None)
        if bookmarkBar:
            for folder in bookmarkBar:
                for bm in folder.get("children", None):
                    self.bookmarks.update({bm.get("name", None): bm.get("url", None)})

        for key in self.bookmarks.keys():
            resultsList.append(launchy.CatItem(self.bookmarks.get(key), key, self.getID(), self.getIcon()))
            BOOKKEEPPER_DEBUG("%-20s: %s" % (key, self.bookmarks.get(key)))
        BOOKKEEPPER_DEBUG("getCatalog() is executed successfully.\n")

    def launchItem(self, inputDataList, catItemOrig):
        """Instructs the plugin that one of its own catalog items 
        was selected by the user and should now be executed.

        If the plugin adds items to the catalog via getResults() 
        or getCatalog() and one of those items is selected by the 
        user, then it is up to the plugin to execute it when the 
        user presses “enter”. This is where you perform the action.
        """
        subprocess.call('start chrome "%s"' % catItemOrig.fullPath, shell=True)

launchy.registerPlugin(pybookkeeper)
