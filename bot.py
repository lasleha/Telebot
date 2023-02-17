import telebot
from telebot import types
import sql

bot_token = '6131879353:AAGKP8nmK-6kksTxJWtymxCBgIWCIihOchs'

bot = telebot.TeleBot(bot_token)

info = dict()


@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    my_id_button = types.KeyboardButton('Мой id')
    favorites_button = types.KeyboardButton('Избранное')
    help_button = types.KeyboardButton('Техподдержка')
    markup.add(my_id_button, favorites_button, help_button)
    bot.send_message(message.from_user.id, "👋 Привет! Я твой бот-помощник!", reply_markup=markup)


def gen_markup():
    markup = types.InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(types.InlineKeyboardButton("🠔", callback_data="cb_left"),
               types.InlineKeyboardButton("🠖", callback_data="cb_right"))
    return markup


def create_caption(co):

    address = ""

    if co['address'] is not None:
        address += co['address']

    if co['stage'] is not None:
        address += f", этаж {co['stage']}"

    if co['number'] is not None:
        address += f", квартира {co['number']}"

    if co['usage'] == 0:
        usage = "Жилое"
    else:
        usage = "Коммерческое"

    if co['type'] == 0:
        co_type = "Здание"
    else:
        co_type = "Участок"

    if co['are_ready']:
        ready = "Введён в эксплуатацию"
    else:
        ready = "Не введён в эксплуатацию"

    caption = f"Адрес: {address}\n" \
              f"Площадь: {co['area']}\n" \
              f"Применение: {usage}\n" \
              f"Тип: {co_type}\n" \
              f"Готовность: {ready}\n" \
              f"Цена: {co['price']}\n" \
              f"Перспективность: {co['perspective']}\n" \
              f"Риск: {co['risk']}\n"

    return caption


@bot.message_handler(content_types=['text'])
def get_text_messages(message):

    chat_id = message.chat.id

    match message.text:

        case 'Мой id':
            bot.send_message(chat_id, f'Ваш id: {chat_id}')

        case 'Избранное':
            if sql.check_usr(chat_id):

                info = sql.favorite(chat_id)

                if len(info) != 0:

                    caption = create_caption(info[0])

                    bot.send_photo(chat_id=chat_id,
                                   caption=f'1 из {len(info)}\n{caption}',
                                   photo=open(info[0]['image'], "rb"),
                                   reply_markup=gen_markup())

        case 'Техподдержка':
            bot.send_message(chat_id, 'Ожидайте оператора')
            # Вызов оператора технической поддержки

        case _:
            bot.send_message(chat_id, 'Извините, запрос не распознан')


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):

    i = int(call.message.caption[:call.message.caption.find(' ')])

    if call.data == "cb_left":

        if i != 1:
            i -= 1

        caption = create_caption(info[i])

        bot.edit_message_media(chat_id=call.message.chat.id, message_id=call.message.message_id,
                               media=types.InputMediaPhoto(open(info[i - 1]['image'], "rb")), reply_markup=gen_markup())

        bot.edit_message_caption(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                 caption=f'{i}/{len(info)}\n{caption}', reply_markup=gen_markup())

    elif call.data == "cb_right":

        if i != len(info):
            i += 1

        caption = create_caption(info[i])

        bot.edit_message_media(chat_id=call.message.chat.id, message_id=call.message.message_id,
                               media=types.InputMediaPhoto(open(info[i - 1]['image'], "rb")), reply_markup=gen_markup())

        bot.edit_message_caption(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                 caption=f'{i}/{len(info)}\n{caption}', reply_markup=gen_markup())


if __name__ == '__main__':
    bot.polling(none_stop=True, interval=0)
