import launchy

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
        pass    
        
    def getResults(self, inputDataList, resultsList):
        # Take the text from the first input item and add a new
        # Catalog item with our plugin id
        text = inputDataList[0].getText()   ### 4
        resultsList.push_back( launchy.CatItem(text,
            "Totalcmd: " + text,
            self.getID(), self.getIcon()) )   ### 5
        
    def getCatalog(self, resultsList):
        pass

    def launchItem(self, inputDataList, catItemOrig):
        # The user chose our catalog item, print it      
        catItem = inputDataList[-1].getTopResult()  ### 6
        print "I was asked to launch: ", catItem.fullPath   ### 7
        
launchy.registerPlugin(Totalcmd)   ### 8