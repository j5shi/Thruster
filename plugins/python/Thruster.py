# -*- coding: utf-8 -*-
import launchy
import subprocess
import os
import re
import urllib
import shutil
import pprint
import sys
from PyQt4 import QtGui, QtCore
import win32gui
from win32con import SW_RESTORE

class Logger(object):

    LOG_LEVEL_DBG, LOG_LEVEL_INF, LOG_LEVEL_WARN, LOG_LEVEL_ERR = range(4)

    # init log level
    LOG_LEVEL = LOG_LEVEL_INF

    def logger(self, level, log):
        if level >= self.LOG_LEVEL:
            print log

    def setLogLevel(self, level):
        self.LOG_LEVEL = level

    def getLogLevel(self, level):
        return self.LOG_LEVEL


class AddonBase(Logger):

    def __init__(self):
        self.resetAddonId()
        self.resetAddonTrigStrs()

        #  the following attributes needs to be updated in child class.
        self.icon = None

    def resetAddonId(self):
        self.id = launchy.hash(self.getAddonName())

    def setAddonId(self, id):
        self.id = id

    def getAddonId(self):
        return self.id

    def setAddonName(self):
        pass

    def getAddonName(self):
        return self.__class__.__name__

    def setAddonIcon(self, filename):
        retVal = True

        if os.path.exists(filename):
            self.icon = filename
        else:
            self.icon = os.path.join(launchy.getIconsPath(), filename)

            if not os.path.exists(self.icon):
                retVal = False
                seif.icon = None
                self.logger(LOG_LEVEL_ERR, "Icon not exist: '%s'." % self.icon)

        return retVal

    def getAddonIcon(self):
        return self.icon

    def resetAddonTrigStrs(self):
        self.triggerStrs = [self.getAddonName(), self.getAddonName().lower()]

    def addAddonTrigStrs(self, string):
        self.triggerStrs.append(string)

    def getAddonTrigStrs(self):
        return self.triggerStrs

    def getCatItem(self, fullPath, shortName):
        return launchy.CatItem(fullPath,
                               shortName,
                               self.getAddonId(),
                               self.getAddonIcon())

    def getResults(self, inputDataList, resultsList):
        pass

    def getCatalog(self, resultsList):
        pass

    def getLabels(self, inputDataList):
        pass

    def getAddonDescription(self):
        """
        TBD
        """
        return "%s" % (self.getAddonName())

    def launchItem(self, inputDataList, catItem):
        return False

    def getFirstInputData(self, inputDataList):
        if len(inputDataList) > 0:
            return inputDataList[0].getText().lower()
        else:
            return None

    def getSecondInputData(self, inputDataList):
        if len(inputDataList) > 1:
            return inputDataList[1].getText().lower()
        else:
            return None

    def getThirdInputData(self, inputDataList):
        if len(inputDataList) > 2:
            return inputDataList[2].getText().lower()
        else:
            return None

    def getLastInputData(self, inputDataList):
        return inputDataList[-1].getText().lower()


class Tasky(AddonBase):

    """http://docs.activestate.com/activepython/2.4/pywin32/win32gui.html"""

    def __init__(self):
        AddonBase.__init__(self)
        self.setAddonIcon("Processor.png")
        self.addAddonTrigStrs('tasky')

    def getResults(self, inputDataList, resultsList):
        query = self.getFirstInputData(inputDataList)

        if query in self.getAddonTrigStrs():

           if len(inputDataList) == 1:
                resultsList.push_front(self.getCatItem(self.getAddonDescription(), self.getAddonName()))
           else:
                windowNameToMatch = self.getSecondInputData(inputDataList)

                self.topLevelWindows = self.getTopLevelWindows()

                for window in self.topLevelWindows:
                    resultsList.append(self.getCatItem(window[1], window[1]))

    def launchItem(self, inputDataList, catItem):
        if catItem.icon == self.getAddonIcon():
            catItem = inputDataList[-1].getTopResult()

            for window in self.topLevelWindows:
                if catItem.shortName == window[1]:
                    self.goToWindow(window[0])
                    return True

    def getTopLevelWindows(self):
        """
        Returns the top level windows in a list of tuples defined (HWND, title)
        """
        windows = []
        win32gui.EnumWindows(self.windowEnumTopLevelCb, windows)
        return windows

    def windowEnumTopLevelCb(self, hwnd, windowsList):
        """
        Window Enum function for getTopLevelWindows
        """
        title = win32gui.GetWindowText(hwnd)
        title = title.decode('gbk').encode('utf-8')
        className = win32gui.GetClassName(hwnd)  
        className = title.decode('gbk').encode('utf-8')

        if win32gui.GetParent(hwnd) == 0 and title != '':
            windowsList.append((hwnd, unicode(title, errors='ignore')))

    def goToWindow(self, hwnd):
        windowPlacement = win32gui.GetWindowPlacement(hwnd)
        showCmd = windowPlacement[1]

        if showCmd == SW_RESTORE:
            win32gui.ShowWindow(hwnd, SW_RESTORE)
        else:
            win32gui.BringWindowToTop(hwnd)

        win32gui.SetForegroundWindow(hwnd)
        win32gui.SetActiveWindow(hwnd)


