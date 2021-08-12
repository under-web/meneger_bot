import telebot
import time
from config import token_api
from intro_text import intro_text
import markups as mark
import sqlite3

my_id = 1107191282


def get_info_user(bot, message):  # функция для отправки информации о юзере в личку
    bot.send_message(my_id, message.text + ' '
                     + f'{message.chat.id}' + ' '
                     + f'{message.from_user.first_name}' + ' '
                     + f'{message.from_user.last_name}')


def run_bot():
    bot = telebot.TeleBot(token_api)


    @bot.message_handler(commands=['start'])  # приветственная функция
    def send_welcome(message):

        conn = sqlite3.connect('users_manager_bot.db')
        cur = conn.cursor()
        cur.execute("""CREATE TABLE IF NOT EXISTS users(
           userid INT PRIMARY KEY,
           fname TEXT,
           lname TEXT);
        """)
        conn.commit()

        user_info = (f'{message.chat.id}',
                     f'{message.from_user.first_name}',
                     f'{message.from_user.last_name}')

        cur.execute("INSERT OR IGNORE INTO users VALUES(?, ?, ?);", user_info)  # если есть такая запись не записывать
        conn.commit()

        img = open('title.jpg', 'rb')
        bot.send_photo(message.chat.id, img)
        bot.send_message(message.chat.id, intro_text,
                         reply_markup=mark.main_menu)

    @bot.message_handler(content_types=['text'])
    # TODO: добавить таблицу в базу с описанием программы клиента
    def send_markup(message):
        if message.text == 'Мне нужна другая программа':
            bot.send_message(message.chat.id, 'Хорошо! Опишите своими словами '
                                              'что должна делать программа и в конце своего описания поставьте символ @ '
                                              '\nчто-бы я понял Вас.', reply_markup=mark.del_markup)
        elif '@' in message.text:
            bot.send_message(message.chat.id, 'Спасибо, с Вами свяжутся в ближайшее время!',
                             reply_markup=mark.del_markup)
            get_info_user(bot, message)

        elif message.text == 'Мне нужен Чат-бот':
            bot.send_message(message.chat.id, 'Хорошо! На сколько вопросов бот должен ответить?',
                             reply_markup=mark.how_ques)


        elif message.text in ['До 10 вопросов', 'От 10 до 20', 'Более 20']:
            bot.send_message(message.chat.id, 'У бота должен быть дополнительный функционал? '
                                              'Например сохранение или обработка данных?',
                             reply_markup=mark.any_func)


        elif message.text in ['Будут доп. функции', 'Нет сложных функций']:
            bot.send_message(message.chat.id, 'Благодарим за опрос, Ваша предварительная стоимость 1800 рублей.'
                                              '\nЦена может меняться в зависимости от сложности Бота',
                             reply_markup=mark.back_menu)
            get_info_user(bot, message)

        elif message.text == 'Назад':
            img = open('title.jpg', 'rb')
            bot.send_photo(message.chat.id, img)
            bot.send_message(message.chat.id, intro_text,
                             reply_markup=mark.main_menu)
        else:
            bot.send_message(message.chat.id, 'Я Вас не понял =(')

    while True:  # функция для пулинга
        print('=^.^=')

        try:
            bot.polling(none_stop=True, interval=3, timeout=20)
            print('Этого не должно быть')
        except telebot.apihelper.ApiException:
            print('Проверьте связь и API')
            time.sleep(10)
        except Exception as e:
            print(e)
            time.sleep(60)


if __name__ == '__main__':
    run_bot()
