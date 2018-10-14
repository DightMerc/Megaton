#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Basic example for a bot that uses inline keyboards.
# This program is dedicated to the public domain under the CC0 license.
"""
import logging

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, ConversationHandler, RegexHandler, MessageHandler, Filters
import os

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)
CHOOSING, TYPING_REPLY = range(2)



def start(bot, update, user_data):
    GetAdministartion()
    if str(update.message.from_user.id) in Administration:

        keyboard = [[InlineKeyboardButton("Отправить сообщение", callback_data='message_send')]]
        reply_markup = InlineKeyboardMarkup(keyboard)

        update.message.reply_text('Выберите действие:', reply_markup=reply_markup)




"""
Динамическая прогрузка INLINE кнопок
"""

def loadingInline():
    groups = []
    with open(os.getcwd()+"\\groups") as file:
        groups = [row.strip() for row in file]
        file.close()

    group_name = []
    with open(os.getcwd()+"\\group_names") as file:
        group_name = [row.strip() for row in file]
        file.close()

    inline = []
    subinline = []

    i=0
    b=1
    while i<len(groups):



"""
Сколько кнопок будет в одной линии. B=3 - три кнопки
"""


        if b == 3:
            My_InlineButton = InlineKeyboardButton(text=str(group_name[i]), callback_data=str(groups[i]))
            subinline.append(My_InlineButton)
            inline.append(subinline)
            subinline = []
            i=i+1
            b=1
        else:
            My_InlineButton = InlineKeyboardButton(text=str(group_name[i]), callback_data=str(groups[i]))
            subinline.append(My_InlineButton)
            i=i+1
            b=b+1
            if i==len(groups):
                inline.append(subinline)
    
    return inline





"""
Обработчик INLINE кнопок
"""




def InlineKeyboardHandler(bot, update, user_data):
"""
Считывание групп из файла
"""
    groups = []
    with open(os.getcwd()+"\\groups") as file:
        groups = [row.strip() for row in file]
        file.close()

"""
Если пользователь администратор, дать ему права
"""

    if str(update.callback_query.from_user.id) in Administration:
        query = update.callback_query

        if query.data == "1":
            with open(os.getcwd()+"\\groups") as file:
                groups = [row.strip() for row in file]
                file.close()

                i=0
                while i<len(groups):
                    bot.sendMessage(groups[i],"Under Construction")
                    i=i+1



        if query.data == "2":
            reLoadGroupName(bot)
            keyboard = loadingInline()
            reply_markup = InlineKeyboardMarkup(keyboard)
            bot.sendMessage(update.callback_query.message.chat.id,'Выберите группу:', reply_markup=reply_markup)
            file = open(os.getcwd()+"\\toSend", "w")
            file.close()


            
"""
Обновление имен групп для отображения на INLINE кнопках
"""

        if query.data == "3":
            reLoadGroupName(bot)



"""
Обработка прихода информации с динамических INLINE кнопок
Проверка, есть ли такие группы в списке групп. Если даю То добавить в файл отправки

Надо сделать изменение сообщение на удаление лишних кнопок
"""
        if query.data in groups:
            with open(os.getcwd()+"\\toSend") as file:
                send = [row.strip() for row in file]
                file.close()
            if query.data in send:
                print()
            else:
                file = open(os.getcwd()+"\\toSend", "a")
                file.write(query.data+"\n")
                file.close()

"""
Обработка вводимого текста
"""
        if query.data == "message_send":
            bot.sendMessage(update.callback_query.message.chat.id,'Введите сообщение:')
            print("typing")
            return TYPING_REPLY

"""
Отправка текста
"""
        if query.data == "SendText":
            SendTo(bot, update, user_data)
        return CHOOSING


"""
Выбор способа отправки
"""
def SendTo(bot, update, user_data):
    keyboard = [[InlineKeyboardButton("Отправить во все группы", callback_data='1'),
                     InlineKeyboardButton("Отправить выборочно", callback_data='2')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
            
    bot.sendMessage(update.message.chat.id,'Выберите действие:', reply_markup=reply_markup)




"""
Лишнее
"""
def help(update):
    update.message.reply_text("Use /start to test this bot.")



"""
Приём текстовой информации. НЕ РАБОТАЕТ!
"""
def received_information(bot, update, user_data):
    print("received")
    res = update.message.text


    keyboard = [[InlineKeyboardButton("Отменить отправку", callback_data='cancel_send'),
                     InlineKeyboardButton("Редактировать", callback_data='edit_text')],
                    [InlineKeyboardButton("Отправить", callback_data="SendText")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
            
    bot.sendMessage(update.message.from_user.id, "Отправить сообщение?")
    bot.sendMessage(update.message.from_user.id, res, reply_markup=reply_markup)


    return CHOOSING






"""
Лишнее
"""
def done(bot, update, user_data):
    if 'choice' in user_data:
        del user_data['choice']

    update.message.reply_text("I learned these facts about you:"
                              "{}"
                              "Until next time!".format(facts_to_str(user_data)))

    user_data.clear()
    return ConversationHandler.END





"""
Обработчик ошибок
"""

def error(bot,update, user_data):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)





"""
Массив с администраторами. Глобальная переменная. Прогружается один раз
"""
Administration = []





"""
Получение списка администраторов
"""
def GetAdministartion():
    global Administration
    with open(os.getcwd()+"\\admin") as file:
            Administration = [row.strip() for row in file]
            file.close()




"""
Получение АЙДИ групп
"""
def idgroup(bot, update):
    with open(os.getcwd()+"\\groups") as file:
            groups = [row.strip() for row in file]
            file.close()
    if update.message.chat_id in groups:
        print()
    else:
        file = open(os.getcwd()+"\\groups", "a")
        file.write(str(update.message.chat_id) +"\n")
        file.close()




"""
Получение названия групп для INLINE кнопок
"""
def reLoadGroupName(bot):
    with open(os.getcwd()+"\\groups") as file:
            groups = [row.strip() for row in file]
            file.close()
    i=0
    file = open(os.getcwd()+"\\group_names", "w")
    file.close

    while i< len(groups):
        res = bot.sendMessage(groups[i], "Check name")
        file = open(os.getcwd()+"\\group_names", "ab")
        data = res.chat.title + "\n"
        data = bytes(data, "utf-8")
        file.write(data)
        file.close()


        """
        Отсылка пробного сообщения и моментальное удаление, для получения названия группы.
        """
        bot.deleteMessage(res.chat.id, res.message_id)
        i=i+1


    

def main():
    # Create the Updater and pass it your bot's token.
    updater = Updater("364316825:AAEc5rhaEQx1-VJ4Jt6SxOUDyro9sKWz2Bo")

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start, pass_user_data=True)],
        
        states={
            CHOOSING: [RegexHandler('_',
                                    start,
                                    pass_user_data=True),
                       ],

            TYPING_REPLY: [MessageHandler(Filters.text,
                                          received_information,
                                          pass_user_data=True)
                           ],
        },

        fallbacks=[RegexHandler('^Done$', done, pass_user_data=True)]
    )


    dp.add_handler(conv_handler)

    # log all errors
    dp.add_error_handler(error)
    dp.add_handler(CallbackQueryHandler(InlineKeyboardHandler,pass_user_data=True))
    dp.add_handler(CommandHandler('idgroup', idgroup))
    dp.add_handler(CommandHandler('start', start, pass_user_data=True))



    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.


if __name__ == '__main__':
    main()