class Calculator(AddonBase):

    def __init__(self):
        AddonBase.__init__(self)
        self.setAddonIcon("Calculator.png")
        self.addAddonTrigStrs('cal')

    def getResults(self, inputDataList, resultsList):
        query = self.getFirstInputData(inputDataList)

        if query in self.getAddonTrigStrs():

            if len(inputDataList) == 1:
                resultsList.push_front(self.getCatItem(self.getAddonDescription(),
                                                       self.getAddonName()))

            if len(inputDataList) > 1:
                try:
                    # Intercept exceptions from invalid math expressions, this
                    # kind of exceptions should not be treated as plugin level
                    # exceptions.
                    try:
                        ret = eval(self.getLastInputData(inputDataList))
                    except:
                        ret = None

                    if isinstance(ret, int) or isinstance(ret, long):
                        retInFloat = None

                        # hex
                        retInHex = '0x%x' % ret

                        # dec
                        retInDecTmp = str(ret)[::-1]
                        retInDec = ''
                        i = 0
                        for figure in retInDecTmp:
                            i += 1
                            retInDec += figure
                            if i == 3:
                                retInDec += ','
                                i = 0
                        retInDec = retInDec.strip(',')[::-1]

                        # octal
                        retInOct = '0%o' % ret

                        # bin
                        retb = format(ret, '032b')
                        retInBin = ""
                        for i in range(len(retb)):
                            retInBin += retb[i] if (i % 4 or i == 0) else ("," + retb[i])

                        # size in bits
                        retInSizeBit = "%s bit" % ret

                        # size in bytes, keep this at last because it will change the value of 'ret'
                        retInSizeByte = ""

                        size_giga_bytes = ret / (1024 ** 3) if ret / (1024 ** 3) else 0
                        ret -= size_giga_bytes * (1024 ** 3)
                        retInSizeByte += "%s GB " % size_giga_bytes if size_giga_bytes else ""

                        size_mega_bytes = ret / (1024 * 1024) if ret / (1024 * 1024) else 0
                        ret -= size_mega_bytes * (1024 ** 2)
                        retInSizeByte += "%s MB " % size_mega_bytes if size_mega_bytes else ""

                        size_kilo_bytes = ret / (1024) if ret / (1024) else 0
                        ret -= size_mega_bytes * (1024 ** 1)
                        retInSizeByte += "%s KB " % size_kilo_bytes if size_kilo_bytes else ""

                        size_bytes = ret % (1024) if ret % (1024) else 0
                        retInSizeByte += "%s B " % size_bytes if size_bytes else ""

                        if not retInSizeByte:
                            retInSizeByte = "0 B"

                    else:
                        retInFloat = ret
                        retInHex = None
                        retInDec = None
                        retInOct = None
                        retInBin = None
                        retInSizeByte = None
                        retInSizeBit = None
                except:
                    raise
                else:
                    if retInFloat is not None:
                        resultsList.push_front(self.getCatItem("", "Result: %s" % (retInFloat)))

                    if retInHex is not None:
                        resultsList.push_front(self.getCatItem("", "Result: %s" % (retInHex)))

                    if retInOct is not None:
                        resultsList.push_front(self.getCatItem("", "Result: %s" % (retInOct)))

                    if retInDec is not None:
                        resultsList.push_front(self.getCatItem("", "Result: %s" % (retInDec)))

                    if retInBin is not None:
                        resultsList.push_front(self.getCatItem("", "Result: %s" % (retInBin)))

                    if retInSizeByte is not None:
                        resultsList.push_front(self.getCatItem("", "Result: %s" % (retInSizeByte)))

                    if retInSizeBit is not None:
                        resultsList.push_front(self.getCatItem("", "Result: %s" % (retInSizeBit)))


