#-*- coding: utf-8 -*
"""
@author: Jia Shi
@email: j5shi@live.com
@last update: 2015-01-27 12:29:31
@version: 0.1
@license: GNU GPL v2
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


def Debugger(log=None):
    global DEBUG
    global FH
    if DEBUG:
        if FH is None:
            logpath = os.path.join(os.environ["APPDATA"], "Launchy/BookmarkMgr.log")
            FH = open(logpath, 'w', 1)
            atexit.register(FH.close)
        if log:
            FH.write("%s - %s\n" % (time.asctime(), log))
#================== DEBUG ENDS ==========================


class BookmarkMgr(launchy.Plugin):
    global Debugger

    def __init__(self):
        launchy.Plugin.__init__(self)
        self.name = "BookmarkMgr"
        self.hash = launchy.hash(self.name)
        self.icon = os.path.join(launchy.getIconsPath(), "BookmarkMgr.png")
        self.bookmarks = {}

        Debugger("instance created: %s" % self)
        Debugger("name: %s" % self.name)
        Debugger("hash: %s" % self.hash)
        Debugger("icon: %s" % self.icon)

    def init(self):
        """Function to do initializations.
        """
        Debugger("init() is executed successfully!")

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
        Debugger("getLabels() is executed successfully!")

    def getResults(self, inputDataList, resultsList):
        """Callback function to ask the plugin for any results
        to a query.
        """
        Debugger("getResults() is executed successfully!")

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

                children = folder.get("children", None)

                if children is not None:
                    for bm in children:
                        self.bookmarks.update({bm.get("name", None): bm.get("url", None)})
                else:
                    self.bookmarks.update({folder.get("name", None): folder.get("url", None)})

        for key in self.bookmarks.keys():
            resultsList.append(launchy.CatItem(self.bookmarks.get(key), key, self.getID(), self.getIcon()))
            Debugger("%-20s: %s" % (key, self.bookmarks.get(key)))
        Debugger("getCatalog() is executed successfully.\n")

    def launchItem(self, inputDataList, catItemOrig):
        """Instructs the plugin that one of its own catalog items
        was selected by the user and should now be executed.

        If the plugin adds items to the catalog via getResults()
        or getCatalog() and one of those items is selected by the
        user, then it is up to the plugin to execute it when the
        user presses “enter”. This is where you perform the action.
        """
        # don't remove the surrounding of "%s", otherwise some URLs will
        # cause unexpected parsing exceptions when & is included in the URL.
        subprocess.Popen('start chrome "%s"' % catItemOrig.fullPath, shell=True)

launchy.registerPlugin(BookmarkMgr)
