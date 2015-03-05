# -*- coding: utf-8 -*-
"""
@author: Jia Shi
@email: j5shi@live.com
@last update: 2015-02-26 17:32:35
@version: 0.5
@license: GNU GPL v2
"""
import launchy
import subprocess
import os
import urllib
from PyQt4 import QtGui, QtCore


PLUGIN_NAME = "PyUltima"
PLUGIN_ID = launchy.hash(PLUGIN_NAME)


class Base(object):

    def getPluginId(self):
        return PLUGIN_ID

    def getPluginName(self):
        return PLUGIN_NAME

    def getIconsPath(self, filename):
        return os.path.join(launchy.getIconsPath(), filename)

    def getCatItem(self, fullPath, shortName, id, icon):
        return launchy.CatItem(fullPath, shortName, id, icon)

    def getResults(self, inputDataList, resultsList):
        pass

    def getCatalog(self, resultsList):
        pass

    def getLabels(self, inputDataList):
        pass



class WebSearch(Base):

    searchEngine = {"url": {"url": "%s", "name": "Web"},
                    "gg": {"url": "https://www.google.com/?gws_rd=ssl#q=%s", "name": "Google"},
                    "bb": {"url": "http://www.bing.com/search?q=%s", "name": "Bing"},
                    "bk": {"url": "http://baike.baidu.com/search?word=%s", "name": "Baidu Baike"},
                    "bd": {"url": "https://www.baidu.com/s?wd=%s", "name": "Baidu"},
                    "tao": {"url": "http://s.taobao.com/search?q=%s", "name": "Taobao"},
                    "pr": {"url": "http://prontoa02.int.net.nokia.com/nokia/pronto/pronto.nsf/PRID/%s?OpenDocument", "name": "Pronto"}, }

    def __init__(self):
        self.id = self.getPluginId()
        self.icon = self.getIconsPath("WebSearch.png")

    def getResults(self, inputDataList, resultsList):
        key = inputDataList[0].getText()
        if key in self.searchEngine.keys():
            resultsList.push_front(self.getCatItem("%s: %s search" % (self.getPluginName(), self.searchEngine.get(key).get("name")),
                                                   "%s" % key,
                                                   self.id,
                                                   self.icon))

    def launchItem(self, inputDataList, catItem):
        if catItem.icon == self.icon:
            key = inputDataList[0].getText()
            if key != "url":
                query = urllib.quote(inputDataList[-1].getText().encode("utf8"))
                url = eval('"%s" %% "%s"' % (self.searchEngine.get(key).get('url'), query))
            else:
                url = inputDataList[-1].getText()
            subprocess.Popen('start chrome "%s"' % url, shell=True)
            return True


class RunCommands(Base):

    CmdAlias = {"putty": "putty.exe",
                "linsee40": 'putty -load "hzling40.china.nsn-net.net"',
                "linsee42": 'putty -load "hzling42.china.nsn-net.net"',
                "vm134": 'putty -load "10.68.203.134"',
                "switch": 'putty -load "Cisco_3560"',
                "cmd": "conemu64", }

    def __init__(self):
        self.id = self.getPluginId()
        self.icon = self.getIconsPath("RunCommands.png")

        self.triggerStr = "Run"


    def getResults(self, inputDataList, resultsList):
        for alias in self.CmdAlias.keys():
            resultsList.push_front(self.getCatItem("%s: Run commands" % (self.getPluginName()),
                                                    alias,
                                                    self.id,
                                                    self.icon))

        if inputDataList[0].getText().strip().lower() == self.triggerStr.lower():
            resultsList.push_front(self.getCatItem("%s: Run commands" % (self.getPluginName()),
                                                    self.triggerStr,
                                                    self.id,
                                                    self.icon))

    def launchItem(self, inputDataList, catItem):
        if catItem.icon == self.icon:
            if len(inputDataList) == 1:
                cmd = self.CmdAlias.get(catItem.shortName)
            else:
                if len(inputDataList[-1].getText().strip()) == 0:
                    cmd = self.CmdAlias.get(inputDataList[-1].getTopResult().shortName, None)
                elif self.CmdAlias.get(inputDataList[-1].getText(), None):
                    cmd = self.CmdAlias.get(inputDataList[-1].getText(), None)
                else:
                    cmd = "conemu64 /cmd %s" % inputDataList[-1].getText()

            print cmd
            if cmd is not None:
                subprocess.Popen(cmd)
            return True