class WebSearch(AddonBase):

    searchEngine = {
        "fan": {
            "url": "http://fanyi.baidu.com/?aldtype=85#en/zh/%s",
            "name": "Baidu Translation"
        },
        "gg": {
            "url": "https://www.google.fi/search?q=%s&oq=hello&sourceid=chrome&ie=UTF-8",
            "name": "Google"
        },
        "cj": {
            "url": "https://translate.google.fi/?um=1&ie=UTF-8&hl=en&client=tw-ob#zh-CN/ja/%s",
            "name": "Google Translation - Chinese to Japanese"
        },
        "jc": {
            "url": "https://translate.google.fi/?um=1&ie=UTF-8&hl=en&client=tw-ob#view=home&op=translate&sl=ja&tl=zh-CN&text=%s",
            "name": "Google Translation - Chinese to Japanese"
        },
        "ii": {
            "url": "http://www.bing.com/search?q=%s",
            "name": "Bing"
        },
        "bb": {
            "url": "https://www.baidu.com/s?wd=%s",
            "name": "Baidu"
        },
        "gmap": {
            "url": "https://www.google.com/maps/search/?api=1&query=%s",
            "name": "Google Maps"
        },
        "bmap": {
            "url": "http://api.map.baidu.com/geocoder?address=%s&output=html&src=Chrome",
            "name": "Baidu Maps"
        },
        "tao": {
            "url": "http://s.taobao.com/search?q=%s",
            "name": "Taobao"
        },
        "jd": {
            "url": "http://search.jd.com/Search?keyword=%s&enc=utf-8",
            "name": "Jingdong"
        },
        "sn": {
            "url": "https://search.suning.com/%s/",
            "name": "Suning"
        },
        "mm": {
            "url": "http://www.boohee.com/food/search?keyword=%s",
            "name": "A Food Database"
        },
        "pr": {
            "url": "https://pronto.inside.nsn.com/pronto/problemReportSearch.html?freeTextdropDownID=prId&searchTopText=%s",
            "name": "Pronto"
        },
        "cpp": {
            "url": "http://www.cplusplus.com/search.do?q=%s",
            "name": "C++"
        },
        "dd": {
            "url": "http://www.dictionary.com/browse/%s",
            "name": "Dictionary"
        },
        "so": {
            "url": "http://stackoverflow.com/search?q=%s",
            "name": "StackOverflow"
        },
        "ieee": {
            "url": "http://ieeexplore.ieee.org/search/searchresult.jsp?newsearch=true&queryText=%s",
            "name": "IEEE"
        },
        "man": {
            "url": "http://www.freebsd.org/cgi/man.cgi?query=%s",
            "name": "Linux Man Page"
        },
        "cygwin": {
            "url": "https://cygwin.com/cgi-bin2/package-grep.cgi?grep=%s&arch=x86",
            "name": "cygwin package search"
        },
        "j3": {
            "url": "https://jira3.int.net.nokia.com/secure/QuickSearch.jspa?searchString=%s",
            "name": "Jira3 Search"
        },
        "jj": {
            "url": "https://jiradc.int.net.nokia.com/secure/QuickSearch.jspa?searchString=%s",
            "name": "JiraDC Search"
        },
        "con": {
            "url": "https://confluence.int.net.nokia.com/dosearchsite.action?cql=siteSearch+~+'%s'",
            "name": "Confluence"
        },
        "ww": {
            "url": "https://wft.int.net.nokia.com/ext/build_content/%s",
            "name": "WFT Build Content Search"
        },
        "sp": {
            "url": "https://nokia.sharepoint.com/_layouts/15/sharepoint.aspx?q=%s&v=search",
            "name": "SharePoint Search"
        },
        "bh": {
            "url": "https://www.zhihu.com/search?type=content&q=%s",
            "name": "Bihu Search"
        },
        "xq": {
            "url": "https://xueqiu.com/k?q=%s",
            "name": "XueQiu Financial Search"
        },
    }

    def __init__(self):
        AddonBase.__init__(self)
        self.setAddonIcon("WebSearch.png")

    @classmethod
    def encodeQuery(cls, query):
        return urllib.quote(query.encode("utf8"))

    @classmethod
    def getUrl(cls, key, query):
        return eval('"%s" %% "%s"' % (WebSearch.searchEngine.get(key).get('url'), WebSearch.encodeQuery(query)))

    def getResults(self, inputDataList, resultsList):
        query = self.getFirstInputData(inputDataList)

        if query in self.searchEngine.keys():
            resultsList.push_front(self.getCatItem("%s: %s search" % (self.getAddonName(), self.searchEngine.get(query).get("name")),
                                                   query))

    def launchItem(self, inputDataList, catItem):
        if catItem.icon == self.getAddonIcon():
            key = self.getFirstInputData(inputDataList)
            query = self.getLastInputData(inputDataList)

            subprocess.Popen('start chrome "%s"' % self.getUrl(key, query), shell=True)
            return True


