# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\main (3).ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1280, 720)
        font = QtGui.QFont()
        font.setFamily("Cascadia Code")
        font.setPointSize(14)
        MainWindow.setFont(font)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.input_edit = QtWidgets.QLineEdit(self.centralwidget)
        self.input_edit.setGeometry(QtCore.QRect(180, 10, 441, 41))
        self.input_edit.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.input_edit.setObjectName("input_edit")
        self.input_label = QtWidgets.QLabel(self.centralwidget)
        self.input_label.setGeometry(QtCore.QRect(10, 10, 161, 41))
        self.input_label.setObjectName("input_label")
        self.reset_button = QtWidgets.QPushButton(self.centralwidget)
        self.reset_button.setGeometry(QtCore.QRect(770, 10, 131, 41))
        self.reset_button.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.reset_button.setObjectName("reset_button")
        self.search_button = QtWidgets.QPushButton(self.centralwidget)
        self.search_button.setGeometry(QtCore.QRect(630, 10, 131, 41))
        self.search_button.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.search_button.setObjectName("search_button")
        self.view_button = QtWidgets.QComboBox(self.centralwidget)
        self.view_button.setGeometry(QtCore.QRect(910, 10, 121, 41))
        font = QtGui.QFont()
        font.setFamily("Cascadia Code")
        font.setPointSize(16)
        self.view_button.setFont(font)
        self.view_button.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.view_button.setStyleSheet("QComboBox {\n"
"    border-radius: 20;\n"
"    background-color: rgb(149, 173, 182);\n"
"    color: white;\n"
"}\n"
"QComboBox::drop-down {\n"
"    width: 0px;\n"
"    height: 0px;\n"
"    border: 0px;\n"
"}\n"
"QComboBox QAbstractItemView {\n"
"  color: white;    \n"
"  background-color: rgb(149, 173, 182);\n"
"  selection-background-color: rgb(54, 73, 78);\n"
"  border: 3px solid white;\n"
"}")
        self.view_button.setObjectName("view_button")
        self.view_button.addItem("")
        self.view_button.addItem("")
        self.view_button.addItem("")
        self.postId_box = QtWidgets.QCheckBox(self.centralwidget)
        self.postId_box.setGeometry(QtCore.QRect(1050, 10, 131, 41))
        self.postId_box.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.postId_box.setObjectName("postId_box")
        self.address_label = QtWidgets.QLabel(self.centralwidget)
        self.address_label.setGeometry(QtCore.QRect(10, 60, 1251, 81))
        self.address_label.setText("")
        self.address_label.setAlignment(QtCore.Qt.AlignCenter)
        self.address_label.setObjectName("address_label")
        self.map_image = QtWidgets.QLabel(self.centralwidget)
        self.map_image.setGeometry(QtCore.QRect(10, 160, 811, 541))
        self.map_image.setText("")
        self.map_image.setScaledContents(True)
        self.map_image.setAlignment(QtCore.Qt.AlignCenter)
        self.map_image.setObjectName("map_image")
        self.status_textedit = QtWidgets.QTextEdit(self.centralwidget)
        self.status_textedit.setGeometry(QtCore.QRect(850, 160, 421, 551))
        self.status_textedit.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)
        self.status_textedit.setObjectName("status_textedit")
        self.status_textedit.setFontPointSize(10)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.input_label.setText(_translate("MainWindow", "Input address:"))
        self.reset_button.setText(_translate("MainWindow", "reset"))
        self.search_button.setText(_translate("MainWindow", "search"))
        self.view_button.setItemText(0, _translate("MainWindow", "scheme"))
        self.view_button.setItemText(1, _translate("MainWindow", "satellite"))
        self.view_button.setItemText(2, _translate("MainWindow", "hybrid"))
        self.postId_box.setText(_translate("MainWindow", "Post index"))