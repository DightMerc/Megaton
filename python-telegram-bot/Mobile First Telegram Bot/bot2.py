#!/usr/bin/env python
# -*- coding: utf-8 -*-


from telegram import ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup,ParseMode
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, RegexHandler,
                          ConversationHandler, CallbackQueryHandler)

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

    file = open(os.getcwd()+"\\users\\" + str(update.message.from_user.id) + ".txt", "a")
    file.close()

    lan_reply_keyboard = [['Русский язык', 'O`zbek tili']]
    markup = ReplyKeyboardMarkup(lan_reply_keyboard, one_time_keyboard=True, resize_keyboard=True)

    bot.send_photo(update.message.from_user.id, photo=open('logo.jpg', 'rb'))
    bot.sendMessage(update.message.from_user.id, "Добро пожаловать, "+ update.message.from_user.first_name + "! Вас приветсвует Бот компании Mobile First")

    update.message.reply_text(
      "Пожалуйста, выберите язык для дальнейшего взаимодействия",
        reply_markup=markup)
    return CHOOSING


def categories(bot, update, user_data):
    language_set(bot, update, user_data)
    lan_reply_keyboard = [['Разработка', 'Дизайн'],['Маркетинг', 'IT-Consulting']]
    markup = ReplyKeyboardMarkup(lan_reply_keyboard, one_time_keyboard=True, resize_keyboard=True)

    language_set(bot, update, user_data)
    update.message.reply_text(
      "Выберите категорию",
        reply_markup=markup)
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

    return lan

def restart_in_diff_lan(bot, update, user_data):
    language_set(bot, update, user_data)
    bot.sendMessage(update.message.from_user.id, "Добро пожаловать, "+ update.message.from_user.first_name + "! Вас приветсвует Бот компании Mobile First")
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
    if (update.message.text == "Разработка" or update.message.text == "Dasturlash"):
        keyboard = [[InlineKeyboardButton("Мобильные приложения", callback_data='1'),
                 InlineKeyboardButton("Сайты", callback_data='2')],

                [InlineKeyboardButton("Telegram боты", callback_data='3')]]

        reply_markup = InlineKeyboardMarkup(keyboard)

        update.message.reply_text('Услуги разработки:', reply_markup=reply_markup)
    if (update.message.text == "Дизайн" or update.message.text == "Dizayn"):
        keyboard = [[InlineKeyboardButton("Логотипы", callback_data='4'),
                 InlineKeyboardButton("Фирменный стиль", callback_data='5')],

                [InlineKeyboardButton("WEB-дизайн", callback_data='6')]]

        reply_markup = InlineKeyboardMarkup(keyboard)
        update.message.reply_text('Дизайн услуги:', reply_markup=reply_markup)
    if (update.message.text == "Маркетинг" or update.message.text == "Marketing"):
        keyboard = [[InlineKeyboardButton("Social Media Marketing(SMM)", callback_data='7'),
                 InlineKeyboardButton("Mobile Media Marketing(MMM)", callback_data='8')],

                [InlineKeyboardButton("Search Engine Optimization(SEO)", callback_data='9')]]

        reply_markup = InlineKeyboardMarkup(keyboard)
        update.message.reply_text('Сетевой Маркетинг:', reply_markup=reply_markup)
    if (update.message.text == "IT-Consulting"):
        keyboard = [[InlineKeyboardButton("Консультирование в сфере ИКТ", callback_data='10'),
                 InlineKeyboardButton("Продвижение ИКТ-проектов", callback_data='11')],

                [InlineKeyboardButton("Аутсорсинг", callback_data='12')]]

        reply_markup = InlineKeyboardMarkup(keyboard)
        update.message.reply_text('Дизайн услуги:', reply_markup=reply_markup)

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

def changeState(bot, chat_id, user_data, newState):
    with open(os.getcwd()+"\\users\\" + str(chat_id) + ".txt") as file:
                array = [row.strip() for row in file]
                file.close()
    current_lan = array[0]
    file = open(os.getcwd()+"\\users\\" + str(chat_id) + ".txt", "w")
    file.write(current_lan + "\n")
    file.write(newState+"\n")
    file.close()

