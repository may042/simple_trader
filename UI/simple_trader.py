# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'simple_trader.ui'
#
# Created by: PyQt5 UI code generator 5.15.11
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(1172, 789)
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(20, 30, 47, 13))
        self.label.setObjectName("label")
        self.pushButton_del = QtWidgets.QPushButton(Dialog)
        self.pushButton_del.setGeometry(QtCore.QRect(1070, 510, 81, 31))
        self.pushButton_del.setObjectName("pushButton_del")
        self.pushButton_edit = QtWidgets.QPushButton(Dialog)
        self.pushButton_edit.setGeometry(QtCore.QRect(240, 510, 101, 31))
        self.pushButton_edit.setObjectName("pushButton_edit")
        self.pushButton_double = QtWidgets.QPushButton(Dialog)
        self.pushButton_double.setGeometry(QtCore.QRect(130, 510, 101, 31))
        self.pushButton_double.setObjectName("pushButton_double")
        self.pushButton_create = QtWidgets.QPushButton(Dialog)
        self.pushButton_create.setGeometry(QtCore.QRect(20, 510, 101, 31))
        self.pushButton_create.setObjectName("pushButton_create")
        self.pushButton_save = QtWidgets.QPushButton(Dialog)
        self.pushButton_save.setGeometry(QtCore.QRect(20, 700, 161, 41))
        self.pushButton_save.setObjectName("pushButton_save")
        self.table_tasks = QtWidgets.QTableWidget(Dialog)
        self.table_tasks.setGeometry(QtCore.QRect(10, 50, 1151, 451))
        self.table_tasks.setObjectName("table_tasks")
        self.table_tasks.setColumnCount(0)
        self.table_tasks.setRowCount(0)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "SuperTrader"))
        self.label.setText(_translate("Dialog", "Задания"))
        self.pushButton_del.setText(_translate("Dialog", "Удалить"))
        self.pushButton_edit.setText(_translate("Dialog", "Редактировать"))
        self.pushButton_double.setText(_translate("Dialog", "Дублировать"))
        self.pushButton_create.setText(_translate("Dialog", "Новое задание"))
        self.pushButton_save.setText(_translate("Dialog", "Сохранить задания в файл"))
