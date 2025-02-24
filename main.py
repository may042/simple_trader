# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

from PyQt5 import uic
from PyQt5 import QtWidgets
from UI.simple_trader import Ui_Dialog
from UI.pokrivator_editor import Ui_pokrivator_editor
import sys
import pandas as pd
from QuikPy import QuikPy
import time

import os


# main_dialog = uic.loadUiType("UI/simple_trader.ui")[0]
# pokrivator_editor_form = uic.loadUiType("UI/pokrivator_editor.ui")[0]

class MainWindow(QtWidgets.QMainWindow, Ui_Dialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.df = pd.read_excel("main_df.xlsx", dtype=str)
        self.task_dict = {}
        self.qp_provider = QuikPy()
        self.status_boxes = {}

        columns = self.df.columns
        self.table_tasks.setColumnCount(len(columns))
        self.table_tasks.setHorizontalHeaderLabels(columns)
        self.table_tasks.setColumnWidth(0, 240)

        self.show_main_table()

        # СОБЫТИЯ
        self.pushButton_edit.clicked.connect(lambda: self.launch_editor(self.table_tasks.currentRow()))
        self.pushButton_create.clicked.connect(lambda: self.launch_editor(self.df.shape[0]))
        self.pushButton_del.clicked.connect(self.del_task)
        self.pushButton_save.clicked.connect(self.save_table)

        self.qp_provider.OnQuote = self.handle  # триггер проверки по изменению котировок
        self.table_tasks.cellChanged.connect(self.change_df_cell)

        # Торговый код


        for i in self.df.index:
            print(f'Подписка на изменения стакана {self.df.loc[i, "class_code"]}.{self.df.loc[i, "sec_code"]}:',
                  self.qp_provider.SubscribeLevel2Quotes(self.df.loc[i, "class_code"], self.df.loc[i, "sec_code"])[
                      'data'])
            print('Статус подписки:',
                  self.qp_provider.IsSubscribedLevel2Quotes(self.df.loc[i, "class_code"], self.df.loc[i, "sec_code"])[
                      'data'])



    def df_to_dict(self, df):
        """Функция принимает датафрейм выдаёт словарь с заданиями"""

        task_dict = {}

        for i in df.index:

            sec_code = df.loc[i, "sec_code"]

            # создаю пустой лист для заданий с данным инструментом
            if sec_code not in task_dict.keys():
                task_dict[sec_code] = []

            int_dict = {"bid": {"quantity": {"max": 10000000, "min": int(df.loc[i, "Min Bid"]) },
                                "price": {"min": float(df.loc[i, "Price"]), "max": None}},
                        "Account": df.loc[i, "Account"],
                        "IgnoreCurPos": False,
                        "TaskID": i,
                        "NeedToSell": int(df.loc[i, "Rest"]),
                        "class_code": df.loc[i, "class_code"],
                        "Type": df.loc[i, "Type"]
                        }

            task_dict[sec_code].append(int_dict)

        return task_dict

    def change_df_cell(self, row , column):
        """Функция отрабатывает при изменении в основной таблице. Записывает соответствующее новое значение в датафрейм."""

        col_name = self.table_tasks.horizontalHeaderItem(column).text()

        self.df.loc[ row , col_name ] = self.table_tasks.currentItem().text()



    def get_volumes_(self, size_list, max_price=None, min_price=None):
        """Функция принимает лист словарей с бидами или оферами ,
        выводит объём и цену удовлетворяющую критерию либо max_price , либо min_price"""

        try:

            if max_price is None and min_price is not None:
                i = len(size_list) - 1
                vol = 0

                while float(size_list[i]["price"]) >= min_price :
                    vol += int(size_list[i]["quantity"])
                    i -= 1


                return vol, float(size_list[i + 1]["price"])

            elif max_price is not None and min_price is None:
                i = 0
                vol = 0

                while float(size_list[i]["price"]) <= max_price :
                    vol += int(size_list[i]["quantity"])
                    i += 1

                return vol, float(size_list[i - 1]["price"])

            else:
                return 0, 0

        except:
            return 0, 0


    def handle(self, data):
        """Функция принимает котировки ,  словарь с заданиями , и действие.
           Сравнивает котировки с заданием, если условие задания выполняется, то выполняет действие"""
        data = data["data"]
        if data["sec_code"] in self.task_dict.keys():  # проверяю есть ли задания для данного стака

            for int_task in self.task_dict[data["sec_code"]]:

                print(f"Проверяю {data["sec_code"]}")

                if "bid" in int_task.keys():

                    size, price = self.get_volumes_(data["bid"],
                                                    max_price=int_task["bid"]["price"]["max"],
                                                    min_price=int_task["bid"]["price"]["min"])

                    print(f" Для {data["sec_code"]} , видим {size} облигаций выше цены {price} ")

                    print(int_task)

                    if int_task["bid"]["quantity"]["max"] > size >= int_task["bid"]["quantity"]["min"]:

                        if int_task["Type"] == "sell":
                            self.sell(NeedToSell=int_task["NeedToSell"],
                                       Account=int_task["Account"],
                                       sec_code=data["sec_code"],
                                       class_code=int_task["class_code"],
                                       size=size,
                                       price=price,
                                       IgnoreCurPos=int_task["IgnoreCurPos"],
                                       TaskID=int_task["TaskID"],
                                       test_mode=True)

    def get_current_position(self, sec_code, client_code ):
        """Выдаёт текущую позицию по инструменту"""

        out = [x['currentbal'] for x in self.qp_provider.GetDepoLimits(sec_code)['data'] if x['client_code'] == client_code
               and x['limit_kind'] == 1]
        if len(out) == 0:
            return 0
        else:
            return out[0]

    def sell(self, NeedToSell, Account, sec_code, class_code, size, price, IgnoreCurPos, TaskID, test_mode):

        if test_mode:
            print(
                f""" Продаю с аккаунта {Account}  облигацию {sec_code} класса {class_code}  в количестве {size} по цене {price} . 
                        IgnoreCurPos = {IgnoreCurPos}. По задаче {TaskID}. А надо было продать {NeedToSell}. """)
            time.sleep(1)

        else:
            pass





    def closeEvent(self, a0):
        self.qp_provider.OnQuote = self.qp_provider.DefaultHandler  # Возвращаем обработчик по умолчанию
        self.qp_provider.CloseConnectionAndThread()  # Перед выходом закрываем соединение и поток QuikPy
        print("Выход корректный")
        app.quit()

    def test_(self):
        print("EST!!")

    def launch_editor(self, index):
        """Запускает окно с редактором покрыватора"""

        dialog = PokrivatorEditor(self, index)

        if index in self.df.index:
            dialog.editor_short_name.setCurrentText(str(self.df.loc[index, "short_name"]))
            dialog.editor_sec_code.setText(str(self.df.loc[index, "sec_code"]))
            dialog.editor_class_code.setText(str(self.df.loc[index, "class_code"]))
            dialog.editor_sell_quantity.setText(str(self.df.loc[index, "Sell Quantity"]))
            dialog.editor_price.setText(str(self.df.loc[index, "Price"]))
            dialog.editor_min_bid.setText(str(self.df.loc[index, "Min Bid"]))

            # устанавливаю радиобаттон счёта в едиторе
            if str(self.df.loc[index, "Account"]) == "395058":
                dialog.radioButton.setChecked(True)

            elif str(self.df.loc[index, "Account"]) == "395058/19V63":
                dialog.radioButton_2.setChecked(True)

            elif str(self.df.loc[index, "Account"]) == "13KP3M":
                dialog.radioButton_3.setChecked(True)

        dialog.exec_()

    def show_main_table(self):
        """Выводит содержимое Основного датафрейма в Основную таблицу"""

        self.table_tasks.setRowCount(self.df.shape[0])



        for j in range(self.table_tasks.columnCount()):
            col_name = self.table_tasks.horizontalHeaderItem(j).text()

            for i in range(self.df.shape[0]):

                self.table_tasks.setItem(i, j, QtWidgets.QTableWidgetItem( str(self.df.loc[i, col_name])) )


        # при кажом отображении основной таблицы синхронизирую словарь заданий и датафрейм
        self.task_dict = self.df_to_dict(self.df)




    def combo_table_(self, comboBox ):
        """Техническая функция , отклик на изменение комбобоксов со статусами в основной таблице"""
        print("#######################")
        print(comboBox.id_)
        self.df.loc[comboBox.id_, "Status"] = comboBox.currentText()
        self.task_dict = self.df_to_dict(self.df)


    def del_task(self):
        """Функция удаляет выделенную задачу"""
        self.df = self.df.drop(self.table_tasks.currentRow()).reset_index(drop=True)
        self.show_main_table()

    def save_table(self):
        """Функция сохраняет текущую таблицу задач"""
        self.df.to_excel("main_df.xlsx", index=False)


class PokrivatorEditor(QtWidgets.QDialog, Ui_pokrivator_editor):
    def __init__(self, root, indx):
        super().__init__()

        self.setupUi(self)
        self.main = root
        self.indx = indx

        self.df_stocks = pd.read_excel("stocks.xlsx")
        self.editor_short_name.addItems(self.df_stocks.short_name.values)
        self.set_codes_()

        # СОБЫТИЯ
        self.editor_short_name.currentTextChanged.connect(self.set_codes_)  # изменение в боксе short_name
        self.buttonBox.accepted.connect(self.add_task)

    def set_codes_(self):
        """Функция устанавливает значения в окошки sec_code , class_code в зависимости от значения поля short_name"""
        short_name = self.editor_short_name.currentText()
        if short_name in self.df_stocks.short_name.values:
            sec_code = self.df_stocks.loc[self.df_stocks.short_name == short_name, "sec_code"].values[0]
            class_code = self.df_stocks.loc[self.df_stocks.short_name == short_name, "class_code"].values[0]
            self.editor_sec_code.setText(sec_code)
            self.editor_class_code.setText(class_code)
        else:
            self.editor_sec_code.clear()
            self.editor_class_code.clear()

    def add_task(self):
        """Функция считывает введённые значения """

        self.main.df.loc[self.indx, "short_name"] = self.editor_short_name.currentText()
        self.main.df.loc[self.indx, "sec_code"] = self.editor_sec_code.text()
        self.main.df.loc[self.indx, "class_code"] = self.editor_class_code.text()
        self.main.df.loc[self.indx, "Sell Quantity"] = self.editor_sell_quantity.text()
        self.main.df.loc[self.indx, "Price"] = self.editor_price.text()
        self.main.df.loc[self.indx, "Min Bid"] = self.editor_min_bid.text()
        self.main.df.loc[self.indx, "Status"] = "Active"
        self.main.df.loc[self.indx, "Executed"] = 0
        self.main.df.loc[self.indx, "Rest"] = self.editor_min_bid.text()

        if self.radioButton.isChecked():
            self.main.df.loc[self.indx, "Account"] = "395058"
        elif self.radioButton_2.isChecked():
            self.main.df.loc[self.indx, "Account"] = "395058/19V63"
        elif self.radioButton_3.isChecked():
            self.main.df.loc[self.indx, "Account"] = "13KP3M"

        self.main.show_main_table()


# if __name__ == '__main__':
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
