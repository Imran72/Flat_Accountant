from accountant.sqliteConnector import sqliteConnector
import datetime


# Проверка на число
def is_number(s):
    try:
        s = str(s).replace(',', '.')
        s = float(s)
        if s >= 0:
            return True
        else:
            return False
    except ValueError:
        return False


# Формирование данных и запись в базу данных
def insert_query(message, text):
    username = message.chat.first_name
    chat_id = message.chat.id
    date = datetime.date.today()
    conn = sqliteConnector()
    conn.add_note(username, date, float(text), chat_id)


# Возвращает информацию по всем пользователям (неподробно)
def get_common_info():
    conn = sqliteConnector()
    mail = conn.get_common_info()
    return mail


# Возвращает списик пользователей по которым в дальнейшем можно запросить полную информацию
def get_users():
    conn = sqliteConnector()
    mail = conn.get_users()
    return mail


# Возвращает приватную и полную информацию по пользователю: сумма+дата траты
def get_private_info(number):
    conn = sqliteConnector()
    mail = conn.get_private_info(number)
    return mail