class RunCommands(AddonBase):

    PROG_OS = 1        # call by OS, usually call an external program
    PROG_THRUSTER = 2  # call by Thruster, usually call a method

    CmdAlias = {"putty": {"prog": PROG_OS, "cmd": "putty.exe"},
                "sync@Company": {"prog": PROG_THRUSTER, "cmd": "self.syncAtCompany()"},
                "sync@Home": {"prog": PROG_THRUSTER, "cmd": "self.syncAtHome()"}}

    def __init__(self):
        AddonBase.__init__(self)
        self.setAddonIcon("RunCommands.png")
        self.addAddonTrigStrs('run')

        # Get putty session from register, the session entry looks like this:
        # rsa2@22:hzling42.china.nsn-net.net    REG_SZ    0x23,0xc1ca944dc...
        proc = subprocess.Popen("reg query HKEY_CURRENT_USER\Software\SimonTatham\PuTTY\SshHostKeys /s", stdout=subprocess.PIPE)

        for line in proc.stdout.readlines():
            lineSplited = line.split()

            if len(lineSplited) >= 3:
                sessionName = lineSplited[0].split(':')[1]
                RunCommands.CmdAlias.update({sessionName: {"prog": RunCommands.PROG_OS,
                                                           "cmd": 'putty -load "%s"' % sessionName}})

    def syncFiles(self, syncTable):
        '''
        @syncTable [(local, remote), ...]: file syncing table.
        '''
        for syncEntry in syncTable:

            src, dst = syncEntry

            if (not os.path.exists(src)) and (not os.path.exists(dst)):
                self.logger(self.LOG_LEVEL_ERR, "both src and dst files not exist:\n  %s  %s." % (src, dst))
            elif os.path.exists(src) and not os.path.exists(dst):
                self.copyFile(src, dst)
            elif os.path.exists(dst) and not os.path.exists(src):
                self.copyFile(dst, src)
            elif os.path.getmtime(dst) > os.path.getmtime(src):
                self.copyFile(dst, src)
            elif os.path.getmtime(dst) < os.path.getmtime(src):
                self.copyFile(src, dst)

    def copyFile(self, src, dst):
        """
        copy file and dir (dir is a kind of file).
        """
        if os.path.isdir(dst):
            os.system('rm -rf "%s"' % (dst))

        os.system('cp -rfuv --strip-trailing-slashes "%s" "%s"' % (src, dst))

    def syncAtCompany(self):

        syncTable = [
            (
                "c:/Program Files (x86)/vim/_vimrc",
                "c:/Home/j5shi/cloud/Private/Vim/_vimrc"
            ),
            (
                "c:/cygwin/home/j5shi/.bash_profile",
                "c:/Home/j5shi/cloud/Private/fs/C/cygwin/home/j5shi/.bash_profile"
            ),
        ]

        self.syncFiles(syncTable)

    def syncAtHome(self):

        syncTable = [
            (
                "c:/Program Files (x86)/vim/_vimrc",
                "d:/cloud/Private/Vim/_vimrc"
            ),
            (
                "c:/cygwin/home/j5shi/.bash_profile",
                "d:/cloud/Private/fs/C/cygwin/home/j5shi/.bash_profile"
            ),
        ]

        self.syncFiles(syncTable)

    def getResults(self, inputDataList, resultsList):
        query = self.getFirstInputData(inputDataList)

        if query in self.getAddonTrigStrs():
            if len(inputDataList) == 1:
                resultsList.push_front(self.getCatItem("%s: Run commands" % self.getAddonName(),
                                                       'Run'))

            if len(inputDataList) > 1:
                for alias in self.CmdAlias.keys():
                    resultsList.push_front(self.getCatItem("%s: Run commands" % (self.getAddonName()),
                                                           alias))

    def launchItem(self, inputDataList, catItem):
        if catItem.icon == self.getAddonIcon():
            alias = self.CmdAlias.get(inputDataList[-1].getTopResult().shortName, {})

            if alias.get("prog", None) == self.PROG_OS:
                cmd = "%s" % (alias.get("cmd"))
                subprocess.Popen(cmd, shell=True)
            elif alias.get("prog", None) == self.PROG_THRUSTER:
                eval("%s" % alias.get("cmd"))
            else:
                pass

            return True


