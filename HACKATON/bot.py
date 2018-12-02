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

import shutil
# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)



def start(bot, update):
	NONE = ""

	received_text = update.message.text
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


def CreateInlineKeyboard(data, place):


	keyboard = []
	keyboard_buttons = []

	length = len(data)

	a=0
	b=0
	if length==1:

		my_keyboard_button = InlineKeyboardButton(text=str(data[a]).replace("\n",""), callback_data=place + " " + str(data[a]).replace("\n",""))
		keyboard_buttons.append(my_keyboard_button)

		keyboard.append(keyboard_buttons)

		return InlineKeyboardMarkup(keyboard)


	else:
		while a<length-1:
			while b<7:
				try:
					my_keyboard_button = InlineKeyboardButton(text=str(data[a]).replace("\n",""), callback_data=place + " " + str(data[a]).replace("\n",""))
					keyboard_buttons.append(my_keyboard_button)

					a+=1
					b+=1
				except Exception as e:
					keyboard.append(keyboard_buttons)
					keyboard_buttons = []

					b=1

					break

			keyboard.append(keyboard_buttons)
			keyboard_buttons = []

			b=1

	return InlineKeyboardMarkup(keyboard)

def CreateInlineKeyboardFloors(data, place):


	keyboard = []
	keyboard_buttons = []

	length = len(data)

	a=0
	while a<length:

		my_keyboard_button = InlineKeyboardButton(text="Этаж " +str(a+1) + " - " +str(data[a]).replace("\n",""), callback_data="floor " + place + " "+str(a))
		keyboard_buttons.append(my_keyboard_button)

		keyboard.append(keyboard_buttons)
		keyboard_buttons = []

		a+=1

	return InlineKeyboardMarkup(keyboard)

def InlineHandler(bot, update):
	NONE = ""
	user = update.callback_query.message.chat.id
	received_text = update.callback_query.data

	if "floor" in received_text:
		received_text = received_text.replace("floor ","")
		data = received_text.split()

		place = data[0]
		if data[1].isdigit():
			floor = data[1]
		else:
			place = place + " "+data[1]
			floor = data[2]

		text = "<b>"+place+"</b> этаж "+str(int(floor)+1)+"\n\nВыберите парковочное место"

		file = open(os.getcwd()+"\\Places\\"+str(place)+"\\floor","r")
		floors = file.readlines()
		file.close()

		free_places = []
		compare = floors[int(floor)]
		for a in os.listdir(os.getcwd()+"\\Places\\"+str(place)+"\\Free\\"):
			if a in compare.split():
				free_places.append(a)

		bot.deleteMessage(user, update.callback_query.message.message_id)

		bot.sendMessage(user, text, reply_markup=CreateInlineKeyboard(free_places, place), parse_mode=telegram.ParseMode.HTML)

	else:
		data = received_text.split()
		place = data[0]
		if data[1].isdigit():
			number_place = data[1]
		else:
			place = place + " "+data[1]
			number_place = data[2]


		shutil.move(os.getcwd()+"\\Places\\"+str(place)+"\\Free\\"+number_place,os.getcwd()+"\\Places\\"+str(place)+"\\Reserved\\"+number_place)

		bot.deleteMessage(user, update.callback_query.message.message_id)

		file = open(os.getcwd()+"\\Places\\"+str(place)+"\\floor","r")
		floors = file.readlines()
		file.close()

		a=0
		while a<len(floors):
			if number_place in floors[a]:
				floor = a+1
				break
			else:
				a+=1

		bot.sendMessage(user, "Вы зарезервировали <b>"+number_place+"</b> место на "+str(floor)+" этаже", parse_mode=telegram.ParseMode.HTML)

		return NONE

