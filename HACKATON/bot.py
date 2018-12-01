#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

from telegram import ReplyKeyboardMarkup
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, RegexHandler,
                          ConversationHandler, CallbackQueryHandler)

import telegram

import logging

import config

import datetime

import os

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)



def start(bot, update):
	NONE = ""

	recieved_text = update.message.text
	user = update.message.from_user.id

	if not os.path.exists(os.getcwd()+"\\Users\\"+str(user)):
		os.makedirs(os.getcwd()+"\\Users\\"+str(user))

	
	if os.path.exists(os.getcwd()+"\\Users\\"+str(user)+"\\phone_number"):

		text = "Выберите действие"

		reply_keyboard = [['Бронирование'],['Мои машины']]
		markup = ReplyKeyboardMarkup(reply_keyboard,resize_keyboard=True, one_time_keyboard=True)

		
		bot.sendMessage(user, text, reply_markup=markup, parse_mode=telegram.ParseMode.HTML)


		return NONE
	else:

		text = "Добро пожаловать в 4Park! Для начала работы, нужно пройти регистрацию"
		bot.sendMessage(user,text, parse_mode=telegram.ParseMode.HTML)

		text = "Отправьте свой номер телефона"
		markup = telegram.ReplyKeyboardMarkup([[telegram.KeyboardButton('Отправить номер', request_contact=True)]], resize_keyboard=True, one_time_keyboard=False)

		bot.sendMessage(user, text, reply_markup=markup, parse_mode=telegram.ParseMode.HTML)

		return NONE


def CreateStableKeyboard(data):
	length = len(data)

	keyboard = []
	keyboard_buttons = []

	if length % 2 == 0:
		a = 0
		i=0
		while i<length:
			my_keyboard_button = str(data[i]).replace("\n","")
			keyboard_buttons.append(my_keyboard_button)
			i+=1
			a+=1
			if a==2:
				keyboard.append(keyboard_buttons)
				keyboard_buttons = []
				a = 0
	else:
		a = 0
		i=0
		while i<length:
			if i == length-1:
				my_keyboard_button = str(data[i]).replace("\n","")
				keyboard_buttons.append(my_keyboard_button)
				i+=1
				a+=1
				if a==1:
					keyboard.append(keyboard_buttons)
					keyboard_buttons = []
					a = 0
					break
			else:
				my_keyboard_button = str(data[i]).replace("\n","")
				keyboard_buttons.append(my_keyboard_button)
				i+=1
				a+=1
				if a==2:
					keyboard.append(keyboard_buttons)
					keyboard_buttons = []
					a = 0

	keyboard_buttons = []
	my_keyboard_button = "Назад"

	keyboard_buttons.append(my_keyboard_button)

	keyboard.append(keyboard_buttons)


	return keyboard


def CreateInlineKeyboard(data):


	keyboard = []
	keyboard_buttons = []

	length = len(data)

	a=0
	for a in data:
		if a!="\n" and a!=data[0]:
			if "см" in a or "Без" in a:
				pass
			else:
				my_keyboard_button = InlineKeyboardButton(text=str(a).replace("\n",""), callback_data="empty")
				keyboard_buttons.append(my_keyboard_button)

		keyboard.append(keyboard_buttons)
		keyboard_buttons = []

	return InlineKeyboardMarkup(keyboard)



