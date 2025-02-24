#
#
# Это библиотека, в которой находятся элементы трейдинга.
#
#


from datetime import datetime
import time  # Подписка на события по времени
from QuikPy import QuikPy  # Работа с QUIK из Python через LUA скрипты QuikSharp
import winsound


class pokrivator():

    def __init__(self, qp_provider, task_dict):

        self.tasks = task_dict
        self.qp_provider = qp_provider

        self.qp_provider.OnQuote = self.cover_this_shit




    def cover_this_shit(self, data):
        """Пользовательский обработчик событий:
        - Изменение стакана котировок
        - Получение обезличенной сделки
        - Получение новой свечки
        """
        # print(f'{datetime.now().strftime("%d.%m.%Y %H:%M:%S")} - {data["data"]}')  # Печатаем полученные данные

        bids = data["data"]['bid']

        for bid in bids:
            if data["data"]["sec_code"] in  self.tasks.keys():





                and \
                    float(bid['price']) >= self.min_price and self.already_covered < self.need_to_cover and \
                    int(bid['quantity']) >= self.min_bid_size and int(bid['quantity']) <= self.max_bid_size:

                self.cur_pos = get_current_position(client_code=self.client_code, sec_code=self.sec_code)

                if self.cur_pos > 0 or self.ignore_cur_pos:
                    if self.ignore_cur_pos:
                        quantity = min( int(bid['quantity']), self.need_to_cover - self.already_covered )
                    else:
                        quantity = min(int(bid['quantity']), self.cur_pos, self.need_to_cover - self.already_covered)

                    transaction = {  # Все значения должны передаваться в виде строк
                        'TRANS_ID': str(1),  # Номер транзакции задается клиентом
                        'CLIENT_CODE': self.client_code,  # Код клиента. Для фьючерсов его нет
                        'ACCOUNT': 'L01-00000F00',  # Счет
                        'ACTION': 'NEW_ORDER',  # Тип заявки: Новая лимитная/рыночная заявка
                        'CLASSCODE': self.class_code,  # Код площадки
                        'SECCODE': self.sec_code,  # Код тикера
                        'OPERATION': 'S',  # B = покупка, S = продажа
                        'PRICE': bid['price'],
                        # Цена исполнения. Для рыночных фьючерсных заявок наихудшая цена в зависимости от направления. Для остальных рыночных заявок цена = 0
                        'QUANTITY': str(quantity),  # Кол-во в лотах
                        'TYPE': 'L'}  # L = лимитная заявка (по умолчанию), M = рыночная заявка

                    if self.virtual_mode:
                        print( f'Новая лимитная/рыночная заявка отправлена на рынок: ... ')

                    else:
                        print( f'Новая лимитная/рыночная заявка отправлена на рынок: {qp_provider.SendTransaction(transaction)["data"]}')


                    self.already_covered += int(bid['quantity'])
                    time.sleep(0.051)

                    # выясняю номер приказа на случай если он не заполнен
                    orders = [x for x in qp_provider.GetOrders(self.client_code, self.sec_code)['data']
                              if x['flags'] == 29 and x['price'] == bid['price']]
                    # отменяю
                    if len(orders) > 0:
                        transaction = {
                            'TRANS_ID': str(2),  # Номер транзакции задается клиентом
                            'ACTION': 'KILL_ORDER',  # Тип заявки: Удаление существующей заявки
                            'CLASSCODE': 'TQOB',  # Код площадки
                            'SECCODE': self.sec_code,  # Код тикера
                            'ORDER_KEY': str(orders[0]['ordernum'])}  # Номер заявки
                        print(
                            f'Удаление заявки отправлено на рынок: {qp_provider.SendTransaction(transaction)["data"]}')

                    winsound.Beep(600, 800)
                    print("Продаю {} по {} . Осталось {}.".format(  quantity , bid['price'], self.need_to_cover - self.already_covered ))
                    print(bid)