class Browser(Base):

    def __init__(self):
        self.id = self.getPluginId()
        self.icon = self.getIconsPath("Chrome.png")

    def launchItem(self, inputDataList, catItem):
        if catItem.icon == self.icon:
            subprocess.Popen('start chrome "%s"' % catItem.fullPath, shell=True)
            return True

    def getCatalog(self, resultsList):
        """
        Callback function to asks the plugin for a static catalog to be
        added to the primary catalog. Some plugins will add permanent
        entries to Launchy primary catalog (until the catalog is rebuilt).

        It will be called when the primary catalog is rebuilt.

        @resultsList <list>: result list to append new entries (CatItem)
                             to, these will be copied over to the primary
                             catalog.
        """
        browserBookmarks = {}
        bookmarkFile = os.path.join(os.environ["localappdata"], "Google/Chrome/User Data/Default/Bookmarks")
        bookmarkManager = eval(open(bookmarkFile, 'r').read())
        bookmarkBar = bookmarkManager.get("roots", None).get("bookmark_bar", None).get("children", None)
        if bookmarkBar:
            for folder in bookmarkBar:
                for bm in folder.get("children", None):
                    browserBookmarks.update({bm.get("name", None): bm.get("url", None)})

        for key in browserBookmarks.keys():
            resultsList.append(self.getCatItem(browserBookmarks.get(key), key, self.id, self.icon))

class DefaultHandler(Base):

    def __init__(self):
        self.id = self.getPluginId()
        self.icon = self.getIconsPath("DefaultHandler.png")

    def launchItem(self, inputDataList, catItem):
        launchy.runProgram('"%s"' % catItem.fullPath, "")
        return True


