# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\ui1.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        font = QtGui.QFont()
        font.setPointSize(14)
        MainWindow.setFont(font)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.input_edit = QtWidgets.QLineEdit(self.centralwidget)
        self.input_edit.setGeometry(QtCore.QRect(10, 10, 281, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.input_edit.setFont(font)
        self.input_edit.setObjectName("input_edit")
        self.horizontalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(300, -10, 500, 80))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.search_button = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.search_button.setObjectName("search_button")
        self.horizontalLayout.addWidget(self.search_button)
        self.reset_button = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.reset_button.setObjectName("reset_button")
        self.horizontalLayout.addWidget(self.reset_button)
        self.view_button = QtWidgets.QComboBox(self.horizontalLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.view_button.setFont(font)
        self.view_button.setObjectName("view_button")
        self.view_button.addItem("")
        self.view_button.addItem("")
        self.view_button.addItem("")
        self.horizontalLayout.addWidget(self.view_button)
        self.postId_box = QtWidgets.QCheckBox(self.horizontalLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.postId_box.setFont(font)
        self.postId_box.setObjectName("postId_box")
        self.horizontalLayout.addWidget(self.postId_box)
        self.address_label = QtWidgets.QLabel(self.centralwidget)
        self.address_label.setGeometry(QtCore.QRect(10, 50, 791, 81))
        self.address_label.setText("")
        self.address_label.setObjectName("address_label")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.search_button.setText(_translate("MainWindow", "search"))
        self.reset_button.setText(_translate("MainWindow", "reset"))
        self.view_button.setItemText(0, _translate("MainWindow", "scheme"))
        self.view_button.setItemText(1, _translate("MainWindow", "satellite"))
        self.view_button.setItemText(2, _translate("MainWindow", "hybrid"))
        self.postId_box.setText(_translate("MainWindow", "show post index"))