def get_current_position( sec_code , client_code='395058'):
    """Выдаёт текущую позицию по инструменту, по дефолту ОФЗ 26238 на основном аккаунте"""

    out = [x['currentbal'] for x in qp_provider.GetDepoLimits(sec_code)['data'] if x['client_code'] == client_code
           and x['limit_kind'] == 1]
    if len(out) == 0:
        return 0
    else:
        return out[0]


if __name__ == '__main__':  # Точка входа при запуске этого скрипта
    qp_provider = QuikPy()  # Подключение к локальному запущенному терминалу QUIK

    class_code = 'TQCB'  # Класс тикера
    sec_code =    'RU000A10A141' #'SU26238RMFS4'  # 'RU000A108UJ6'

    sec_dict = {26244 : "SU26244RMFS2" , 26240:"SU26240RMFS0" , 26238:"SU26238RMFS4" , 26230:"SU26230RMFS1" , 26243:"SU26243RMFS4" ,
                26246: 'SU26246RMFS7' , "gazprom":"RU000A107F49" , 26247:"SU26247RMFS5" , 26233:"SU26233RMFS5" , 26245:"SU26245RMFS9"}


    print(f'Подписка на изменения стакана {class_code}.{sec_code}:', qp_provider.SubscribeLevel2Quotes(class_code, sec_code)['data'])
    print('Статус подписки:', qp_provider.IsSubscribedLevel2Quotes(class_code, sec_code)['data'])
    sleep_sec = 30000000  # Кол-во секунд получения котировок

    #pok = pokrivator(99.45, need_to_cover = 300 , min_bid_size=5, max_bid_size=2000000,  ignore_cur_pos=False , client_code='395058/19V63' ,  sec_code= 'RU000A107SA1' )

    #pok1 = pokrivator(75.25, need_to_cover=4000, min_bid_size=100, max_bid_size=2000000,
    #                                  ignore_cur_pos=False , client_code='395058/19V63' ,  sec_code= sec_dict[26247] , class_code="TQOB")

    #pok2 = pokrivator(99.35, need_to_cover=900, min_bid_size=10, max_bid_size=2000000, ignore_cur_pos=False , client_code='395058' ,  sec_code= sec_dict["gazprom"] )

    #pok3 = pokrivator(63.45, need_to_cover=4000, min_bid_size=1, max_bid_size=10000,  ignore_cur_pos=True , client_code='395058/19V63' ,  sec_code= sec_dict[26243] , class_code="TQOB")

    #pok4 = pokrivator(64.79, need_to_cover=7000, min_bid_size=1, ignore_cur_pos=True , client_code='395058/19V63' ,  sec_code= sec_dict[26243] , class_code="TQOB")

    #pok2 = pokrivator(50.37, need_to_cover=3500, min_bid_size=50, max_bid_size=2000000, ignore_cur_pos=False , client_code='395058' ,  sec_code= sec_dict[26238] )
    #pok2 = pokrivator(98, need_to_cover=1500, min_bid_size=1, max_bid_size=2000000, ignore_cur_pos=False , client_code='395058/19V63' ,  sec_code= "SU29027RMFS8" , class_code="TQOB" )
    pok2 = pokrivator(100.49, need_to_cover=900, min_bid_size=1, max_bid_size=2000000, ignore_cur_pos=False , client_code='395058/19V63' ,  sec_code= "RU000A10A141" , class_code="TQCB" ) # монополия



    print('Секунд котировок:', sleep_sec)
    time.sleep(sleep_sec)  # Ждем кол-во секунд получения котировок
    print(f'Отмена подписки на изменения стакана:', qp_provider.UnsubscribeLevel2Quotes(class_code, sec_code)['data'])
    print('Статус подписки:', qp_provider.IsSubscribedLevel2Quotes(class_code, sec_code)['data'])
    qp_provider.OnQuote = qp_provider.DefaultHandler  # Возвращаем обработчик по умолчанию


# SU26244RMFS2 - 26244
# SU26240RMFS0   - 26240
    # SU26230RMFS1  26230


    # Выход
    qp_provider.CloseConnectionAndThread()  # Перед выходом закрываем соединение и поток QuikPy
