#!/usr/bin/env python
# -*- coding: utf-8 -*-


from telegram import ReplyKeyboardMarkup
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, RegexHandler,
                          ConversationHandler)

import gettext
import logging
import config
import os


# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

CHOOSING, TYPING_REPLY = range(2)



def start(bot, update,user_data):
#Инициализация языка
    if os.path.exists(os.getcwd()+"\\users"):
        print("Directory USERS is already created")
    else:
        os.mkdir(os.getcwd()+"\\users", 0o777)
        print("Creating USERS directory")

    if  os.path.exists(os.getcwd()+"\\users\\" + str(update.message.from_user.id) + ".txt"):
        with open(os.getcwd()+"\\users\\" + str(update.message.from_user.id) + ".txt") as file:
                  array = [row.strip() for row in file]
                  file.close()
        try:
            if array[0]:
              print("file users is empty")
              restart_in_diff_lan(bot, update, user_data)

        except Exception as e:
            print("file users is empty")

            file = open(os.getcwd()+"\\users\\" + str(update.message.from_user.id) + ".txt", "a")
            file.close()

            lan_reply_keyboard = [['Русский язык', 'O`zbek tili']]
            markup = ReplyKeyboardMarkup(lan_reply_keyboard, one_time_keyboard=True, resize_keyboard=True)

            bot.sendMessage(update.message.from_user.id, "Добро пожаловать, "+ update.message.from_user.first_name + "! Вас приветсвует Бот компании Mobile First")

            update.message.reply_text(
              "Пожалуйста, выберите язык для дальнейшего взаимодействия",
                reply_markup=markup)
            return CHOOSING
            
    else:
        print("new user creating")
        es = gettext.translation('guess', localedir='locale', languages=["ru"])
        es.install()

        file = open(os.getcwd()+"\\users\\" + str(update.message.from_user.id) + ".txt", "a")
        file.close()

        lan_reply_keyboard = [['Русский язык', 'O`zbek tili']]
        markup = ReplyKeyboardMarkup(lan_reply_keyboard, one_time_keyboard=True, resize_keyboard=True)

        es = gettext.translation('guess', localedir='locale', languages=["ru"])
        es.install()
        bot.sendMessage(update.message.from_user.id, "Добро пожаловать, "+ update.message.from_user.first_name + "! Вас приветсвует Бот компании Mobile First")

        es = gettext.translation('guess', localedir='locale', languages=["ru"])
        es.install()
        update.message.reply_text(
          "Пожалуйста, выберите язык для дальнейшего взаимодействия",
            reply_markup=markup)

        return CHOOSING


def categories(bot, update, user_data):
    language_set(bot, update, user_data)
    lan_reply_keyboard = [[_('Разработка'), _('Дизайн')],[_('Маркетинг'), _('IT-Consulting')]]
    markup = ReplyKeyboardMarkup(lan_reply_keyboard, one_time_keyboard=True, resize_keyboard=True)

    language_set(bot, update, user_data)
    update.message.reply_text(
      _("Выберите категорию"),
        reply_markup=markup)
    print("return choosing")
    return CHOOSING

def language_set(bot, update, user_data):

    with open(os.getcwd()+"\\users\\" + str(update.message.from_user.id) + ".txt") as file:
                array = [row.strip() for row in file]
                file.close()

    current_lan = array[0]

    if current_lan=="ru":
      lan = "ru"
    elif current_lan=="uz":
      lan = "uz"
    elif current_lan=="en":
      lan= "en"
    else:
      lan = "ru"
    es = gettext.translation('guess', localedir='locale', languages=[lan])
    es.install()

def restart_in_diff_lan(bot, update, user_data):
    language_set(bot, update, user_data)
    bot.sendMessage(update.message.from_user.id, _("Добро пожаловать, ")+ update.message.from_user.first_name + _("! Вас приветсвует Бот компании Mobile First"))
    categories(bot, update, user_data)

def lan_detected(bot, update, user_data):
    print("detecting language")
    selected_lan = update.message.text
    if selected_lan == "Русский язык":
      current_lan = "ru"
    elif selected_lan =="O`zbek tili":
      current_lan = "uz"
    else: 
      current_lan = "en"

    file = open(os.getcwd()+"\\users\\" + str(update.message.from_user.id) + ".txt", "w")
    file.write(current_lan + "\n")
    file.close()
    print("Language was set: " + current_lan)

    if current_lan != "ru":
      restart_in_diff_lan(bot, update, user_data)
    else:
      categories(bot, update, user_data)

    return CHOOSING


def category_set(bot, update, user_data):
    print("Разработка")
    return CHOOSING



def received_information(bot, update, user_data):
    text = update.message.text
    category = user_data['choice']
    user_data[category] = text
    del user_data['choice']
    update.message.reply_text("Neat! Just so you know, this is what you already told me:"
                              "{}"
                              "You can tell me more, or change your opinion on something.".format(
                                  facts_to_str(user_data)), reply_markup=markup)

    return CHOOSING


def done(bot, update, user_data):
    if 'choice' in user_data:
        del user_data['choice']

    update.message.reply_text("I learned these facts about you:"
                              "{}"
                              "Until next time!".format(facts_to_str(user_data)))

    user_data.clear()
    return ConversationHandler.END


def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)

    


def main():
    # Create the Updater and pass it your bot's token.
    updater = Updater(config.token)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start, pass_user_data=True)],
        
        states={
            CHOOSING: [RegexHandler('^(Русский язык|O`zbek tili)$',
                                    lan_detected,
                                    pass_user_data=True),
                       RegexHandler('^(Разработка|Dasturlash)$',
                                    category_set,
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

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.


if __name__ == '__main__':
    main()
