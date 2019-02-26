from io import BytesIO
import requests
from telegram_token import token
from model1 import *
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from PIL import Image
import information


def __main__():
    updater = Updater(token=token)  # Токен API к Telegram
    dispatcher = updater.dispatcher
    classes = ['картина', 'гравюра', 'икона', 'скульптура', 'рисунок']

    # Обработка команд
    def start_command(bot, update):
        bot.send_message(chat_id=update.message.chat_id, text='Добрый день! Отправьте мне фотографию '
                                                              'произведения искусства, жанр которого вы хотели бы'
                                                              ' узнать')

    def help_command(bot, update):
        bot.send_message(chat_id=update.message.chat_id, text='Меня зовут АртБот, и я умею определять жанр искусства по'
                                                              ' фотографии объекта. Для этого достаточно лишь кинуть'
                                                              ' мне фотографию)')

    def text_message(bot, update):
        info = information.genres
        ans = information.answers
        text = update.message.text.lower()
        understood = False
        answered = False

        for i in classes:
            if i[:4] in text:
                if not answered:
                    understood = True
                    answered = True
                    bot.send_message(chat_id=update.message.chat_id, text=info[i])
                    break

        for i in ans.keys():
            if i in text:
                if not answered:
                    understood = True
                    bot.send_message(chat_id=update.message.chat_id, text=ans[i])
                    break

        if not understood:
            response = 'Я вас не понимаю, повторите еще раз'
            bot.send_message(chat_id=update.message.chat_id, text=response)

    def photo_message(bot, update):
        text = 'На вашей фотографии изображен(а) '
        file_id = update.message.photo[-1].file_id
        file = bot.get_file(file_id)
        url = file.file_path
        img = Image.open(BytesIO(requests.get(url).content))

        predictor = ClassPredictor()
        processed_img = predictor.process_img(img)
        output = predictor.predict(processed_img)

        bot.send_message(chat_id=update.message.chat_id, text=text + output)

    # Хендлеры
    start_command_handler = CommandHandler('start', start_command)

    help_command_handler = CommandHandler('help', help_command)

    text_message_handler = MessageHandler(Filters.text, text_message)

    photo_message_handler = MessageHandler(Filters.photo, photo_message)

    dispatcher.add_handler(start_command_handler)
    dispatcher.add_handler(help_command_handler)
    dispatcher.add_handler(text_message_handler)
    dispatcher.add_handler(photo_message_handler)

    updater.start_polling(clean=True)
    updater.idle()


__main__()