class BrowserBookmarks(AddonBase):

    def __init__(self):
        AddonBase.__init__(self)
        self.setAddonIcon("Chrome.png")

    def launchItem(self, inputDataList, catItem):
        if catItem.icon == self.getAddonIcon():
            subprocess.Popen('start chrome "%s"' % catItem.fullPath, shell=True)
            return True

    def getBookMarks(self, bookmarks, bookmarkBarObj):
        for obj in bookmarkBarObj:
            self.logger(self.LOG_LEVEL_DBG, "%s" % (obj.get('name')))

            if obj.get("type", '') is "folder":
                bookmarks = self.getBookMarks(bookmarks, obj.get("children", []))

            elif obj.get("type", '') is "url":
                bookmarks.update({obj.get("name", ''): obj.get("url", '')})

        return bookmarks

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
        bookmarks = {}
        bookmarkFile = os.path.join(os.environ["localappdata"], "Google/Chrome/User Data/Default/Bookmarks")
        bookmarkManager = eval(open(bookmarkFile, 'r').read())
        bookmarkBar = bookmarkManager.get("roots", None).get("bookmark_bar", None).get("children", [])
        bookmarks = self.getBookMarks(bookmarks, bookmarkBar)

        for key in bookmarks.keys():
            resultsList.append(self.getCatItem(bookmarks.get(key), key))


class Shortcuts(AddonBase):

    def __init__(self):
        AddonBase.__init__(self)
        self.setAddonIcon("DefaultHandler.png")

    def cb_S_CR(self, inputDataList, catItem):
        """
        open in totalcmd right panel.
        """
        subprocess.Popen('start TOTALCMD64.exe /O /A /T /R="%s"' % catItem.fullPath, shell=True)

    def cb_C_CR(self, inputDataList, catItem):
        """
        open in totalcmd left panel.
        """
        subprocess.Popen('start TOTALCMD64.exe /O /A /T /L="%s"' % catItem.fullPath, shell=True)

    def cb_M_CR(self, inputDataList, catItem):
        """
        edit in gvim.exe
        """
        subprocess.Popen('start gvim.exe --remote-tab-silent "%s"' % catItem.fullPath, shell=True)

    def cb_C_S_CR(self, inputDataList, catItem):
        """
        copy selected item's full path to clipboard
        """
        subprocess.Popen('echo %s | clip' % catItem.fullPath.replace('\\', '/'), shell=True)

    def cb_M_S_CR(self, inputDataList, catItem):
        """
        open the selected item with gvim.exe
        """
        subprocess.Popen('start gvim.exe --remote-tab-silent "%s"' % 
                os.path.join(launchy.getScriptsPath(), "Thruster.py"),
                shell=True)


    def launchItem(self, inputDataList, catItem):
        if len(inputDataList) == 1:
            modifier = QtGui.QApplication.keyboardModifiers()

            if modifier == QtCore.Qt.ShiftModifier:
                self.cb_S_CR(inputDataList, catItem)

            elif modifier == QtCore.Qt.ControlModifier:
                self.cb_C_CR(inputDataList, catItem)

            elif modifier == QtCore.Qt.AltModifier:
                self.cb_M_CR(inputDataList, catItem)

            elif modifier == (QtCore.Qt.ControlModifier | QtCore.Qt.ShiftModifier):
                self.cb_C_S_CR(inputDataList, catItem)

            elif modifier == (QtCore.Qt.AltModifier | QtCore.Qt.ShiftModifier):
                self.cb_M_S_CR(inputDataList, catItem)

            else:
                return False

            return True