def text_handler(bot, update):
	NONE = ""

	received_text = update.message.text
	user = update.message.from_user.id

	Places = os.listdir(os.getcwd()+"\\Places")

	if received_text in Places:

		text = "<b>"+received_text+"</b>\n\nВыберите этаж"

		free_places = os.listdir(os.getcwd()+"\\Places\\"+received_text+"\\Free\\")

		file = open(os.getcwd()+"\\Places\\"+str(received_text)+"\\floor","r")
		floors = file.readlines()
		file.close()

		length = len(floors)

		free_data = []
		num=0
		for b in floors:
			compare = b.split()
			for a in os.listdir(os.getcwd()+"\\Places\\"+str(received_text)+"\\Free\\"):
				if a in compare:
					num +=1
			free_data.append(num)
			num=0


		bot.send_photo(chat_id=user,caption=text, reply_markup=CreateInlineKeyboardFloors(free_data, received_text), photo=open(os.getcwd()+"\\Places\\"+received_text+"\\image.jpg", 'rb'),parse_mode=telegram.ParseMode.HTML)

		return NONE





	if os.path.exists(os.getcwd()+"\\Users\\"+str(user)+"\\add_car_number"):
		os.remove(os.getcwd()+"\\Users\\"+str(user)+"\\add_car_number")

		file = open(os.getcwd()+"\\Users\\"+str(user)+"\\cars","a",encoding="utf8")
		file.write(received_text+"\n")
		file.close()

		text = "<b>Необязательно</b>\n\nВведите описание машины. Например, Машина Папы, Рабочая, Volvo"

		file = open(os.getcwd()+"\\Users\\"+str(user)+"\\add_car_description","w")
		file.close()

		reply_keyboard = [['Далее']]
		markup = ReplyKeyboardMarkup(reply_keyboard,resize_keyboard=True, one_time_keyboard=True)

		bot.sendMessage(user, text, reply_markup=markup, parse_mode=telegram.ParseMode.HTML)

		return NONE

	if os.path.exists(os.getcwd()+"\\Users\\"+str(user)+"\\add_car_description"):
		if received_text!="Далее":
			os.remove(os.getcwd()+"\\Users\\"+str(user)+"\\add_car_description")

			file = open(os.getcwd()+"\\Users\\"+str(user)+"\\cars","r")
			cars = file.readlines()
			file.close()

			file = open(os.getcwd()+"\\Users\\"+str(user)+"\\description","a", encoding="utf8")
			file.write(cars[len(cars)-1].replace("\n","")+" "+received_text+"\n")
			file.close()

			text = "Вот и всё! Приятного пользования (с) Команда 4Park"

			bot.sendMessage(user, text, parse_mode=telegram.ParseMode.HTML)

			text = "Выберите действие"

			reply_keyboard = [['Бронирование'],['Мои машины']]
			markup = ReplyKeyboardMarkup(reply_keyboard,resize_keyboard=True, one_time_keyboard=True)

			
			bot.sendMessage(user, text, reply_markup=markup, parse_mode=telegram.ParseMode.HTML)


			return NONE

	if "Далее" in received_text:
		os.remove(os.getcwd()+"\\Users\\"+str(user)+"\\add_car_description")

		file = open(os.getcwd()+"\\Users\\"+str(user)+"\\cars","r")
		cars = file.readlines()
		file.close()

		file = open(os.getcwd()+"\\Users\\"+str(user)+"\\description","a", encoding="utf8")
		file.write(cars[len(cars)-1].replace("\n","")+"\n")
		file.close()

		text = "Вот и всё! Приятного пользования (с) Команда Easy+Park"

		bot.sendMessage(user, text, parse_mode=telegram.ParseMode.HTML)

		text = "Выберите действие"

		reply_keyboard = [['Бронирование'],['Мои машины']]
		markup = ReplyKeyboardMarkup(reply_keyboard,resize_keyboard=True, one_time_keyboard=True)

		
		bot.sendMessage(user, text, reply_markup=markup, parse_mode=telegram.ParseMode.HTML)


		return NONE


	if "Добавить машину" in received_text:
		
		text = "Отправьте номер машины вида\n<b>01 A000AA</b>"

		file = open(os.getcwd()+"\\Users\\"+str(user)+"\\add_car_number","w")
		file.close()

		bot.sendMessage(user, text, parse_mode=telegram.ParseMode.HTML)

		return NONE

	if "Бронирование" in received_text:

		text = "Выберите место, куда бы вы хотели поехать"

		Places = os.listdir(os.getcwd()+"\\Places")

		bot.sendMessage(user, text, reply_markup=ReplyKeyboardMarkup(CreateStableKeyboard(Places),resize_keyboard=True, one_time_keyboard=True))

		return NONE

	if "Мои машины" in received_text:

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
	dispatcher.add_handler(CallbackQueryHandler(InlineHandler))

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