class PyUltima(launchy.Plugin):

    """
    http://pylaunchy.sourceforge.net/docs/launchy.html#launchy.Plugin.launchyShow
    https://github.com/leonid-shevtsov/launchy/blob/master/plugins/verby/Verby.cpp

    This class represents a Launchy Python plugin.

    By combining a script that has a class that inherits from Plugin and
    the launchy module itself, Python scripts can be added to Launchy as
    real plugins.

    Every plugin needs to be registered using the launchy.registerPlugin() function.
    """

    def __init__(self):
        """
        Every plugin should have the following __init__ function.
        """
        launchy.Plugin.__init__(self)

        self.name = PLUGIN_NAME
        self.id = PLUGIN_ID
        self.icon = os.path.join(launchy.getIconsPath(), "%s.png" % self.name)

    def init(self):
        """
        This message informs the plugin that it is being loaded.

        This is a good time to do any initialization work.
        """
        print "=============================="
        print "instance created: %s" % self
        print "hash: %s" % self.getID()
        print "name: %s" % self.getName()
        print "icon: %s" % self.getIcon()
        print "loading addons:"
        self.addons = []
        self.registerAddon(Browser)
        self.registerAddon(WebSearch)
        self.registerAddon(RunCommands)
        self.registerAddon(DefaultHandler)
        print "finished loading addons."
        print "=============================="

    def registerAddon(self, addon):
        a = addon()

        if type(a).__name__ != "DefaultHandler":
            self.addons.insert(0, a)
        else:
            # the DefaultHandler should always be the
            # last addon to process queries
            self.addons.append(a)

        print "  - %s loaded" % type(a).__name__

    def getID(self):
        """
        Asks the Plugin for its ID Number.

        Launchy needs an unsigned int identification value for each loaded plugin.
        You supply your own here. Typically, this is the result of hashing a string,
        as shown in the example below.

        @return <int>: plugin ID.
        """
        return self.id

    def getName(self):
        """
        Asks the plugin for its string name.

        @return <str>: plugin name.
        """
        return self.name

    def getIcon(self):
        """
        @return <str>: icon filename.
        """
        return self.icon

    def getCatalog(self, resultsList):
        """
        Callback function to asks the plugin for a static catalog to be
        added to the primary catalog. Some plugins will add permanent
        entries to Launchy primary catalog (until the catalog is rebuilt).

        It will be called when the primary catalog is rebuilt.

        @resultsList <list>: result list to append new entries (CatItem)
                             to, these will be copied over to the primary
                             catalog.
        """
        for addon in self.addons:
            addon.getCatalog(resultsList)

    def getLabels(self, inputDataList):
        """
        Asks the plugin if it would like to apply a label to the
        current search query.

        It is sometimes useful to label user queries with plugin-defined tags.

        The InputData class stores the current user query. It is in a List
        structure because each time "tab" is pressed by the user a new InputData
        is formed and appended to the list. In other words, if the user typed
        "google <tab> this is my query" then inputDataList would represent a
        list of 2 InputData classes, with the first representing "google", and
        the second, "this is my query". Each InputData can be tagged individually.

        @inputDataList <List>: list of InputData, user's search query.

        @Warning: This is called each time the user changes a character in his or
                  her query, so make sure it's fast.
        """
        for addon in self.addons:
            addon.getLabels(inputDataList)

    def getResults(self, inputDataList, resultsList):
        """
        Asks the plugin for any results to a query.

        If your plugin returns catalog results on the fly to a query (e.g. a website
        query for weby or a calculator result), then this is the place to do so. The
        existing results are stored in a ResultsList object, which is a CatItem's
        (short for Catalog Items) list. You can append your own results to it.

        @inputDataList <List>: list of InputData, user's search query.
        @resultsList <List>: ResultsList holds the catalog items that are relevent to
                             a search query. Plugins that want to add new catalog items
                             for a search query should use this class.
        """
        # handle everything by us
        inputDataList[0].setID(self.getID())

        for addon in self.addons:
            addon.getResults(inputDataList, resultsList)

    def launchItem(self, inputDataList, catItem):
        """
        Instructs the plugin that one of its own catalog items
        was selected by the user and should now be executed.

        If the plugin adds items to the catalog via getResults()
        or getCatalog() and one of those items is selected by the
        user, then it is up to the plugin to execute it when the
        user presses "enter". This is where you perform the action.

        @param inputDataList <List>: List of InputData, user's search query.
        @param catItem <CatItem>: The user selected catalog item.
        """
        for addon in self.addons:
            if addon.launchItem(inputDataList, catItem):
                print type(addon).__name__
                break

    def hasDialog(self):
        """
        Asks the plugin if it has a dialog to display in the options menu.

        @return <bool>: true if the plugin has a dialog, or false otherwise.
        """
        pass

    def doDialog(self, parentWidget):
        """
        Tells the plugin that it's time to show its user interface.
        The function should create the widget and return it.

        - The plugin is passed a raw C++ pointer. It should be converted to QWidget
          by the user with SIP function wrapinstance.
        - SIP documentation can be found here.
        - The creation of plugin widgets should be done with PyQt4.
        - PyQt4 Documentation and Tutorial are available from PythonInfo Wiki.

        @parentWidget <void*>: The parent widget of all plugin widgets. Call wrapinstance to use it.
        @return       <void*>: The result of unwrapinstance( myPluginWidget )
        """
        pass

    def endDialog(self, accept):
        """
        Informs the plugin that it should close its dialog.

        @accept <bool>: whether the plugin should accept changes made by the
                        user while the dialog was open
        """
        pass

    def launchyShow(self):
        """
        This message informs the plugin that Launchy is now
        visible on the screen.
        """
        pass

    def launchyHide(self):
        """
        This message informs the plugin that Launchy is no
        longer visible on the screen.

        Note: this function will not be called if another
        plugin function has not returned yet (e.g. Launchy
        is hidden in the middle of launchItem()).
        """
        pass

launchy.registerPlugin(PyUltima)
