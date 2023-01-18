####@commsoc_bot
import telebot
from telebot import apihelper
import requests
from datetime import datetime, timedelta, date
from telebot import types
import sqlite3



daytime = "08:00"
nighttime = "20:00"
deepnight = "00:00"
day = datetime.now().day
now = datetime.now()
current_date = date.today()
current_date_form = current_date.strftime("%d.%m.%Y")
current_time_form = now.strftime("%H:%M")
# current_time_form2 = now.strftime("%H:%M:%S")
date_delta = now + timedelta(days=-1)
date_delta2 = now + timedelta(days=1)
date_delta_form = date_delta.strftime("%d.%m.%Y")
date_delta2_form = date_delta2.strftime("%d.%m.%Y")
month_name = current_date.strftime("%b")

# (datetime.now() + timedelta(days=-1)).strftime("%d.%m.%Y")



database1 = sqlite3.connect('schedule.db')              #скрипт связывается с указанной базой данных для работы с её значениями

cur = database1.cursor()

cur.execute("""SELECT cur_dt, morn_id, evn_id, sm1.nameSurname, sm2.nameSurname, sm1.telegram, sm2.telegram FROM grafic
INNER JOIN smena AS sm1 ON grafic.morn_id=sm1.id
INNER JOIN smena AS sm2 ON grafic.evn_id=sm2.id""")   # выбор значений из таблицы grafic и объединение с таблицей smena согласно id определенной смены
dbexecute = cur.fetchall()                            # вызов всей таблицы

# print(dbexecute)


def delta_time_minus1():
    return (datetime.now() + timedelta(days=-1)).strftime("%d.%m.%Y")
def delta_time_plus1():
    return (datetime.now() + timedelta(days=1)).strftime("%d.%m.%Y")
def vcurrent_date():
    return date.today().strftime("%d.%m.%Y")
def vcurrent_time():
    return datetime.now().strftime("%H:%M")



def database():             #таблица grafic имеет поля с ответственными дневной и ночной смены(morn_id и evn_id). данная переменная фильтрует значения согласно текущей дате и времени суток и выводит только те, ячейки которые соответсвуют текущим временным рамкам и дате.
        for el in dbexecute:
            if el[0] == vcurrent_date() and daytime < vcurrent_time() < nighttime:          #проверяется соответствие временных маркеров. если строка даты равна текушей дате, а текущее время больше 08:00 но меньше 20:00 то возвращается строка с текущей датой и только столбец morn_id из бд schedule.db
                return str(el[1]) and str(el[3]) + ' ' + str(el[5])
            elif el[0] == vcurrent_date() and vcurrent_time() > nighttime:                 #проверяется соответствие временных маркеров. если строка даты равна текушей дате, а текущее время больше 20:00 то возвращается строка с текущей датой и только столбец evn_id из бд schedule.db
                return str(el[0]) and str(el[4]) + ' ' + str(el[6])
            elif el[0] == delta_time_minus1() and deepnight < vcurrent_time() < daytime:          #проверяется соответствие временных маркеров. если строка даты равна текушей дате минус 1 день, а текущее время больше 00:00 но меньше 08:00 то возвращается строка с предыдущей датой и только столбец evn_id из бд schedule.db
                return el[0] == delta_time_minus1() and (el[4]) + ' ' + (el[6])


def database_change():                          #переменная для передачи смены(кнопка "передача смены") и вызова следующего ответственного
    for el in dbexecute:
        if el[0] == vcurrent_date() and daytime < vcurrent_time() < nighttime:  # для дневной смены
            return str(el[0]) and str(el[4]) + ' ' + str(el[6])
            return ('1')
        elif el[0] == delta_time_plus1() and deepnight < vcurrent_time() < daytime:         # для ночной смены
            return el[0] == delta_time_plus1() and (el[4]) + ' ' + (el[6])
            return ('2')

# print(database_change())
# print(database())


database1.commit()

database1.close()



