import telebot
from telebot import types
import threading
import sql

bot_token = '6131879353:AAGKP8nmK-6kksTxJWtymxCBgIWCIihOchs'

bot = telebot.TeleBot(bot_token)

photos = [
    r'C:\Users\to_se\OneDrive\Изображения\GameCenter\AtomicHeart\AtomicHeart_sample.jpg',
    r'C:\Users\to_se\OneDrive\Изображения\GameCenter\LostArk\LostArk_sample.jpg'
]


@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    my_id_button = types.KeyboardButton('Мой id')
    favorites_button = types.KeyboardButton('Избранное')
    markup.add(my_id_button, favorites_button)
    bot.send_message(message.from_user.id, "👋 Привет! Я твой бот-помощник!", reply_markup=markup)


def gen_markup():
    markup = types.InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(types.InlineKeyboardButton("🠔", callback_data="cb_left"),
               types.InlineKeyboardButton("🠖", callback_data="cb_right"))
    return markup


@bot.message_handler(content_types=['text'])
def get_text_messages(message):

    if message.text == 'Мой id':
        bot.send_message(message.from_user.id, f'Ваш id: {message.from_user.id}')

    elif message.text == 'Избранное':
        if sql.CheckUsr():
            bot.send_photo(chat_id=message.chat.id,
                           caption=f'1/{len(photos)}',
                           photo=open(photos[0], "rb"),
                           reply_markup=gen_markup())

    else:
        bot.send_message(message.from_user.id, 'Извините, запрос не распознан')


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):

    i = int(call.message.caption[0])

    if call.data == "cb_left":

        if i != 1:
            i -= 1

        bot.edit_message_media(chat_id=call.message.chat.id, message_id=call.message.message_id,
                               media=types.InputMediaPhoto(open(photos[i - 1], "rb")), reply_markup=gen_markup())

        bot.edit_message_caption(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                 caption=f'{i}/{len(photos)}', reply_markup=gen_markup())

    elif call.data == "cb_right":

        if i != len(photos):
            i += 1

        bot.edit_message_media(chat_id=call.message.chat.id, message_id=call.message.message_id,
                               media=types.InputMediaPhoto(open(photos[i - 1], "rb")), reply_markup=gen_markup())

        bot.edit_message_caption(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                 caption=f'{i}/{len(photos)}', reply_markup=gen_markup())


if __name__ == '__main__':
    bot.polling(none_stop=True, interval=0)