def InlineKeyboardHandler(bot, update, user_data):
    query = update.callback_query
    id = query.message.chat_id
    if query.data == "1":

        changeState(bot, id, user_data,"mobile")

        lan_reply_keyboard = [['Сделать заказ', 'Портфолио'],['Назад']]
        markup = ReplyKeyboardMarkup(lan_reply_keyboard, one_time_keyboard=True, resize_keyboard=True)
        bot.send_photo(query.message.chat_id, photo=open('mobile.jpeg', 'rb'))
        bot.delete_message(chat_id=query.message.chat_id,
        message_id=query.message.message_id)
        bot.sendMessage(query.message.chat_id,"*Мобильные приложения* – это _долгосрочные_ инвестиции.\nНельзя забывать о том, что этот рынок активно _растет_, и тем компаниям, которые смогут занять свою нишу и закрепиться на нем, стать _лидерами_ будет намного легче.", reply_markup=markup ,parse_mode=ParseMode.MARKDOWN)
        
        return CHOOSING
    if query.data == "2":

        changeState(bot, id, user_data,"sites")

        lan_reply_keyboard = [['Сделать заказ', 'Портфолио'],['Назад']]
        markup = ReplyKeyboardMarkup(lan_reply_keyboard, one_time_keyboard=True, resize_keyboard=True)
        bot.send_photo(query.message.chat_id, photo=open('sites.jpg', 'rb'))
        bot.delete_message(chat_id=query.message.chat_id,
        message_id=query.message.message_id)
        bot.sendMessage(query.message.chat_id,"*Веб сайт* - это уникальная _возможность_ не только заявить о себе на бескрайних просторах Интернета, но и инструмент, способный приносить _прибыль_.", reply_markup=markup ,parse_mode=ParseMode.MARKDOWN)
        return CHOOSING
    if query.data == "3":

        changeState(bot, id, user_data,"bots")

        lan_reply_keyboard = [['Сделать заказ', 'Портфолио'],['Назад']]
        markup = ReplyKeyboardMarkup(lan_reply_keyboard, one_time_keyboard=True, resize_keyboard=True)
        bot.send_photo(query.message.chat_id, photo=open('telegram.jpeg', 'rb'))
        bot.delete_message(chat_id=query.message.chat_id,
        message_id=query.message.message_id)
        bot.sendMessage(query.message.chat_id,"Telegram набирает популярность с рекордной скоростью. *Telegram Bot* - поможет Вам завоевать и развить новую платформу для бизнеса, найти свою целевую аудиторию и распространить информацию о Вас.", reply_markup=markup ,parse_mode=ParseMode.MARKDOWN)
        return CHOOSING
    if query.data == "4":

        changeState(bot, id, user_data,"logos")

        lan_reply_keyboard = [['Сделать заказ', 'Портфолио'],['Назад']]
        markup = ReplyKeyboardMarkup(lan_reply_keyboard, one_time_keyboard=True, resize_keyboard=True)
        bot.send_photo(query.message.chat_id, photo=open('logotype.jpg', 'rb'))
        bot.delete_message(chat_id=query.message.chat_id,
        message_id=query.message.message_id)
        bot.sendMessage(query.message.chat_id,"*Логотип* – это _лицо_ Вашей компании.\nА хорошо _продуманный_ и стильный_ логотип - красный флаг для Ваших клиентов.", reply_markup=markup ,parse_mode=ParseMode.MARKDOWN)
        return CHOOSING
    if query.data == "5":

        changeState(bot, id, user_data,"selfStyle")

        lan_reply_keyboard = [['Сделать заказ', 'Портфолио'],['Назад']]
        markup = ReplyKeyboardMarkup(lan_reply_keyboard, one_time_keyboard=True, resize_keyboard=True)
        bot.send_photo(query.message.chat_id, photo=open('selfStyle.jpeg', 'rb'))
        bot.delete_message(chat_id=query.message.chat_id,
        message_id=query.message.message_id)
        bot.sendMessage(query.message.chat_id,"*Фирменный стиль* – это Ваше _все_.\nФирменный стиль является одним из _главных_ средств борьбы за _покупателя_. Помните - встречают по одежке.", reply_markup=markup ,parse_mode=ParseMode.MARKDOWN)
        return CHOOSING
    if query.data == "6":

        changeState(bot, id, user_data,"webDesign")

        lan_reply_keyboard = [['Сделать заказ', 'Портфолио'],['Назад']]
        markup = ReplyKeyboardMarkup(lan_reply_keyboard, one_time_keyboard=True, resize_keyboard=True)
        bot.send_photo(query.message.chat_id, photo=open('webdesign.jpg', 'rb'))
        bot.delete_message(chat_id=query.message.chat_id,
        message_id=query.message.message_id)
        bot.sendMessage(query.message.chat_id,"*Веб-дизайн* – это графическое оформление. Это то, как люди увидят Ваш _сайт_.", reply_markup=markup ,parse_mode=ParseMode.MARKDOWN)
        return CHOOSING
    if query.data == "7":

        changeState(bot, id, user_data,"marketing")

        lan_reply_keyboard = [['Сделать заказ', 'Портфолио'],['Назад']]
        markup = ReplyKeyboardMarkup(lan_reply_keyboard, one_time_keyboard=True, resize_keyboard=True)
        bot.send_photo(query.message.chat_id, photo=open('mobile.jpeg', 'rb'))
        bot.delete_message(chat_id=query.message.chat_id,
        message_id=query.message.message_id)
        bot.sendMessage(query.message.chat_id,"*Социальные сети* давно перестали быть местом только для общения. Это площадка по привлечению _клиентов_. Настало время раскрутиться в _сети_.", reply_markup=markup ,parse_mode=ParseMode.MARKDOWN)
        return CHOOSING
    if query.data == "8":

        changeState(bot, id, user_data,"smm")

        lan_reply_keyboard = [['Сделать заказ', 'Портфолио'],['Назад']]
        markup = ReplyKeyboardMarkup(lan_reply_keyboard, one_time_keyboard=True, resize_keyboard=True)
        bot.send_photo(query.message.chat_id, photo=open('mobile.jpeg', 'rb'))
        bot.delete_message(chat_id=query.message.chat_id,
        message_id=query.message.message_id)
        bot.sendMessage(query.message.chat_id,"*Мобильные приложения* – это _долгосрочные_ инвестиции.\nНельзя забывать о том, что этот рынок активно _растет_, и тем компаниям, которые смогут занять свою нишу и закрепиться на нем, стать _лидерами_ будет намного легче.", reply_markup=markup ,parse_mode=ParseMode.MARKDOWN)
        return CHOOSING
    if query.data == "9":

        changeState(bot, id, user_data,"mmm")

        lan_reply_keyboard = [['Сделать заказ', 'Портфолио'],['Назад']]
        markup = ReplyKeyboardMarkup(lan_reply_keyboard, one_time_keyboard=True, resize_keyboard=True)
        bot.send_photo(query.message.chat_id, photo=open('mobile.jpeg', 'rb'))
        bot.delete_message(chat_id=query.message.chat_id,
        message_id=query.message.message_id)
        bot.sendMessage(query.message.chat_id,"*Мобильные приложения* – это _долгосрочные_ инвестиции.\nНельзя забывать о том, что этот рынок активно _растет_, и тем компаниям, которые смогут занять свою нишу и закрепиться на нем, стать _лидерами_ будет намного легче.", reply_markup=markup ,parse_mode=ParseMode.MARKDOWN)
        return CHOOSING
    if query.data == "10":

        changeState(bot, id, user_data,"seo")

        lan_reply_keyboard = [['Сделать заказ', 'Портфолио'],['Назад']]
        markup = ReplyKeyboardMarkup(lan_reply_keyboard, one_time_keyboard=True, resize_keyboard=True)
        bot.send_photo(query.message.chat_id, photo=open('mobile.jpeg', 'rb'))
        bot.delete_message(chat_id=query.message.chat_id,
        message_id=query.message.message_id)
        bot.sendMessage(query.message.chat_id,"*Мобильные приложения* – это _долгосрочные_ инвестиции.\nНельзя забывать о том, что этот рынок активно _растет_, и тем компаниям, которые смогут занять свою нишу и закрепиться на нем, стать _лидерами_ будет намного легче.", reply_markup=markup ,parse_mode=ParseMode.MARKDOWN)
        return CHOOSING
    if query.data == "11":

        changeState(bot, id, user_data,"projectUp")

        lan_reply_keyboard = [['Сделать заказ', 'Портфолио'],['Назад']]
        markup = ReplyKeyboardMarkup(lan_reply_keyboard, one_time_keyboard=True, resize_keyboard=True)
        bot.send_photo(query.message.chat_id, photo=open('mobile.jpeg', 'rb'))
        bot.delete_message(chat_id=query.message.chat_id,
        message_id=query.message.message_id)
        bot.sendMessage(query.message.chat_id,"*Мобильные приложения* – это _долгосрочные_ инвестиции.\nНельзя забывать о том, что этот рынок активно _растет_, и тем компаниям, которые смогут занять свою нишу и закрепиться на нем, стать _лидерами_ будет намного легче.", reply_markup=markup ,parse_mode=ParseMode.MARKDOWN)
        return CHOOSING
    if query.data == "12":

        changeState(bot, id, user_data,"outsorsing")

        lan_reply_keyboard = [['Сделать заказ', 'Портфолио'],['Назад']]
        markup = ReplyKeyboardMarkup(lan_reply_keyboard, one_time_keyboard=True, resize_keyboard=True)
        bot.send_photo(query.message.chat_id, photo=open('mobile.jpeg', 'rb'))
        bot.delete_message(chat_id=query.message.chat_id,
        message_id=query.message.message_id)
        bot.sendMessage(query.message.chat_id,"*Мобильные приложения* – это _долгосрочные_ инвестиции.\nНельзя забывать о том, что этот рынок активно _растет_, и тем компаниям, которые смогут занять свою нишу и закрепиться на нем, стать _лидерами_ будет намного легче.", reply_markup=markup ,parse_mode=ParseMode.MARKDOWN)
        return CHOOSING

    return CHOOSING

def buy(bot, update, user_data):
    bot.sendMessage(update.message.chat_id,"Для того, чтобы сделать заказ вам нужно связаться с нашими представителями.\n\nP+998901234567\n@dight")

Administration = []

#Получение списка администрации
def GetAdministartion():
    print("Getting list of Administration")
    with open(os.getcwd()+"\\admin") as file:
            Administration = [row.strip() for row in file]
            file.close()

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
                       RegexHandler('^(Разработка|Дизайн|Маркетинг|IT-Consulting)$',
                                    category_set,
                                    pass_user_data=True),
                       RegexHandler('^Назад$',
                                    categories,
                                    pass_user_data=True),
                       RegexHandler('^Сделать заказ$',
                                    buy,
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

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.


if __name__ == '__main__':
    main()
