# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'simple_trader.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_task_editor(object):
    def setupUi(self, task_editor):
        task_editor.setObjectName("task_editor")
        task_editor.resize(486, 335)
        self.buttonBox = QtWidgets.QDialogButtonBox(task_editor)
        self.buttonBox.setGeometry(QtCore.QRect(130, 290, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.comboBox = QtWidgets.QComboBox(task_editor)
        self.comboBox.setGeometry(QtCore.QRect(20, 50, 161, 31))
        self.comboBox.setObjectName("comboBox")
        self.label = QtWidgets.QLabel(task_editor)
        self.label.setGeometry(QtCore.QRect(20, 30, 91, 16))
        self.label.setObjectName("label")
        self.label_4 = QtWidgets.QLabel(task_editor)
        self.label_4.setGeometry(QtCore.QRect(30, 180, 61, 16))
        self.label_4.setObjectName("label_4")
        self.lineEdit_2 = QtWidgets.QLineEdit(task_editor)
        self.lineEdit_2.setGeometry(QtCore.QRect(100, 180, 113, 20))
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.label_5 = QtWidgets.QLabel(task_editor)
        self.label_5.setGeometry(QtCore.QRect(30, 230, 161, 16))
        self.label_5.setObjectName("label_5")
        self.lineEdit_3 = QtWidgets.QLineEdit(task_editor)
        self.lineEdit_3.setGeometry(QtCore.QRect(190, 230, 113, 20))
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.radioButton = QtWidgets.QRadioButton(task_editor)
        self.radioButton.setGeometry(QtCore.QRect(410, 60, 82, 17))
        self.radioButton.setObjectName("radioButton")
        self.buttonGroup = QtWidgets.QButtonGroup(task_editor)
        self.buttonGroup.setObjectName("buttonGroup")
        self.buttonGroup.addButton(self.radioButton)
        self.radioButton_2 = QtWidgets.QRadioButton(task_editor)
        self.radioButton_2.setGeometry(QtCore.QRect(410, 90, 82, 17))
        self.radioButton_2.setObjectName("radioButton_2")
        self.buttonGroup.addButton(self.radioButton_2)
        self.splitter = QtWidgets.QSplitter(task_editor)
        self.splitter.setGeometry(QtCore.QRect(30, 120, 207, 20))
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName("splitter")
        self.label_2 = QtWidgets.QLabel(self.splitter)
        self.label_2.setObjectName("label_2")
        self.lineEdit = QtWidgets.QLineEdit(self.splitter)
        self.lineEdit.setObjectName("lineEdit")
        self.label_3 = QtWidgets.QLabel(self.splitter)
        self.label_3.setObjectName("label_3")

        self.retranslateUi(task_editor)
        self.buttonBox.accepted.connect(task_editor.accept) # type: ignore
        self.buttonBox.rejected.connect(task_editor.reject) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(task_editor)

    def retranslateUi(self, task_editor):
        _translate = QtCore.QCoreApplication.translate
        task_editor.setWindowTitle(_translate("task_editor", "Задание"))
        self.label.setText(_translate("task_editor", "Инструмент"))
        self.label_4.setText(_translate("task_editor", "не дешевле"))
        self.label_5.setText(_translate("task_editor", "Миниммальный размер бида"))
        self.radioButton.setText(_translate("task_editor", "Main"))
        self.radioButton_2.setText(_translate("task_editor", "6 mln"))
        self.label_2.setText(_translate("task_editor", "Продать"))
        self.label_3.setText(_translate("task_editor", "лотов"))
