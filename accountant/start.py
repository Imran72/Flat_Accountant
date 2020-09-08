from accountant.relational import is_number, insert_query, get_users, get_common_info, get_private_info
import telebot
from .Mode import Mode

token = "1379702508:AAGquXO8II-Uzky60_YHzR7Ni6yddMQOZhg"
bot = telebot.TeleBot(token=token)
moder = Mode()


# Обработчик начала общения
@bot.message_handler(commands=['start'])
def start_cmd(message):
    name = message.chat.first_name
    keybd = telebot.types.ReplyKeyboardMarkup(True)
    btn3 = telebot.types.KeyboardButton(text='Добавить Money🤑️')
    btn1 = telebot.types.KeyboardButton(text='Узнать общие данные⚖️')
    btn2 = telebot.types.KeyboardButton(text='Узнать частные данные🤷‍')
    keybd.add(btn3)
    keybd.add(btn1)
    keybd.add(btn2)
    text = 'Привет, {}! \n \n'.format(name)
    text += "Я храню данные по вашей квартире💵 \n" \
            "Отправь сумму денег, потраченную тобою на общее дело,и я добавлю их в базу🏦 \n" \
            "По истечении 7 дней все пользователи получат уведомление - каждый узнает, сколько должен😱"
    bot.send_message(message.chat.id, text, reply_markup=keybd)


# Обработчик 0-положения
@bot.message_handler(content_types=['text'], func=lambda message: moder.mode == Mode.States.INITIAL_STATE)
def send_text(message):
    chat_id = message.chat.id
    text = message.text
    if text == 'Узнать общие данные⚖️':
        mail = get_common_info()
        bot.send_message(chat_id, mail, parse_mode='Markdown')
    elif text == 'Узнать частные данные🤷‍':
        mail = "Выберите номер пользователя, который вас интересует:\n\n" + get_users()
        bot.send_message(chat_id, mail)
        moder.mode = Mode.States.PRIVATE_INFO
    elif text == 'Добавить Money🤑️':
        mail = "Прекрасный выбор! Вводите сумму🤖"
        moder.mode = Mode.States.RECORDING_STATE
        bot.send_message(chat_id, mail)
    else:
        mail = 'Для начала выберите режим, мой друг)'
        bot.send_message(chat_id, mail)


# Обработчик текстовых сообщений или, иначе говоря, 1-состояния
@bot.message_handler(content_types=['text'], func=lambda message: moder.mode == Mode.States.RECORDING_STATE)
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
        moder.mode = Mode.States.INITIAL_STATE
    elif text == 'Узнать общие данные⚖️':
        mail = get_common_info()
        bot.send_message(chat_id, mail, parse_mode='Markdown')
        moder.mode = Mode.States.INITIAL_STATE
    elif text == 'Узнать частные данные🤷‍':
        mail = "Выберите номер пользователя, который вас интересует:\n\n" + get_users()
        bot.send_message(chat_id, mail)
        moder.mode = Mode.States.PRIVATE_INFO
    else:
        mail = 'Нужно отправить сумму, которую вы сегодня потратили!'
        bot.send_message(chat_id, mail)


# Обработчик запроса на частные данные или, иначе говоря, 2-состояния
@bot.message_handler(content_types=['text'], func=lambda message: moder.mode == Mode.States.PRIVATE_INFO)
def send_user_info(message):
    chat_id = message.chat.id
    text = str(message.text)
    if text == 'Узнать частные данные🤷‍':
        mail = "Выберите номер пользователя, который вас интересует:\n\n" + get_users()
        bot.send_message(chat_id, mail)
        moder.mode = Mode.States.PRIVATE_INFO
    elif text.isdigit():
        number = int(text)
        members = len(get_users().split('\n'))
        if number < 1 or number > members - 1:
            mail = "Нет пользователя с таким номером!"
            bot.send_message(chat_id, mail)
        else:
            mail = get_private_info(number)
            bot.send_message(chat_id, mail, parse_mode='Markdown')
            moder.mode = Mode.States.INITIAL_STATE
    elif text == 'Узнать общие данные⚖️':
        mail = get_common_info()
        bot.send_message(chat_id, mail, parse_mode='Markdown')
        moder.mode = Mode.States.INITIAL_STATE
    else:
        mail = "Пользователя под таким номером нет! Попытайтесь еще разок🤫"
        bot.send_message(chat_id, mail)


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
