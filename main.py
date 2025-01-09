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

# main_dialog = uic.loadUiType("UI/simple_trader.ui")[0]
# pokrivator_editor_form = uic.loadUiType("UI/pokrivator_editor.ui")[0]

class MainWindow(QtWidgets.QMainWindow ,Ui_Dialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.df = pd.read_excel("main_df.xlsx")

        columns = self.df.columns
        self.table_tasks.setColumnCount(len(columns))
        self.table_tasks.setHorizontalHeaderLabels(columns)
        self.table_tasks.setColumnWidth(0,240)

        self.show_main_table()

        #СОБЫТИЯ
        self.pushButton_edit.clicked.connect(lambda : self.launch_editor(self.table_tasks.currentRow()))
        self.pushButton_create.clicked.connect(lambda : self.launch_editor(self.df.shape[0]))
        self.pushButton_del.clicked.connect(self.del_task)
        self.pushButton_save.clicked.connect(self.save_table)

        #quit = QtWidgets.QAction("Quit" , self)
        #quit.triggered.connect(self.test_)

    def closeEvent(self, a0):
        print("est4")
        app.quit()


    def test_(self):
        print("EST!!")


    def launch_editor(self, index):
        """Запускает окно с редактором покрыватора"""

        dialog = PokrivatorEditor(self, index)

        if index in self.df.index:
            dialog.editor_short_name.setCurrentText( str(self.df.loc[index, "short_name"]) )
            dialog.editor_sec_code.setText( str(self.df.loc[index, "sec_code"]) )
            dialog.editor_class_code.setText( str(self.df.loc[index, "class_code"]) )
            dialog.editor_sell_quantity.setText( str(self.df.loc[index, "Sell Quantity"]) )
            dialog.editor_price.setText( str(self.df.loc[index, "Price"]) )
            dialog.editor_min_bid.setText( str(self.df.loc[index, "Min Bid"]) )

            # устанавливаю радиобаттон счёта в едиторе
            if str(self.df.loc[index, "Account"] ) == "395058":
                dialog.radioButton.setChecked(True)

            elif str(self.df.loc[index, "Account"] ) == "395058/19V63":
                dialog.radioButton_2.setChecked(True)

            elif str(self.df.loc[index, "Account"] ) == "13KP3M":
                dialog.radioButton_3.setChecked(True)


        dialog.exec_()

    def show_main_table(self):
        """Выводит содержимое Основного датафрейма в Основную таблицу"""

        self.table_tasks.setRowCount( self.df.shape[0] )

        for i in range(self.df.shape[0]):
            for j in range(self.table_tasks.columnCount()):
                self.table_tasks.setItem(i,j, QtWidgets.QTableWidgetItem(str(self.df.loc[i,self.table_tasks.horizontalHeaderItem(j).text()])))

    def del_task(self):
        """Функция удаляет выделенную задачу"""
        self.df = self.df.drop(self.table_tasks.currentRow()).reset_index(drop=True)
        self.show_main_table()

    def save_table(self):
        """Функция сохраняет текущую таблицу задач"""
        self.df.to_excel("main_df.xlsx", index=False)







class PokrivatorEditor(QtWidgets.QDialog , Ui_pokrivator_editor):
    def __init__(self, root, indx):
        super().__init__()

        self.setupUi(self)
        self.main = root
        self.indx = indx

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

        self.main.df.loc[ self.indx, "short_name" ] = self.editor_short_name.currentText()
        self.main.df.loc[ self.indx, "sec_code"] = self.editor_sec_code.text()
        self.main.df.loc[ self.indx, "class_code"] = self.editor_class_code.text()
        self.main.df.loc[ self.indx, "Sell Quantity"] = self.editor_sell_quantity.text()
        self.main.df.loc[ self.indx, "Price"] = self.editor_price.text()
        self.main.df.loc[ self.indx, "Min Bid"] = self.editor_min_bid.text()
        self.main.df.loc[ self.indx, "Status"] = "Active"
        self.main.df.loc[ self.indx, "Executed"] = 0
        self.main.df.loc[ self.indx, "Rest"] = self.editor_min_bid.text()

        if self.radioButton.isChecked():
            self.main.df.loc[self.indx, "Account"] = "395058"
        elif self.radioButton_2.isChecked():
            self.main.df.loc[self.indx, "Account"] = "395058/19V63"
        elif self.radioButton_3.isChecked():
            self.main.df.loc[self.indx, "Account"] = "13KP3M"



        self.main.show_main_table()


#if __name__ == '__main__':
# create QApplication object
app = QtWidgets.QApplication([])

# create your QMainWindow instance
window = MainWindow()

# show the window
window.show()

print("est1")

# start the loop
sys.exit(app.exec_())

print("est2")


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
