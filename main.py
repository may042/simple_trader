# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

from PyQt5 import uic
from PyQt5 import QtWidgets
from UI.simple_trader import Ui_Dialog
from UI.pokrivator_editor import Ui_pokrivator_editor
import sys
import pandas as pd

import os

main_dialog = uic.loadUiType("UI/simple_trader.ui")[0]
pokrivator_editor_form = uic.loadUiType("UI/pokrivator_editor.ui")[0]

class MainWindow(QtWidgets.QMainWindow ,Ui_Dialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.df = pd.read_excel("main_df.xlsx")

        columns = self.df.columns
        self.table_tasks.setColumnCount(len(columns))
        self.table_tasks.setHorizontalHeaderLabels(columns)
        self.table_tasks.setColumnWidth(0,40)

        self.show_main_table()

        #СОБЫТИЯ
        self.pushButton_edit.clicked.connect(self.launch_editor)
        #self.pushButton_create.clicked.connect(self.test_)


    def test_(self):
        print("EST!!")


    def launch_editor(self):
        """Запускает окно с редактором покрыватора"""
        dialog = PokrivatorEditor(self)
        dialog.exec_()


    def show_main_table(self):
        """Выводит содержимое Основного датафрейма в Основную таблицу"""

        self.table_tasks.setRowCount( self.df.shape[0] )

        for i in range(self.df.shape[0]):
            for j in range(self.table_tasks.columnCount()):
                self.table_tasks.setItem(i,j, QtWidgets.QTableWidgetItem(str(self.df.loc[i,self.table_tasks.horizontalHeaderItem(j).text()])))




class PokrivatorEditor(QtWidgets.QDialog , Ui_pokrivator_editor):
    def __init__(self, root,):
        super().__init__()
        #QtWidgets.QDialog.__init__(self, parent)
        self.setupUi(self)
        self.main = root

        self.df_stocks = pd.read_excel("stocks.xlsx")
        self.editor_short_name.addItems(self.df_stocks.short_name.values)
        self.set_codes_()

        # СОБЫТИЯ
        self.editor_short_name.currentTextChanged.connect(self.set_codes_)   #изменение в боксе short_name
        self.buttonBox.accepted.connect(self.add_task)


    def set_codes_(self ):
        """Функция устанавливает значения в окошки sec_code , class_code в зависимости от значения поля short_name"""
        short_name = self.editor_short_name.currentText()
        if short_name in self.df_stocks.short_name.values:
            sec_code = self.df_stocks.loc[self.df_stocks.short_name == short_name , "sec_code"].values[0]
            class_code = self.df_stocks.loc[self.df_stocks.short_name == short_name, "class_code"].values[0]
            self.editor_sec_code.setText(sec_code)
            self.editor_class_code.setText(class_code)
        else:
            self.editor_sec_code.clear()
            self.editor_class_code.clear()

    def add_task(self):
        """Функция считывает введённые значения """
        N = self.main.df.shape[0]
        self.main.df.loc[ N, "short_name" ] = self.editor_short_name.currentText()
        self.main.df.loc[ N, "sec_code"] = self.editor_sec_code.text()
        self.main.df.loc[ N, "class_code"] = self.editor_class_code.text()
        self.main.df.loc[ N, "Sell Quantity"] = self.editor_sell_quantity.text()
        self.main.df.loc[ N, "Price"] = self.editor_price.text()
        self.main.df.loc[ N, "Min Bid"] = self.editor_min_bid.text()
        self.main.df.loc[ N, "Status"] = "Active"
        self.main.df.loc[ N, "Executed"] = 0
        self.main.df.loc[ N, "Rest"] = self.editor_min_bid.text()

        self.main.show_main_table()


#if __name__ == '__main__':
# create QApplication object
app = QtWidgets.QApplication([])

# create your QMainWindow instance
window = MainWindow()

# show the window
window.show()

# start the loop
sys.exit(app.exec_())


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
