# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'pywebindex.ui'
#
# Created: Fri Sep 05 15:18:17 2008
#      by: PyQt4 UI code generator 4.4.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_PyWebIndex(object):
    def setupUi(self, PyWebIndex):
        PyWebIndex.setObjectName("PyWebIndex")
        PyWebIndex.resize(382,424)
        self.verticalLayout = QtGui.QVBoxLayout(PyWebIndex)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem = QtGui.QSpacerItem(40,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.label = QtGui.QLabel(PyWebIndex)
        self.label.setObjectName("label")
        self.horizontalLayout_2.addWidget(self.label)
        spacerItem1 = QtGui.QSpacerItem(40,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.entriesTable = QtGui.QTableWidget(PyWebIndex)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.entriesTable.sizePolicy().hasHeightForWidth())
        self.entriesTable.setSizePolicy(sizePolicy)
        self.entriesTable.setObjectName("entriesTable")
        self.verticalLayout.addWidget(self.entriesTable)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem2 = QtGui.QSpacerItem(40,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem2)
        self.addEntryButton = QtGui.QPushButton(PyWebIndex)
        self.addEntryButton.setObjectName("addEntryButton")
        self.horizontalLayout.addWidget(self.addEntryButton)
        spacerItem3 = QtGui.QSpacerItem(58,17,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem3)
        self.removeEntryButton = QtGui.QPushButton(PyWebIndex)
        self.removeEntryButton.setObjectName("removeEntryButton")
        self.horizontalLayout.addWidget(self.removeEntryButton)
        spacerItem4 = QtGui.QSpacerItem(40,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem4)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.forceDatabaseRebuildBox = QtGui.QCheckBox(PyWebIndex)
        self.forceDatabaseRebuildBox.setObjectName("forceDatabaseRebuildBox")
        self.verticalLayout.addWidget(self.forceDatabaseRebuildBox)

        self.retranslateUi(PyWebIndex)
        QtCore.QObject.connect(self.addEntryButton,QtCore.SIGNAL("clicked()"),PyWebIndex.addEntry_clicked)
        QtCore.QObject.connect(self.removeEntryButton,QtCore.SIGNAL("clicked()"),PyWebIndex.removeEntry_clicked)
        QtCore.QMetaObject.connectSlotsByName(PyWebIndex)

    def retranslateUi(self, PyWebIndex):
        PyWebIndex.setWindowTitle(QtGui.QApplication.translate("PyWebIndex", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("PyWebIndex", "PyWebIndex - Launch links from index pages", None, QtGui.QApplication.UnicodeUTF8))
        self.entriesTable.clear()
        self.entriesTable.setColumnCount(2)
        self.entriesTable.setRowCount(0)
        headerItem = QtGui.QTableWidgetItem()
        headerItem.setText(QtGui.QApplication.translate("PyWebIndex", "Name", None, QtGui.QApplication.UnicodeUTF8))
        self.entriesTable.setHorizontalHeaderItem(0,headerItem)
        headerItem1 = QtGui.QTableWidgetItem()
        headerItem1.setText(QtGui.QApplication.translate("PyWebIndex", "Index URL", None, QtGui.QApplication.UnicodeUTF8))
        self.entriesTable.setHorizontalHeaderItem(1,headerItem1)
        self.addEntryButton.setToolTip(QtGui.QApplication.translate("PyWebIndex", "Add a new entry", None, QtGui.QApplication.UnicodeUTF8))
        self.addEntryButton.setText(QtGui.QApplication.translate("PyWebIndex", "+", None, QtGui.QApplication.UnicodeUTF8))
        self.removeEntryButton.setToolTip(QtGui.QApplication.translate("PyWebIndex", "Remove the selected entry", None, QtGui.QApplication.UnicodeUTF8))
        self.removeEntryButton.setText(QtGui.QApplication.translate("PyWebIndex", "-", None, QtGui.QApplication.UnicodeUTF8))
        self.forceDatabaseRebuildBox.setToolTip(QtGui.QApplication.translate("PyWebIndex", "Rebuild database even if settings were not changed", None, QtGui.QApplication.UnicodeUTF8))
        self.forceDatabaseRebuildBox.setText(QtGui.QApplication.translate("PyWebIndex", "Force database rebuild", None, QtGui.QApplication.UnicodeUTF8))

