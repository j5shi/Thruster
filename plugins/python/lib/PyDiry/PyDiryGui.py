import launchy
from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import QVariant

from ui_pydiry import *
from ui_pydiry_new_entry import *

class PyDiryUi(QtGui.QWidget):
	def __init__(self, parent=None):
		QtGui.QWidget.__init__(self, parent)
		self.ui = Ui_PyDiryWidget()
		self.ui.setupUi(self)
		
		settings = launchy.settings
		table = self.ui.entriesTable
		
		size = settings.beginReadArray("PyDiry/dirs")
		table.setRowCount(size)
		
		for i in range(0, size):
			settings.setArrayIndex(i);
			nameItem = QtGui.QTableWidgetItem( settings.value("name").toString() )
			pathItem = QtGui.QTableWidgetItem( settings.value("path").toString() )
			table.setItem(i, 0, nameItem)
			table.setItem(i, 1, pathItem)
		
		settings.endArray()

	def addEntry_clicked(self):
		newEntryDialog = NewDirectoryEntryDialog(self)
		newEntryDialog.exec_()
		if not newEntryDialog.isValid:
			return
		
		table = self.ui.entriesTable
		lastItemCount = table.rowCount()
		table.insertRow(table.rowCount())
		table.setCurrentCell(lastItemCount, 0)
		
		nameItem = QtGui.QTableWidgetItem( newEntryDialog.name )
		pathItem = QtGui.QTableWidgetItem( newEntryDialog.directory )
		
		table.setItem(lastItemCount, 0, nameItem)
		table.setItem(lastItemCount, 1, pathItem)
	
	def removeEntry_clicked(self):
		currentRow = self.ui.entriesTable.currentRow()
		if currentRow != -1:
			self.ui.entriesTable.removeRow(currentRow)
			
	def writeSettings(self):
		settings = launchy.settings
		table = self.ui.entriesTable
		
		# Remove all empty rows
		itemsToRemove = []
		for i in range(0, table.rowCount()):
			nameItem = table.item(i,0)
			pathItem = table.item(i,1)
			if nameItem == None or pathItem == None:
				itemsToRemove.append(i)
			elif nameItem.text() == "" or pathItem == "":
				itemsToRemove.append(i)
		
		for item in itemsToRemove:
			table.removeRow(i)
		
		# Add all rows to the dirs array
		settings.remove("PyDiry/dirs")
		settings.beginWriteArray("PyDiry/dirs")
		for i in range(0, table.rowCount()):
			settings.setArrayIndex(i)
			settings.setValue("name", QVariant(table.item(i,0).text()))
			settings.setValue("path", QVariant(table.item(i,1).text()))
		settings.endArray()

class NewDirectoryEntryDialog(QtGui.QDialog):
	def __init__(self, parent=None):
		QtGui.QDialog.__init__(self, parent)
		self.ui = Ui_NewDirectoryEntryDialog()
		self.ui.setupUi(self)
		self.isValid = False
		
	def accept(self):
		self.directory = self.ui.directoryLineEdit.text()
		self.name = self.ui.nameLineEdit.text()
		
		if self.directory.isEmpty():
			self.reject()
		elif self.name.isEmpty():
			QtGui.QMessageBox.information(self,
				"Name is empty", "Please set a name for the directory")
			return
		else:
			self.isValid = True
			QtGui.QDialog.accept(self)
		
	def reject(self):
		QtGui.QDialog.reject(self)
	
	def selectDirectory_clicked(self):
		dir = QtGui.QFileDialog.getExistingDirectory( None, QtCore.QString(),
			self.ui.directoryLineEdit.text())
		# this, "Select a directory",
		# lastDir,
		# QtGui.QFileDialog.ShowDirsOnly );
		
		nativeDir = QtCore.QDir.toNativeSeparators(dir)
		self.ui.directoryLineEdit.setText(nativeDir)