def text_handler(bot, update):
	NONE = ""

	recieved_text = update.message.text
	user = update.message.from_user.id

	if os.path.exists(os.getcwd()+"\\Users\\"+str(user)+"\\add_car_number"):
		os.remove(os.getcwd()+"\\Users\\"+str(user)+"\\add_car_number")

		file = open(os.getcwd()+"\\Users\\"+str(user)+"\\cars","a",encoding="utf8")
		file.write(recieved_text+"\n")
		file.close()

		text = "<b>Необязательно</b>\n\nВведите описание машины. Например, Машина Папы, Рабочая, Volvo"

		file = open(os.getcwd()+"\\Users\\"+str(user)+"\\add_car_description","w")
		file.close()

		reply_keyboard = [['Далее']]
		markup = ReplyKeyboardMarkup(reply_keyboard,resize_keyboard=True, one_time_keyboard=True)

		bot.sendMessage(user, text, reply_markup=markup, parse_mode=telegram.ParseMode.HTML)

		return NONE

	if os.path.exists(os.getcwd()+"\\Users\\"+str(user)+"\\add_car_description"):
		if recieved_text!="Далее":
			os.remove(os.getcwd()+"\\Users\\"+str(user)+"\\add_car_description")

			file = open(os.getcwd()+"\\Users\\"+str(user)+"\\cars","r")
			cars = file.readlines()
			file.close()

			file = open(os.getcwd()+"\\Users\\"+str(user)+"\\description","a", encoding="utf8")
			file.write(cars[len(cars)-1].replace("\n","")+" "+recieved_text+"\n")
			file.close()

			text = "Вот и всё! Приятного пользования (с) Команда 4Park"

			bot.sendMessage(user, text, parse_mode=telegram.ParseMode.HTML)

			text = "Выберите действие"

			reply_keyboard = [['Бронирование'],['Мои машины']]
			markup = ReplyKeyboardMarkup(reply_keyboard,resize_keyboard=True, one_time_keyboard=True)

			
			bot.sendMessage(user, text, reply_markup=markup, parse_mode=telegram.ParseMode.HTML)


			return NONE

	if "Далее" in recieved_text:
		os.remove(os.getcwd()+"\\Users\\"+str(user)+"\\add_car_description")

		file = open(os.getcwd()+"\\Users\\"+str(user)+"\\cars","r")
		cars = file.readlines()
		file.close()

		file = open(os.getcwd()+"\\Users\\"+str(user)+"\\description","a", encoding="utf8")
		file.write(cars[len(cars)-1].replace("\n","")+"\n")
		file.close()

		text = "Вот и всё! Приятного пользования (с) Команда 4Park"

		bot.sendMessage(user, text, parse_mode=telegram.ParseMode.HTML)

		text = "Выберите действие"

		reply_keyboard = [['Бронирование'],['Мои машины']]
		markup = ReplyKeyboardMarkup(reply_keyboard,resize_keyboard=True, one_time_keyboard=True)

		
		bot.sendMessage(user, text, reply_markup=markup, parse_mode=telegram.ParseMode.HTML)


		return NONE


	if "Добавить машину" in recieved_text:
		
		text = "Отправьте номер машины вида <b>01 A000AA</b>"

		file = open(os.getcwd()+"\\Users\\"+str(user)+"\\add_car_number","w")
		file.close()

		bot.sendMessage(user, text, parse_mode=telegram.ParseMode.HTML)

		return NONE

	if "Бронирование" in recieved_text:

		text = "Выберите место, куда бы вы хотели поехать"

		Places = os.listdir(os.getcwd()+"\\Places")

		bot.sendMessage(user, text, reply_markup=ReplyKeyboardMarkup(CreateStableKeyboard(Places),resize_keyboard=True, one_time_keyboard=True))

		return NONE

	if "Мои машины" in recieved_text:

		file = open(os.getcwd()+"\\Users\\"+str(user)+"\\description", "r", encoding="utf8")
		Cars = file.readlines()
		file.close()

		text = "Ваши машины"

		bot.sendMessage(user, text, reply_markup=CreateInlineKeyboard(Cars),resize_keyboard=True, one_time_keyboard=True)

		return NONE

	return NONE

def contact_handler(bot, update):
	NONE = ""

	user = update.message.from_user.id

	number = update.message.contact.phone_number

	if user == update.message.contact.user_id:
		if not "998" in number:
			text = "Приносим извинения за неудобства, но сервис 4Park пока что работает только на территории Узбекистана :(\n\nWe apologize for the inconvenience, but the 4Park service so far works only in the territory of Uzbekistan: ("

			bot.sendMessage(user, text, parse_mode=telegram.ParseMode.HTML)
		
			return NONE

		else:

			file = open(os.getcwd()+"\\Users\\"+str(user)+"\\phone_number","w")
			file.write(str(number))
			file.close()

			if os.path.exists(os.getcwd()+"\\Users\\"+str(user)+"\\cars"):

				text = "Выберите действие"

				reply_keyboard = [['Бронирование'],['Мои машины']]
				markup = ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True, one_time_keyboard=True)

				
				bot.sendMessage(user, text, reply_markup=markup, parse_mode=telegram.ParseMode.HTML)

				return NONE
			else:

				text = "Почти готово, но у вас пока нет добавленных машин"

				reply_keyboard = [['Добавить машину']]
				markup = ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True, one_time_keyboard=True)

				
				bot.sendMessage(user, text, reply_markup=markup, parse_mode=telegram.ParseMode.HTML)

				return NONE

	else:
		bot.sendMessage(user,"Нужно отправить свой номер!")

		return NONE



def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)


def main():
	if not os.path.exists(os.getcwd()+"\\Users\\"):
		os.makedirs(os.getcwd()+"\\Users\\")


	# Create the Updater and pass it your bot's token.
	print(str(datetime.datetime.now()) + "  Bot started...")
	updater = Updater(config.token)

	# Get the dispatcher to register handlers
	dispatcher = updater.dispatcher

	# Add conversation handler with the states CHOOSING, TYPING_CHOICE and TYPING_REPLY

	dispatcher.add_handler(CommandHandler("start",start))
	dispatcher.add_handler(MessageHandler(Filters.text, text_handler))
	dispatcher.add_handler(MessageHandler(Filters.contact, contact_handler))

	# log all errors
	dispatcher.add_error_handler(error)

	# Start the Bot
	updater.start_polling()

	# Run the bot until you press Ctrl-C or the process receives SIGINT,
	# SIGTERM or SIGABRT. This should be used most of the time, since
	# start_polling() is non-blocking and will stop the bot gracefully.
	updater.idle()


if __name__ == '__main__':
    main()