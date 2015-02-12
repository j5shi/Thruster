#-*- coding: utf-8 -*
"""
@author: Jia Shi
@email: j5shi@live.com
@last update: 2015-02-11 10:19:20
@version: 0.1
@license: GNU GPL v2
"""
import launchy
import subprocess
import os

class PyVerby(launchy.Plugin):

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

        self.name = "PyVerby"
        self.hash = launchy.hash(self.name)
        self.icon = os.path.join(launchy.getIconsPath(), "%s.png" % self.name)
        
        # Total Commander
        self.totalcmdLongname = "Open in Total Commander"
        self.totalcmdShortname = "Totalcmd"
        self.totalcmdID = self.getID()
        self.totalcmdIcon = os.path.join(launchy.getIconsPath(), "Totalcmd.png")
        self.totalcmdCatItem = launchy.CatItem(self.totalcmdLongname, self.totalcmdShortname, self.totalcmdID, self.totalcmdIcon)
        
        # VIM
        self.vimLongname = "Open in GVIM"
        self.vimShortname = "Vim"
        self.vimID = self.getID()
        self.vimIcon = os.path.join(launchy.getIconsPath(), "VIM.png")
        self.vimCatItem = launchy.CatItem(self.vimLongname, self.vimShortname, self.vimID, self.vimIcon)


    def init(self):
        """
        This message informs the plugin that it’s being loaded.

        This is a good time to do any initialization work.
        """
        print "instance created: %s" % self
        print "hash: %s" % self.hash
        print "name: %s" % self.name
        print "icon: %s" % self.icon
        print "init() executed successfully!"

    def getID(self):
        """
        Asks the Plugin for its ID Number.

        Launchy needs an unsigned int identification value for each loaded plugin.
        You supply your own here. Typically, this is the result of hashing a string,
        as shown in the example below.

        @return <int>: plugin ID.
        """
        return self.hash

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
        entries to Launchy’s primary catalog (until the catalog is rebuilt).

        It will be called when the primary catalog is rebuilt.

        @resultsList <list>: result list to append new entries (CatItem)
                             to, these will be copied over to the primary
                             catalog.
        """
        pass

    def getLabels(self, inputDataList):
        """
        Asks the plugin if it would like to apply a label to the
        current search query.

        It is sometimes useful to label user queries with plugin-defined tags.

        The InputData class stores the current user’s query. It is in a List
        structure because each time “tab” is pressed by the user a new InputData
        is formed and appended to the list. In other words, if the user typed
        “google <tab> this is my query” then inputDataList would represent a
        list of 2 InputData classes, with the first representing “google”, and
        the second, “this is my query”. Each InputData can be tagged individually.

        @inputDataList <List>: list of InputData, user’s search query.

        @Warning: This is called each time the user changes a character in his or
                  her query, so make sure it’s fast.
        """
        pass

    def getResults(self, inputDataList, resultsList):
        """
        Asks the plugin for any results to a query.

        If your plugin returns catalog results on the fly to a query (e.g. a website
        query for weby or a calculator result), then this is the place to do so. The
        existing results are stored in a ResultsList object, which is a CatItem‘s
        (short for Catalog Items) list. You can append your own results to it.

        @inputDataList <List>: list of InputData, user’s search query.
        @resultsList <List>: ResultsList holds the catalog items that are relevent to
                             a search query. Plugins that want to add new catalog items
                             for a search query should use this class.
        """
        if len(inputDataList) == 2 and os.path.exists(inputDataList[0].getTopResult().fullPath):
            resultsList.push_back(self.totalcmdCatItem)
            resultsList.push_back(self.vimCatItem)
            inputDataList[0].getTopResult().id = self.getID()

    def launchItem(self, inputDataList, catItem):
        """
        Instructs the plugin that one of its own catalog items
        was selected by the user and should now be executed.

        If the plugin adds items to the catalog via getResults()
        or getCatalog() and one of those items is selected by the
        user, then it is up to the plugin to execute it when the
        user presses “enter”. This is where you perform the action.

        @param inputDataList <List>: List of InputData, user’s search query.
        @param catItem <CatItem>: The user selected catalog item.
        """
        if len(inputDataList) == 2:
            if inputDataList[1].getTopResult().shortName == self.totalcmdShortname:
                subprocess.Popen('start TOTALCMD64.exe /O /A /T "%s"' % catItem.fullPath, shell=True)
            elif inputDataList[1].getTopResult().shortName == self.vimShortname:
                subprocess.Popen('"c:/Program Files (x86)/vim/vim74/gvim.exe" --remote-tab-silent "%s"' % catItem.fullPath, shell=True)

    def hasDialog(self):
        """
        Asks the plugin if it has a dialog to display in the options menu.

        @return <bool>: true if the plugin has a dialog, or false otherwise.
        """
        pass

    def doDialog(self, parentWidget):
        """
        Tells the plugin that it’s time to show its user interface.
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

launchy.registerPlugin(PyVerby)
