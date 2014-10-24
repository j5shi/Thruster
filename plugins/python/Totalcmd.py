#-*- coding: utf-8 -*
"""
@author: Jia Shi
@email: j5shi@live.com
@data: 2014-10-23 23:10:25
@version: 0.1
@license: GNU GPL v2
"""
import launchy
import subprocess

class Totalcmd(launchy.Plugin):
    def __init__(self):
        launchy.Plugin.__init__(self)
        self.name = "Totalcmd"
        self.hash = launchy.hash(self.name)
        self.icon = os.path.join(launchy.getIconsPath(), "Totalcmd.png")
    
    def init(self):
        pass
        
    def getID(self):
        return self.hash

    def getName(self):
        return self.name

    def getIcon(self):
         return self.icon
        
    def getLabels(self, inputDataList):
        if len(inputDataList) > -1:
            return
        else:
            subprocess.Popen('start chrome "www.sina.com"', shell=True)
        
    def getResults(self, inputDataList, resultsList):
        resultsList.push_back(launchy.CatItem(
            "Open in Totalcmd",
            "Open in Totalcmd",
            self.getID(), 
            self.getIcon()))
        
    def getCatalog(self, resultsList):
        pass
        
    def launchItem(self, inputDataList, catItemOrig):
        pass
        
launchy.registerPlugin(Totalcmd)