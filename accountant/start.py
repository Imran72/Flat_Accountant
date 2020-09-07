from accountant.exta_fun import is_number, insert_query, get_own_info, get_common_info
import telebot

token = "1379702508:AAGquXO8II-Uzky60_YHzR7Ni6yddMQOZhg"
bot = telebot.TeleBot(token=token)


# Обработчик начала общения
@bot.message_handler(commands=['start'])
def start_cmd(message):
    name = message.chat.first_name
    keybd = telebot.types.ReplyKeyboardMarkup(True)
    btn1 = telebot.types.KeyboardButton(text='Узнать общие данные⚖️')
    btn2 = telebot.types.KeyboardButton(text='Узнать частные данные🤷‍')
    keybd.add(btn1)
    keybd.add(btn2)
    text = 'Привет, {}! \n \n'.format(name)
    text += "Я храню данные по вашей квартире💵 \n" \
            "Отправь сумму денег, потраченную тобою на общее дело,и я добавлю их в базу🏦 \n" \
            "По истечении 7 дней все пользователи получат уведомление - каждый узнает, сколько должен😱"
    bot.send_message(message.chat.id, text, reply_markup=keybd)


# Обработчик текстовых сообщений
@bot.message_handler(content_types=['text'])
def send_text(message):
    chat_id = message.chat.id
    text = message.text
    if is_number(text):
        try:
            text = str(text).replace(',', '.')
            insert_query(message, text)
            mail = 'Ваши данные были успешно занесены в базу! Спасибо за содействие'
            bot.send_message(chat_id, mail)
        except Exception as e:
            mail = 'К сожалению, что-то пошло не так. Убедитель, что вы ввели валидное положительное число'
            bot.send_message(chat_id, mail)
            print(e+'!')
    elif text == 'Узнать общие данные⚖️':
        mail = get_common_info()
        bot.send_message(chat_id, mail, parse_mode='Markdown')
    elif text == 'Узнать частные данные🤷‍':
        mail = "Выберите номер пользователя, который вас интересует:\n\n" + get_own_info()
        bot.send_message(chat_id, mail)
    else:
        mail = 'Нужно отправить сумму, которую вы сегодня потратили!'
        bot.send_message(chat_id, mail)

def f():
    pass
'''
# ежедневная проверка на запись
def job():
    conn = sqliteConnector()
    conn.check_days_of_life()


schedule.every().day.at("10:30").do(job)


def go():
    while True:
        schedule.run_pending()
        time.sleep(1)


t = threading.Thread(target=go, name="тест")
t.start()
'''

bot.polling()
