# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'pydiry_new_entry.ui'
#
# Created: Fri Sep 05 01:36:41 2008
#      by: PyQt4 UI code generator 4.4.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_NewDirectoryEntryDialog(object):
    def setupUi(self, NewDirectoryEntryDialog):
        NewDirectoryEntryDialog.setObjectName("NewDirectoryEntryDialog")
        NewDirectoryEntryDialog.resize(408,118)
        NewDirectoryEntryDialog.setSizeGripEnabled(True)
        NewDirectoryEntryDialog.setModal(True)
        self.verticalLayout = QtGui.QVBoxLayout(NewDirectoryEntryDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtGui.QLabel(NewDirectoryEntryDialog)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label,0,0,1,1)
        self.directoryLineEdit = QtGui.QLineEdit(NewDirectoryEntryDialog)
        self.directoryLineEdit.setObjectName("directoryLineEdit")
        self.gridLayout.addWidget(self.directoryLineEdit,0,1,1,1)
        self.selectDirectoryButton = QtGui.QToolButton(NewDirectoryEntryDialog)
        self.selectDirectoryButton.setPopupMode(QtGui.QToolButton.DelayedPopup)
        self.selectDirectoryButton.setToolButtonStyle(QtCore.Qt.ToolButtonIconOnly)
        self.selectDirectoryButton.setObjectName("selectDirectoryButton")
        self.gridLayout.addWidget(self.selectDirectoryButton,0,2,1,1)
        self.label_2 = QtGui.QLabel(NewDirectoryEntryDialog)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2,1,0,1,1)
        self.nameLineEdit = QtGui.QLineEdit(NewDirectoryEntryDialog)
        self.nameLineEdit.setObjectName("nameLineEdit")
        self.gridLayout.addWidget(self.nameLineEdit,1,1,1,1)
        self.verticalLayout.addLayout(self.gridLayout)
        self.label_3 = QtGui.QLabel(NewDirectoryEntryDialog)
        self.label_3.setObjectName("label_3")
        self.verticalLayout.addWidget(self.label_3)
        self.buttonBox = QtGui.QDialogButtonBox(NewDirectoryEntryDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setCenterButtons(False)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(NewDirectoryEntryDialog)
        QtCore.QObject.connect(self.buttonBox,QtCore.SIGNAL("accepted()"),NewDirectoryEntryDialog.accept)
        QtCore.QObject.connect(self.buttonBox,QtCore.SIGNAL("rejected()"),NewDirectoryEntryDialog.reject)
        QtCore.QObject.connect(self.selectDirectoryButton,QtCore.SIGNAL("clicked()"),NewDirectoryEntryDialog.selectDirectory_clicked)
        QtCore.QMetaObject.connectSlotsByName(NewDirectoryEntryDialog)

    def retranslateUi(self, NewDirectoryEntryDialog):
        NewDirectoryEntryDialog.setWindowTitle(QtGui.QApplication.translate("NewDirectoryEntryDialog", "New directory entry", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("NewDirectoryEntryDialog", "Directory:", None, QtGui.QApplication.UnicodeUTF8))
        self.selectDirectoryButton.setText(QtGui.QApplication.translate("NewDirectoryEntryDialog", "...", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("NewDirectoryEntryDialog", "Name:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("NewDirectoryEntryDialog", "<b>Tip</b>: You can use envrionement variables, e.g. %USERPROFILE%\\My Documents", None, QtGui.QApplication.UnicodeUTF8))

