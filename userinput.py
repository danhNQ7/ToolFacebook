# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'dialog_input.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class User_Input(object):
    def setupUi(self, Dialog):
        self.Dialog =Dialog
        self.Dialog.setObjectName("Dialog")
        self.Dialog.resize(385, 565)
        self.txtUID = QtWidgets.QTextEdit(Dialog)
        self.txtUID.setGeometry(QtCore.QRect(20, 40, 351, 451))
        self.txtUID.setObjectName("txtUID")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(150, 20, 67, 17))
        self.label.setObjectName("label")
        self.pushButton = QtWidgets.QPushButton(Dialog)
        self.pushButton.setGeometry(QtCore.QRect(140, 510, 89, 25))
        self.pushButton.setObjectName("pushButton")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
        self.text=''
        self.pushButton.clicked.connect(self.click)
    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label.setText(_translate("Dialog", "Nhập ID"))
        self.pushButton.setText(_translate("Dialog", "Thực hiện"))
    def click(self):
        
        self.text= self.txtUID.toPlainText()
        self.Dialog.close()