class DefaultHandler(AddonBase):

    pattern_pronto_pattern0 = re.compile("^[pP][rR]\d+\s*$")
    pattern_pronto_pattern1 = re.compile("^[nN][aA]\d+\s*$")
    pattern_pronto_pattern2 = re.compile("^[cC][aA][sS]-\d+.*$")
    pattern_jira3 = re.compile("(^[pP][sS][fF][eE][aA][tT][uU][rR][eE]-\d+\s*$)")
    pattern_jiradc_pattern0 = re.compile("(^[fF][cC][aA]_[pP][sS]_[uU][pP]-\d+\s*$)")
    pattern_google = re.compile("(^\/{1}[^/]*$)")
    pattern_baidu = re.compile("^\/{2}([^/]*$)|(^\s{2}\S.*$)")
    pattern_bing = re.compile("^\/{3}([^/]*$)|(^\s{3}\S.*$)")
    pattern_taobao = re.compile("^\?([^?]*$)")
    pattern_url = re.compile("(^http.*$)|(^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}.*$)|(^www.*$)|(.*\.com.*$)|(.*\.cn.*$)")
    pattern_stocks = re.compile("(^[sS]?[HhZz]?[\d]{6}\s*$)|(^\s{1}\S.*$)")

    fullpath_jiradc = "Search in JiraDC"
    fullpath_jira3 = "Search in Jira3"
    fullpath_pronto = "Search in Pronto" 
    fullpath_google = "Search in Google"
    fullpath_baidu = "Search in Baidu"
    fullpath_bing = "Search in Bing"
    fullpath_baidumap = "Search in Baidu Map"
    fullpath_taobao = "Search in Taobao"
    fullpath_xueqiu = "Search in XueQiu Finance"

    def __init__(self):
        AddonBase.__init__(self)
        self.setAddonIcon("DefaultHandler.png")

    def getResults(self, inputDataList, resultsList):
        if len(inputDataList) == 1:
            resultsList.push_front(self.getCatItem("%s: at your service, sir!" % self.getAddonName(), ""))
            resultsList.push_front(self.getCatItem(self.fullpath_jiradc, ""))
            resultsList.push_front(self.getCatItem(self.fullpath_jira3, ""))
            resultsList.push_front(self.getCatItem(self.fullpath_pronto, ""))
            resultsList.push_front(self.getCatItem(self.fullpath_google, ""))
            resultsList.push_front(self.getCatItem(self.fullpath_baidu, ""))
            resultsList.push_front(self.getCatItem(self.fullpath_baidumap, ""))
            resultsList.push_front(self.getCatItem(self.fullpath_bing, ""))
            resultsList.push_front(self.getCatItem(self.fullpath_taobao, ""))
            resultsList.push_front(self.getCatItem(self.fullpath_xueqiu, ""))

    def launchItem(self, inputDataList, catItem):
        self.logger(self.LOG_LEVEL_DBG, "Default handler query: %s" % self.getFirstInputData(inputDataList))

        query = self.getFirstInputData(inputDataList)

        if catItem.fullPath == self.fullpath_jiradc:
            url = WebSearch.getUrl('jj', query.strip())
            subprocess.Popen('start chrome "%s"' % url, shell=True)

        elif catItem.fullPath == self.fullpath_jira3:
            url = WebSearch.getUrl('j3', query.strip())
            subprocess.Popen('start chrome "%s"' % url, shell=True)

        elif catItem.fullPath == self.fullpath_pronto:
            url = WebSearch.getUrl('pr', query.strip())
            subprocess.Popen('start chrome "%s"' % url, shell=True)

        elif catItem.fullPath == self.fullpath_google:
            url = WebSearch.getUrl('gg', query.strip())
            subprocess.Popen('start chrome "%s"' % url, shell=True)

        elif catItem.fullPath == self.fullpath_baidu:
            url = WebSearch.getUrl('bb', query.strip())
            subprocess.Popen('start chrome "%s"' % url, shell=True)

        elif catItem.fullPath == self.fullpath_baidu:
            url = WebSearch.getUrl('bmap', query.strip())
            subprocess.Popen('start chrome "%s"' % url, shell=True)

        elif catItem.fullPath == self.fullpath_bing:
            url = WebSearch.getUrl('ii', query.strip())
            subprocess.Popen('start chrome "%s"' % url, shell=True)

        elif catItem.fullPath == self.fullpath_taobao:
            url = WebSearch.getUrl('tao', query.strip())
            subprocess.Popen('start chrome "%s"' % url, shell=True)

        elif catItem.fullPath == self.fullpath_xueqiu:
            url = WebSearch.getUrl('xq', query.strip())
            subprocess.Popen('start chrome "%s"' % url, shell=True)

        elif catItem.icon == self.getAddonIcon():
            # if nothing in query, use what get from clipboard as query
            if not query.strip():
                myClipBoard = QtGui.QApplication.clipboard()
                query = str(myClipBoard.text("plain", QtGui.QClipboard.Clipboard)).strip()
                #  self.logger(self.LOG_LEVEL_INF, "query: %s" % query)

            if self.pattern_pronto_pattern0.match(query) or \
               self.pattern_pronto_pattern1.match(query) or \
               self.pattern_pronto_pattern2.match(query):
                url = WebSearch.getUrl('pr', query.strip())

            elif self.pattern_jira3.match(query):
                url = WebSearch.getUrl('j3', query.strip())

            elif self.pattern_jiradc_pattern0.match(query):
                url = WebSearch.getUrl('jj', query.strip())

            elif self.pattern_google.match(query):
                url = WebSearch.getUrl('gg', query[1:].strip())

            elif self.pattern_baidu.match(query):
                url = WebSearch.getUrl('bb', query[2:])

            elif self.pattern_bing.match(query):
                url = WebSearch.getUrl('ii', query[3:])

            elif self.pattern_taobao.match(query):
                url = WebSearch.getUrl('tao', query[1:])

            elif self.pattern_stocks.match(query):
                url = WebSearch.getUrl('xq', query)

            elif self.pattern_url.match(query):
                url = query.strip()

            else:
                #  url = query
                url = WebSearch.getUrl('gg', query.strip())   # use google as a fallback option

            subprocess.Popen('start chrome "%s"' % url, shell=True)
        else:
            launchy.runProgram('"%s"' % catItem.fullPath, "")

        return True


