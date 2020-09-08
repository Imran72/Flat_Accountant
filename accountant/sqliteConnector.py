import sqlite3
import datetime
import itertools
import telebot

from . import config

token = config.token
bot = telebot.TeleBot(token=token)


# ORM-handmade или класс взаимодействия с базой данных, реализованной на Sqlite
class sqliteConnector:
    def __init__(self):
        self.start_day = '2020-09-08'
        self.days_of_life = 7

    # Запись данных пользователя
    def add_note(self, username, bill_date, bill, chat_id):
        with sqlite3.connect('mydatabase.db') as conn:
            conn.cursor().execute("""INSERT INTO notes (username, date, bill, chat_id)
            VALUES (?, ?, ?, ?)""",
                                  (username, bill_date, bill, chat_id))

    # Ежедневная проверка на истечение срока сбора данных
    def check_days_of_life(self):
        with sqlite3.connect('mydatabase.db') as conn:
            try:
                sql = """SELECT date from notes ORDER BY date"""
                cursor = conn.cursor()
                cursor.execute(sql)
                records = cursor.fetchall()
                print(records)
                start = datetime.datetime.strptime(records[0][0], '%Y-%m-%d')
                finish = datetime.datetime.strptime(records[-1][0], '%Y-%m-%d')
                print(start)
                print(finish)
                days = (finish - start).days
                if days >= self.days_of_life:
                    self.account_distribution()
                    self.clean_data()
                    self.start_day = datetime.date.today()
                    print("Данные были затерты")
                    return True
            except Exception:
                print("Вероятно еще нет данных")
                return False

    # Функция зачистки ненужных данных
    def clean_data(self):
        with sqlite3.connect('mydatabase.db') as conn:
            self.send_pdf()
            sql = """DELETE from notes"""
            cursor = conn.cursor()
            cursor.execute(sql)

    # Запрос на подсчет полной информации, расчет задолжностей по каждому пользователю
    def account_distribution(self):
        dict = {}
        with sqlite3.connect('mydatabase.db') as conn:
            sql = """SELECT * FROM notes """
            cursor = conn.cursor()
            records = cursor.execute(sql)
            for chat_id, bill_iter in itertools.groupby(records, key=lambda r: r[4]):
                full_bill = sum([i[3] for i in bill_iter])
                dict[chat_id] = full_bill

        medium_value = sum(list(dict.values())) / len(list(dict.keys()))
        for key in dict:
            delta = medium_value - dict[key]
            if delta > 0:
                text = 'За прошедшую неделю вы потратили меньше, нежели потратили ' \
                       'все остальные в среднем. Пора платить по счетам и нести долги ' \
                       'в казну! С вас полагается {} рублей'.format(delta)
            elif delta < 0:
                text = 'День сегодняшний ознаменован подсчетом затраченных всеми средств. По итогам этих подсчетов вы оказались' \
                       'в числе тех, кто внес в общее дело более, чем все остальные. Посему вам возлагается сумма в размере' \
                       '{} рублей'.format(delta)
            else:
                text = 'Вы чисты как снег. Заплатили вровень со средним значением, от чего вам полагается похвала в отсутсвие вознаграждения!'
            bot.send_message(key, text)

    # Функция, возвращающая общую информацию по всем пользователям
    def get_common_info(self):
        try:
            dict = {}
            with sqlite3.connect('mydatabase.db') as conn:
                sql = """SELECT * FROM notes"""
                cursor = conn.cursor()
                records = cursor.execute(sql)
                records = sorted(records, key=lambda r: r[4])
                for info, bill_iter in itertools.groupby(records, key=lambda r: str(r[1]) + "?" + str(r[4])):
                    full_bill = sum([i[3] for i in bill_iter])
                    dict[info] = full_bill
            message = ""
            index = 1
            for el in dict:
                one, two = el.split('?')
                message += '{}. [{}](tg://user?id={}) - {} рублей \n'.format(index, one, two, dict[el])
                index += 1
            return message
        except Exception:
            return 123

    # Функция, возвращающая список пользователей
    def get_users(self):
        try:
            st = ''
            index = 1
            with sqlite3.connect('mydatabase.db') as conn:
                sql = """SELECT DISTINCT username FROM notes """
                cursor = conn.cursor()
                records = cursor.execute(sql)
                for el in records:
                    st += "{}. {}\n".format(index, str(el)[2:-3])
                    index += 1
            return st
        except Exception:
            return "Пока данных нет"

    # Информация относительно определенного лица -  зависит от выбора
    def get_private_info(self, number):
        try:
            with sqlite3.connect('mydatabase.db') as conn:
                sql = """SELECT DISTINCT username, chat_id FROM notes """
                cursor = conn.cursor()
                records = cursor.execute(sql)
                name = ''
                chat_id = 0
                index = 1
                for el in records:
                    if index == number:
                        name = el[0]
                        chat_id = el[1]
                        break
                    index += 1
                records = conn.cursor().execute("""SELECT * FROM notes WHERE username = (?)""", (name,))
                st = 'Информация по пользователю [{}](tg://user?id={}):\n'.format(name, chat_id)
                for el in records:
                    st += str(el[2]) + ' потрачено ' + str(el[3]) + ' рублей\n'
                return st
        except Exception:
            return "Пока данных нет"

    # По истечению 7 дней данные затираются, формируется PDF документ, отправляемый...
    def send_pdf(self):
        pass
