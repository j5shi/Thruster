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

        self.name = "PyUltima"
        self.pluginId = launchy.hash(self.name)
        self.icon = os.path.join(launchy.getIconsPath(), "%s.png" % self.name)
        self.defaultHandlerShortName = "Open in Default Program"

        # Search Engine
        self.searchEngine = {"url": {"url": "%s",
                                     "name": "Web"},
                             "gg": {"url": "https://www.google.com/?gws_rd=ssl#q=%s",
                                    "name": "Google"},
                             "bb": {"url": "http://www.bing.com/search?q=%s",
                                    "name": "Bing"},
                             "bk": {"url": "http://baike.baidu.com/search?word=%s",
                                    "name": "Baidu Baike"},
                             "bd": {"url": "https://www.baidu.com/s?wd=%s",
                                    "name": "Baidu"},
                             "tao": {"url": "http://s.taobao.com/search?q=%s",
                                     "name": "Taobao"},
                             "pr": {"url": "http://prontoa02.int.net.nokia.com/nokia/pronto/pronto.nsf/PRID/%s?OpenDocument",
                                    "name": "Pronto"}, }

        self.searchEngineFullPath = ""
        self.searchEngineShortName = "%s: search" % self.name
        self.searchEngineId = self.getID()
        self.searchEngineIcon = os.path.join(launchy.getIconsPath(), "WebSearch.png")
        self.searchEngineCatItem = launchy.CatItem(self.searchEngineFullPath,
                                                   self.searchEngineShortName,
                                                   self.searchEngineId,
                                                   self.searchEngineIcon)

        # Run Commands
        self.runCommandsCmdAlias = {"cmd": "conemu64"}
        self.runCommandsFullPath = "%s: run commands" % self.name
        self.runCommandsShortName = "Run"
        self.runCommandsId = self.getID()
        self.runCommandsIcon = os.path.join(launchy.getIconsPath(), "RunCommands.png")
        self.runCommandsCatItem = launchy.CatItem(self.runCommandsFullPath,
                                                  self.runCommandsShortName,
                                                  self.runCommandsId,
                                                  self.runCommandsIcon)

        # Open in Total Commander Left Panel
        self.totalcmdLeftPanelFullPath = ""
        self.totalcmdLeftPanelShortName = "%s: open in Totalcmd left panel" % self.name
        self.totalcmdLeftPanelId = self.getID()
        self.totalcmdLeftPanelIcon = os.path.join(launchy.getIconsPath(), "Totalcmd.png")
        self.totalcmdLeftPanelCatItem = launchy.CatItem(self.totalcmdLeftPanelFullPath,
                                                        self.totalcmdLeftPanelShortName,
                                                        self.totalcmdLeftPanelId,
                                                        self.totalcmdLeftPanelIcon)

        # Open in Total Commander Right Panel
        self.totalcmdRightPanelFullPath = ""
        self.totalcmdRightPanelShortName = "%s: open in Totalcmd right panel" % self.name
        self.totalcmdRightPanelId = self.getID()
        self.totalcmdRightPanelIcon = os.path.join(launchy.getIconsPath(), "Totalcmd.png")
        self.totalcmdRightPanelCatItem = launchy.CatItem(self.totalcmdRightPanelFullPath,
                                                         self.totalcmdRightPanelShortName,
                                                         self.totalcmdRightPanelId,
                                                         self.totalcmdRightPanelIcon)

        # Open in GVIM
        self.vimFullPath = ""
        self.vimShortName = "%s: open in Vim" % self.name
        self.vimId = self.getID()
        self.vimIcon = os.path.join(launchy.getIconsPath(), "VIM.png")
        self.vimCatItem = launchy.CatItem(self.vimFullPath,
                                          self.vimShortName,
                                          self.vimId,
                                          self.vimIcon)

        # Open in Browser
        self.browserBookmarks = {}
        self.browserFullPath = ""
        self.browserShortName = "%s: open in Google Chrome" % self.name
        self.browserId = self.getID()
        self.browserIcon = os.path.join(launchy.getIconsPath(), "Chrome.png")
        self.browserCatItem = launchy.CatItem(self.browserFullPath,
                                              self.browserShortName,
                                              self.browserId,
                                              self.browserIcon)

        # Default Handler
        self.defaultFullPath = ""
        self.defaultShortName = "%s: open in default program" % self.name
        self.defaultId = self.getID()
        self.defaultIcon = ""
        self.defaultCatItem = launchy.CatItem(self.defaultFullPath,
                                              self.defaultShortName,
                                              self.defaultId,
                                              self.defaultIcon)

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
        print "init() executed successfully!"
        print "=============================="

    def getID(self):
        """
        Asks the Plugin for its ID Number.

        Launchy needs an unsigned int identification value for each loaded plugin.
        You supply your own here. Typically, this is the result of hashing a string,
        as shown in the example below.

        @return <int>: plugin ID.
        """
        return self.pluginId

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
        bookmarkFile = os.path.join(os.environ["localappdata"], "Google/Chrome/User Data/Default/Bookmarks")
        bookmarkManager = eval(open(bookmarkFile, 'r').read())
        bookmarkBar = bookmarkManager.get("roots", None).get("bookmark_bar", None).get("children", None)
        if bookmarkBar:
            for folder in bookmarkBar:
                for bm in folder.get("children", None):
                    self.browserBookmarks.update({bm.get("name", None): bm.get("url", None)})

        for key in self.browserBookmarks.keys():
            resultsList.append(launchy.CatItem(self.browserBookmarks.get(key),
                                               key,
                                               self.browserId,
                                               self.browserIcon))

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
        pass

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
        inputDataList[0].setID(self.getID())

        if inputDataList[0].getText() in self.searchEngine.keys():
            key = inputDataList[0].getText()
            self.searchEngineCatItem.shortName = key
            self.searchEngineCatItem.fullPath = "%s %s" % (self.searchEngineShortName, self.searchEngine.get(key).get("name"))
            resultsList.push_front(self.searchEngineCatItem)
        elif inputDataList[0].getText().strip().lower() == self.runCommandsShortName.lower():
            resultsList.push_front(self.runCommandsCatItem)
        elif len(inputDataList) > 1:
            resultsList.push_back(self.totalcmdRightPanelCatItem)
            resultsList.push_back(self.totalcmdLeftPanelCatItem)
            resultsList.push_back(self.vimCatItem)
            resultsList.push_back(self.browserCatItem)
            resultsList.push_back(self.defaultCatItem)

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
        # using shortcuts
        if len(inputDataList) == 1:
            modifier = QtGui.QApplication.keyboardModifiers()

            if modifier == QtCore.Qt.ShiftModifier:
                inputDataList[-1].setText(self.totalcmdRightPanelShortName)
            elif modifier == QtCore.Qt.ControlModifier:
                inputDataList[-1].setText(self.totalcmdLeftPanelShortName)
        else:
            # use the top result if last query is empty
            if len(inputDataList[-1].getText().strip()) == 0:
                inputDataList[-1].setText(inputDataList[-1].getTopResult().shortName)

        ############################################################################
        # Using shortNames or icon path (in case shortNames have special meanings, #
        # like bookmark name) to decide which handler to handle                    #
        #                                                                          #
        # catItem always refers to the selected item in the result list of the     #
        # first member in inputDataList                                            #
        ############################################################################

        # launch chrome bookmarks
        if catItem.icon == self.browserIcon or inputDataList[-1].getText() == self.browserShortName:
            subprocess.Popen('start chrome "%s"' % catItem.fullPath, shell=True)

        # run commands
        elif catItem.icon == self.runCommandsIcon:
            cmd = self.runCommandsCmdAlias.get(inputDataList[-1].getText(), None)

            if cmd is None:
                cmd = "conemu64 /cmd %s" % inputDataList[-1].getText()

            subprocess.Popen(cmd)

        # web search
        elif inputDataList[0].getText() in self.searchEngine.keys():
            key = inputDataList[0].getText()
            if key != "url":
                query = urllib.quote(inputDataList[-1].getText().encode("utf8"))
                url = eval('"%s" %% "%s"' % (self.searchEngine.get(key).get('url'), query))
            else:
                url = inputDataList[-1].getText()
            subprocess.Popen('start chrome "%s"' % url, shell=True)

        # open in total commander left panel
        elif inputDataList[-1].getText() == self.totalcmdLeftPanelShortName:
            subprocess.Popen('start TOTALCMD64.exe /O /A /T /L="%s"' % catItem.fullPath, shell=True)

        # open in total commander right panel
        elif inputDataList[-1].getText() == self.totalcmdRightPanelShortName:
            subprocess.Popen('start TOTALCMD64.exe /O /A /T /R="%s"' % catItem.fullPath, shell=True)

        # open in gvim
        elif inputDataList[-1].getText() == self.vimShortName:
            subprocess.Popen('start gvim.exe --remote-tab-silent "%s"' % catItem.fullPath, shell=True)

        # open in default software
        else:
            launchy.runProgram('"%s"' % catItem.fullPath, "")

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