class Thruster(launchy.Plugin, Logger):

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

        self.addons = []
        self.name = "Thruster"
        self.id = launchy.hash(self.name)
        self.icon = os.path.join(launchy.getIconsPath(), "%s.png" % self.name)

    def init(self):
        """
        This message informs the plugin that it is being loaded.

        This is a good time to do any initialization work.
        """
        self.logger(self.LOG_LEVEL_INF, "Python: %s" % sys.version)
        self.logger(self.LOG_LEVEL_INF, "Python interpreter: %s" % sys.executable)
        self.logger(self.LOG_LEVEL_INF, "==============================")
        self.logger(self.LOG_LEVEL_INF, "instance created: %s" % self)
        self.logger(self.LOG_LEVEL_INF, "hash: %s" % self.getID())
        self.logger(self.LOG_LEVEL_INF, "name: %s" % self.getName())
        self.logger(self.LOG_LEVEL_INF, "icon: %s" % self.getIcon())
        self.logger(self.LOG_LEVEL_INF, "loading addons:")
        self.addons = []
        self.registerAddon(Tasky)
        self.registerAddon(BrowserBookmarks)
        self.registerAddon(WebSearch)
        self.registerAddon(RunCommands)
        self.registerAddon(Calculator)
        self.registerAddon(Shortcuts)
        self.registerAddon(DefaultHandler)
        self.logger(self.LOG_LEVEL_INF, "finished loading addons.")
        self.logger(self.LOG_LEVEL_INF, "==============================")
        self.initAddons()

    def registerAddon(self, addon):
        a = addon()

        if type(a).__name__ != "DefaultHandler":
            self.addons.insert(0, a)
        else:
            # the DefaultHandler should always be the
            # last addon to process queries
            self.addons.append(a)

        self.logger(self.LOG_LEVEL_INF, "  - %s loaded" % type(a).__name__)

    def initAddons(self):
        """
        Every catItem belongs to a plugin, this is indicated by the id. By
        setting the right id, the catItem can be handled by the correct plugin.
        """
        for addon in self.addons:
            addon.setAddonId(self.id)

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
        try:
            for addon in self.addons:
                if addon.launchItem(inputDataList, catItem):
                    self.logger(self.LOG_LEVEL_DBG,
                                "Addon %s executed query: %s." % (addon.getAddonName(), addon.getLastInputData(inputDataList)))
                    break
        except:
            #  os.system('start "" /B gvim.exe --remote-tab-silent "%s"' %
                      #  os.path.dirname(os.path.realpath(sys.argv[0])), 'stderr.txt')
            raise

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

launchy.registerPlugin(Thruster)
