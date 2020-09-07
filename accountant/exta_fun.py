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
    username = message.chat.username
    chat_id = message.chat.id
    date = datetime.date.today()
    conn = sqliteConnector()
    conn.add_note(username, date, float(text), chat_id)


def get_common_info():
    conn = sqliteConnector()
    mail = conn.get_info()
    return mail


def get_own_info():
    conn = sqliteConnector()
    mail = conn.get_users()
    return mail
