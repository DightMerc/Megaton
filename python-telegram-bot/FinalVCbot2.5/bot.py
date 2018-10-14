# -*- coding: utf-8 -*-
import logging
import sqlite3
from config import *
from telegram.ext import Updater, CommandHandler, MessageHandler, CallbackQueryHandler, Filters
from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from transitions import Machine

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

updater = Updater(token)


class MainFunc(object):

    def __init__(self):
        """Машина состояний и переменные"""
        self.msg_user = None

        self.states = ['await', 'enter']

        self.status = None

        self.machine = Machine(model=self, states=self.states, initial='await')

        self.machine.add_transition(trigger='state_enter', source='await', dest='enter', before='fun_enter')

        self.machine.add_transition(trigger='msg_from_user', source='enter', dest='enter', before='msg_enter')

        self.machine.add_transition(trigger='send_to_await', source='enter', dest='await', before='send_msg')

    def fun_enter(self, bot, update):
        query = update.callback_query

        if query['from_user']['id'] == admin_id:
            bot.send_message(chat_id=query.message.chat_id, text='Жду вашего сообщения')
            self.status = query['data']
        else:
            bot.edit_message_text(chat_id=query.message.chat_id, message_id=query.message.message_id,
                                  text='У вас нет прав')

    def msg_enter(self, bot, update):
        accept_key = [[InlineKeyboardButton("✅", callback_data='accept')]]

        bot.send_message(chat_id=update.message.chat_id,
                         text='Подтвердить',
                         reply_markup=InlineKeyboardMarkup(accept_key))

        self.msg_user = update.message.text

    def send_msg(self, bot, update):
        query = update.callback_query

        if query['from_user']['id'] == admin_id:
            if self.status == 'all':
                connect = sqlite3.connect('database/groupid.db3')
                cursor = connect.cursor()
                cursor.execute("SELECT group_id FROM gropuid")
                results = cursor.fetchall()

                for i in results:
                    for k in i:
                        bot.send_message(chat_id=k, text=self.msg_user)

                bot.send_message(chat_id=query.message.chat_id, text='Отправленно', parse_mode='HTML')

                self.msg_user = None

            else:
                bot.send_message(chat_id=self.status, text=self.msg_user)

        else:
            bot.send_message(chat_id=query.message.chat_id, text='У вас нет прав')

obj_class = MainFunc()


def start_bot(bot, update):
    """Проверка на админа и добавление id группы в БД"""
    update_msg = update.message
    if update_msg['chat']['type'] == 'supergroup' or update_msg['chat']['type'] == 'group':
        if update_msg['from_user']['id'] == admin_id:
            connect = sqlite3.connect('database/groupid.db3')
            cursor = connect.cursor()
            cursor.execute("SELECT group_id FROM gropuid")
            results = cursor.fetchall()
            transit = []

            for i in results:
                for k in i:
                    transit.append(k)

            if update_msg['chat']['id'] in transit:
                bot.send_message(chat_id=update_msg.chat_id, text='Группа уже добавлена')
            else:
                cursor.execute("INSERT INTO gropuid (group_id, group_name) VALUES (?, ?)",
                               (update_msg['chat']['id'], update_msg['chat']['title']))
                connect.commit()
                bot.send_message(chat_id=update_msg.chat_id, text='Группа добавлена')
            cursor.close()
            connect.close()
        else:
            bot.send_message(chat_id=update_msg.chat_id, text='У вас нет прав!')
    else:
        bot.send_message(chat_id=update_msg.chat_id, text='Вы не в групповом чате')


def send_bot(bot, update):
    """Проверка на админа и интерфейс для ввода"""
    update_msg = update.message
    if update_msg['chat']['type'] == 'private':
        if update_msg['from_user']['id'] == admin_id:
            connect = sqlite3.connect('database/groupid.db3')
            cursor = connect.cursor()
            cursor.execute("SELECT group_id, group_name FROM gropuid")
            results = cursor.fetchall()
            cursor.close()
            connect.close()

            transit_id = []
            transit_name = []

            for i in results:
                transit_id.append(i[0])
                transit_name.append(i[1])

            key = [[InlineKeyboardButton(label, callback_data=data)] for label, data in zip(transit_name, transit_id)]

            bot.send_message(chat_id=update_msg.chat_id,
                             text="Выберете группу",
                             reply_markup=InlineKeyboardMarkup(key))

            key_all = [[InlineKeyboardButton('Во все группы', callback_data='all')]]

            bot.send_message(chat_id=update_msg.chat_id,
                             text="Или отправить всем?",
                             reply_markup=InlineKeyboardMarkup(key_all))

            for i in transit_id:
                updater.dispatcher.add_handler(CallbackQueryHandler(obj_class.state_enter, pattern=str(i)))

        else:
            bot.send_message(chat_id=update_msg.chat_id, text='У вас нет прав!')
    else:
        bot.send_message(chat_id=update_msg.chat_id, text='Перейдите в личку бота')


def start(bot, update):
    update_msg = update.message
    bot.send_message(chat_id=update_msg.chat_id, text='''Добавить группу в базу данных командой /get
Отправить сообщение в группу(ы) /send''')

updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(CommandHandler('get', start_bot))
updater.dispatcher.add_handler(CommandHandler('send', send_bot))

updater.dispatcher.add_handler(CallbackQueryHandler(obj_class.state_enter, pattern='all'))
updater.dispatcher.add_handler(CallbackQueryHandler(obj_class.send_to_await, pattern='accept'))
updater.dispatcher.add_handler(MessageHandler(Filters.text, obj_class.msg_from_user))


updater.start_polling(poll_interval=1.0, timeout=20)
updater.idle()
