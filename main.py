#Либы
import telebot
bot = telebot.TeleBot('Bot`s API Token')
from yandexfreetranslate import YandexFreeTranslate
yt = YandexFreeTranslate(api = "ios")
from langid import classify
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup
import os
from gtts import gTTS

#---Словари для сохранения языка и текста синтеза---
lang_user = {

}

user_texts = {
    
}

#---Команда /start---
@bot.message_handler(commands=['start'])
def send_welcome(message):
	markup = InlineKeyboardMarkup()
	markup.row_width = 1
	markup1 = InlineKeyboardButton("Перевести с ин. языка", callback_data="transRU")
	markup2 = InlineKeyboardButton("Перевести на ин. язык", callback_data="transfromru")
	markup.add(markup1, markup2)
	bot.send_message(message.chat.id, 'Привет!\nТут вы сможете перевести сообщения.\nДля управления используй кнопки ниже.', reply_markup=markup)

#---Перевод Ин.яз => RU---
@bot.callback_query_handler(func=lambda callback: callback.data == "transRU")
def transRU_callback(callback):
	markup = InlineKeyboardMarkup()
	markup.row_width = 1
	markup1 = InlineKeyboardButton("Меню", callback_data="menu")
	markup.add(markup1)
	msg = bot.edit_message_text(chat_id = callback.message.chat.id, message_id = callback.message.message_id, text = 'При перерводе с некоторых языков бот может вести себя некорректно!\n\nВведите сообщение для перевода, или нажмите на кнопку чтобы вернуться в меню:', reply_markup=markup)
	bot.clear_step_handler_by_chat_id(chat_id = callback.message.chat.id)
	bot.register_next_step_handler(msg, translate_message)	

def translate_message(message):
	markup = InlineKeyboardMarkup()
	markup.row_width = 2
	markup1 = InlineKeyboardButton("Еще раз", callback_data="transRU1")
	markup2 = InlineKeyboardButton("Меню", callback_data="menu1")
	markup3 = InlineKeyboardButton("Синтез", callback_data="sintezNA")
	markup.add(markup1, markup2, markup3)
	lang1 = classify(message.text)
	try:
		#print(lang1)
		translated_text = yt.translate(lang1[0], "ru", message.text)
		user_texts[str(message.chat.id)] = translated_text
		bot.reply_to(message, text = f'`{translated_text}`\n\n*Нажмите на текст, чтобы скопировать его.*', reply_markup=markup, parse_mode="Markdown")
	except:
		markup = InlineKeyboardMarkup()
		markup.row_width = 2
		markup1 = InlineKeyboardButton("Еще раз", callback_data="transRU1")
		markup2 = InlineKeyboardButton("Меню", callback_data="menu")
		markup.add(markup1, markup2)
		bot.send_message(chat_id=message.chat.id, text = "Выбранный вами язык не поддерживается.\nПоробуйте другой язык", reply_markup=markup)

@bot.callback_query_handler(func=lambda callback: callback.data == "transRU1")
def transRU1_callback(callback):
	markup = InlineKeyboardMarkup()
	markup.row_width = 1
	markup1 = InlineKeyboardButton("Меню", callback_data="menu")
	markup.add(markup1)
	msg = bot.send_message(chat_id=callback.message.chat.id, text = "Введите сообщение еще раз или вернитесь в меню", reply_markup=markup)
	bot.clear_step_handler_by_chat_id(chat_id = callback.message.chat.id)
	bot.register_next_step_handler(msg, translate_message)

#---Меню---
@bot.callback_query_handler(func=lambda callback: callback.data == "menu")
def menu_callback(callback):
	markup = InlineKeyboardMarkup()
	markup.row_width = 1
	markup1 = InlineKeyboardButton("Перевести с ин. языка", callback_data="transRU")
	markup2 = InlineKeyboardButton("Перевести на ин. язык", callback_data="transfromru")
	markup.add(markup1, markup2)
	bot.edit_message_text(chat_id = callback.message.chat.id, message_id = callback.message.message_id, text = 'Выберите одну из функций ниже:', reply_markup=markup)

@bot.callback_query_handler(func=lambda callback: callback.data == "menu1")
def menu1_callback(callback):
	markup = InlineKeyboardMarkup()
	markup.row_width = 1
	markup1 = InlineKeyboardButton("Перевести с ин. языка", callback_data="transRU")
	markup2 = InlineKeyboardButton("Перевести на ин. язык", callback_data="transfromru")
	markup.add(markup1, markup2)
	bot.send_message(chat_id = callback.message.chat.id, text = 'Выберите одну из функций ниже:', reply_markup=markup)
	
#---Перевод RU => ИН.ЯЗ---	
@bot.callback_query_handler(func=lambda callback: callback.data == "transfromru")
def transfromru_callback(callback):
	markup = InlineKeyboardMarkup()
	markup1 = InlineKeyboardButton("Английский 🇬🇧", callback_data="ENG")
	markup2 = InlineKeyboardButton("Немецкий 🇩🇪", callback_data="DE")
	markup3 = InlineKeyboardButton("Китайский 🇨🇳", callback_data="ZN")
	markup4 = InlineKeyboardButton("Японский 🇯🇵", callback_data="JA")
	markup5 = InlineKeyboardButton("Иcпанский 🇪🇸", callback_data="ES")
	markup6 = InlineKeyboardButton("Хинди 🇮🇳", callback_data="HI")
	markup7 = InlineKeyboardButton("Арабский 🇪🇬", callback_data="AR")
	markup8 = InlineKeyboardButton("Бенгал 🇧🇩", callback_data="BN")
	markup9 = InlineKeyboardButton("Португал 🇵🇹", callback_data="PT")
	markup10 = InlineKeyboardButton("Меню", callback_data="menu")
	markup.add(markup1, markup2, markup3, markup4, markup5, markup6, markup7, markup8, markup9, markup10)
	bot.edit_message_text(chat_id = callback.message.chat.id, message_id = callback.message.message_id, text = 'Веберите на какой язык хотите перевести, или нажмите на кнопку чтобы вернуться в меню:', reply_markup=markup)

@bot.callback_query_handler(func=lambda callback: callback.data == "transfromru1")
def transfromru1_callback(callback):
	markup = InlineKeyboardMarkup()
	markup1 = InlineKeyboardButton("Английский 🇬🇧", callback_data="ENG")
	markup2 = InlineKeyboardButton("Немецкий 🇩🇪", callback_data="DE")
	markup3 = InlineKeyboardButton("Китайский 🇨🇳", callback_data="ZN")
	markup4 = InlineKeyboardButton("Японский 🇯🇵", callback_data="JA")
	markup5 = InlineKeyboardButton("Иcпанский 🇪🇸", callback_data="ES")
	markup6 = InlineKeyboardButton("Хинди 🇮🇳", callback_data="HI")
	markup7 = InlineKeyboardButton("Арабский 🇪🇬", callback_data="AR")
	markup8 = InlineKeyboardButton("Бенгал 🇧🇩", callback_data="BN")
	markup9 = InlineKeyboardButton("Португал 🇵🇹", callback_data="PT")
	markup10 = InlineKeyboardButton("Меню", callback_data="menu")
	markup.add(markup1, markup2, markup3, markup4, markup5, markup6, markup7, markup8, markup9, markup10)
	bot.send_message(chat_id = callback.message.chat.id, text = 'Веберите на какой язык хотите перевести, или нажмите на кнопку чтобы вернуться в меню:', reply_markup=markup)

#---Английский---
@bot.callback_query_handler(func=lambda callback: callback.data == "ENG")
def ENG_callback(callback):
	markup = InlineKeyboardMarkup()
	markup.row_width = 1
	markup1 = InlineKeyboardButton("Вернуться к выбору языка", callback_data="transfromru")
	markup2 = InlineKeyboardButton("Меню", callback_data="menu")
	markup.add(markup1, markup2)
	msg = bot.edit_message_text(chat_id = callback.message.chat.id, message_id = callback.message.message_id, text = 'Отправьте сообщение для перевода, или вернитесь в меню', reply_markup=markup)
	bot.clear_step_handler_by_chat_id(chat_id = callback.message.chat.id)
	bot.register_next_step_handler(msg, ENG_trans)

@bot.callback_query_handler(func=lambda callback: callback.data == "ENG1")
def ENG1_callback(callback):
	markup = InlineKeyboardMarkup()
	markup.row_width = 1
	markup1 = InlineKeyboardButton("Вернуться к выбору языка", callback_data="transfromru")
	markup2 = InlineKeyboardButton("Меню", callback_data="menu")
	markup.add(markup1, markup2)
	msg = bot.send_message(chat_id = callback.message.chat.id, text = 'Отправьте сообщение для перевода, или вернитесь в меню', reply_markup=markup)
	bot.clear_step_handler_by_chat_id(chat_id = callback.message.chat.id)
	bot.register_next_step_handler(msg, ENG_trans)

def ENG_trans(message):
	global lang_user
	global user_texts
	lang_user[str(message.chat.id)] = 'en'
	markup = InlineKeyboardMarkup()
	markup1 = InlineKeyboardButton("Еще раз", callback_data="ENG1")
	markup2 = InlineKeyboardButton("Меню", callback_data="menu1")
	markup3 = InlineKeyboardButton("Синтез речи", callback_data="sintezFrom")
	markup4 = InlineKeyboardButton("Вернуться к выбору языка", callback_data="transfromru1")
	markup.add(markup1, markup2, markup3, markup4)
	translated_text = yt.translate("ru", "en", message.text)
	user_texts[str(message.chat.id)] = translated_text
	bot.reply_to(message, text = f'`{translated_text}`\n\n*Нажмите на текст, чтобы скопировать его.*', reply_markup=markup, parse_mode = 'Markdown')

#---Немецкий---
@bot.callback_query_handler(func=lambda callback: callback.data == "DE")
def DE_callback(callback):
	markup = InlineKeyboardMarkup()
	markup.row_width = 1
	markup1 = InlineKeyboardButton("Вернуться к выбору языка", callback_data="transfromru")
	markup2 = InlineKeyboardButton("Меню", callback_data="menu")
	markup.add(markup1, markup2)
	msg = bot.edit_message_text(chat_id = callback.message.chat.id, message_id = callback.message.message_id, text = 'Отправьте сообщение для перевода, или вернитесь в меню', reply_markup=markup)
	bot.clear_step_handler_by_chat_id(chat_id = callback.message.chat.id)
	bot.register_next_step_handler(msg, DE_trans)
	
@bot.callback_query_handler(func=lambda callback: callback.data == "DE1")
def DE_callback(callback):
	markup = InlineKeyboardMarkup()
	markup.row_width = 1
	markup1 = InlineKeyboardButton("Вернуться к выбору языка", callback_data="transfromru")
	markup2 = InlineKeyboardButton("Меню", callback_data="menu")
	markup.add(markup1, markup2)
	msg = bot.send_message(chat_id = callback.message.chat.id, text = 'Отправьте сообщение для перевода, или вернитесь в меню', reply_markup=markup)
	bot.clear_step_handler_by_chat_id(chat_id = callback.message.chat.id)
	bot.register_next_step_handler(msg, DE_trans)

def DE_trans(message):
	global lang_user
	global user_texts
	lang_user[str(message.chat.id)] = 'de'
	markup = InlineKeyboardMarkup()
	markup1 = InlineKeyboardButton("Еще раз", callback_data="DE1")
	markup2 = InlineKeyboardButton("Меню", callback_data="menu1")
	markup3 = InlineKeyboardButton("Синтез речи", callback_data="sintezFrom")
	markup4 = InlineKeyboardButton("Вернуться к выбору языка", callback_data="transfromru1")
	markup.add(markup1, markup2, markup3, markup4)
	translated_text = yt.translate("ru", "de", message.text)
	user_texts[str(message.chat.id)] = translated_text
	bot.reply_to(message, text = f'`{translated_text}`\n\n*Нажмите на текст, чтобы скопировать его.*', reply_markup=markup, parse_mode = 'Markdown')

#---Китайский---
@bot.callback_query_handler(func=lambda callback: callback.data == "ZN")
def ZN_callback(callback):
	markup = InlineKeyboardMarkup()
	markup.row_width = 1
	markup1 = InlineKeyboardButton("Вернуться к выбору языка", callback_data="transfromru")
	markup2 = InlineKeyboardButton("Меню", callback_data="menu")
	markup.add(markup1, markup2)
	msg = bot.edit_message_text(chat_id = callback.message.chat.id, message_id = callback.message.message_id, text = 'Отправьте сообщение для перевода, или вернитесь в меню', reply_markup=markup)
	bot.clear_step_handler_by_chat_id(chat_id = callback.message.chat.id)
	bot.register_next_step_handler(msg, ZN_trans)
	
@bot.callback_query_handler(func=lambda callback: callback.data == "ZN1")
def ZN1_callback(callback):
	markup = InlineKeyboardMarkup()
	markup.row_width = 1
	markup1 = InlineKeyboardButton("Вернуться к выбору языка", callback_data="transfromru")
	markup2 = InlineKeyboardButton("Меню", callback_data="menu")
	markup.add(markup1, markup2)
	msg = bot.send_message(chat_id = callback.message.chat.id, text = 'Отправьте сообщение для перевода, или вернитесь в меню', reply_markup=markup)
	bot.clear_step_handler_by_chat_id(chat_id = callback.message.chat.id)
	bot.register_next_step_handler(msg, ZN_trans)

def ZN_trans(message):
	global lang_user
	global user_texts
	lang_user[str(message.chat.id)] = 'zh'
	markup = InlineKeyboardMarkup()
	markup1 = InlineKeyboardButton("Еще раз", callback_data="ZN1")
	markup2 = InlineKeyboardButton("Меню", callback_data="menu1")
	markup3 = InlineKeyboardButton("Синтез речи", callback_data="sintezFrom")
	markup4 = InlineKeyboardButton("Вернуться к выбору языка", callback_data="transfromru1")
	markup.add(markup1, markup2, markup3, markup4)
	translated_text = yt.translate("ru", "zh", message.text)
	user_texts[str(message.chat.id)] = translated_text
	bot.reply_to(message, text = f'`{translated_text}`\n\n*Нажмите на текст, чтобы скопировать его.*', reply_markup=markup, parse_mode = 'Markdown')

#---Итальянский---
@bot.callback_query_handler(func=lambda callback: callback.data == "JA")
def JA_callback(callback):
	markup = InlineKeyboardMarkup()
	markup.row_width = 1
	markup1 = InlineKeyboardButton("Вернуться к выбору языка", callback_data="transfromru")
	markup2 = InlineKeyboardButton("Меню", callback_data="menu")
	markup.add(markup1, markup2)
	msg = bot.edit_message_text(chat_id = callback.message.chat.id, message_id = callback.message.message_id, text = 'Отправьте сообщение для перевода, или вернитесь в меню', reply_markup=markup)
	bot.clear_step_handler_by_chat_id(chat_id = callback.message.chat.id)
	bot.register_next_step_handler(msg, JA_trans)
	
@bot.callback_query_handler(func=lambda callback: callback.data == "JA1")
def JA1_callback(callback):
	markup = InlineKeyboardMarkup()
	markup.row_width = 1
	markup1 = InlineKeyboardButton("Вернуться к выбору языка", callback_data="transfromru")
	markup2 = InlineKeyboardButton("Меню", callback_data="menu")
	markup.add(markup1, markup2)
	msg = bot.send_message(chat_id = callback.message.chat.id, text = 'Отправьте сообщение для перевода, или вернитесь в меню', reply_markup=markup)
	bot.clear_step_handler_by_chat_id(chat_id = callback.message.chat.id)
	bot.register_next_step_handler(msg, JA_trans)

def JA_trans(message):
	global lang_user
	global user_texts
	lang_user[str(message.chat.id)] = 'ja'
	markup = InlineKeyboardMarkup()
	markup1 = InlineKeyboardButton("Еще раз", callback_data="IT1")
	markup2 = InlineKeyboardButton("Меню", callback_data="menu1")
	markup3 = InlineKeyboardButton("Синтез речи", callback_data="sintezFrom")
	markup4 = InlineKeyboardButton("Вернуться к выбору языка", callback_data="transfromru1")
	markup.add(markup1, markup2, markup3, markup4)
	translated_text = yt.translate("ru", "ja", message.text)
	user_texts[str(message.chat.id)] = translated_text
	bot.reply_to(message, text = f'`{translated_text}`\n\n*Нажмите на текст, чтобы скопировать его.*', reply_markup=markup, parse_mode = 'Markdown')

#---Испанский---
@bot.callback_query_handler(func=lambda callback: callback.data == "ES")
def ES_callback(callback):
	markup = InlineKeyboardMarkup()
	markup.row_width = 1
	markup1 = InlineKeyboardButton("Вернуться к выбору языка", callback_data="transfromru")
	markup2 = InlineKeyboardButton("Меню", callback_data="menu")
	markup.add(markup1, markup2)
	msg = bot.edit_message_text(chat_id = callback.message.chat.id, message_id = callback.message.message_id, text = 'Отправьте сообщение для перевода, или вернитесь в меню', reply_markup=markup)
	bot.clear_step_handler_by_chat_id(chat_id = callback.message.chat.id)
	bot.register_next_step_handler(msg, ES_trans)
	
@bot.callback_query_handler(func=lambda callback: callback.data == "ES1")
def ES1_callback(callback):
	markup = InlineKeyboardMarkup()
	markup.row_width = 1
	markup1 = InlineKeyboardButton("Вернуться к выбору языка", callback_data="transfromru")
	markup2 = InlineKeyboardButton("Меню", callback_data="menu")
	markup.add(markup1, markup2)
	msg = bot.send_message(chat_id = callback.message.chat.id, text = 'Отправьте сообщение для перевода, или вернитесь в меню', reply_markup=markup)
	bot.clear_step_handler_by_chat_id(chat_id = callback.message.chat.id)
	bot.register_next_step_handler(msg, ES_trans)

def ES_trans(message):
	global lang_user
	global user_texts
	lang_user[str(message.chat.id)] = 'es'
	markup = InlineKeyboardMarkup()
	markup1 = InlineKeyboardButton("Еще раз", callback_data="ES1")
	markup2 = InlineKeyboardButton("Меню", callback_data="menu1")
	markup3 = InlineKeyboardButton("Синтез речи", callback_data="sintezFrom")
	markup4 = InlineKeyboardButton("Вернуться к выбору языка", callback_data="transfromru1")
	markup.add(markup1, markup2, markup3, markup4)
	translated_text = yt.translate("ru", "es", message.text)
	user_texts[str(message.chat.id)] = translated_text
	bot.reply_to(message, text = f'`{translated_text}`\n\n*Нажмите на текст, чтобы скопировать его.*', reply_markup=markup, parse_mode = 'Markdown')

#---Хинди---
@bot.callback_query_handler(func=lambda callback: callback.data == "HI")
def HI_callback(callback):
	markup = InlineKeyboardMarkup()
	markup.row_width = 1
	markup1 = InlineKeyboardButton("Вернуться к выбору языка", callback_data="transfromru")
	markup2 = InlineKeyboardButton("Меню", callback_data="menu")
	markup.add(markup1, markup2)
	msg = bot.edit_message_text(chat_id = callback.message.chat.id, message_id = callback.message.message_id, text = 'Отправьте сообщение для перевода, или вернитесь в меню', reply_markup=markup)
	bot.clear_step_handler_by_chat_id(chat_id = callback.message.chat.id)
	bot.register_next_step_handler(msg, HI_trans)
	
@bot.callback_query_handler(func=lambda callback: callback.data == "HI1")
def HI1_callback(callback):
	markup = InlineKeyboardMarkup()
	markup.row_width = 1
	markup1 = InlineKeyboardButton("Вернуться к выбору языка", callback_data="transfromru")
	markup2 = InlineKeyboardButton("Меню", callback_data="menu")
	markup.add(markup1, markup2)
	msg = bot.send_message(chat_id = callback.message.chat.id, text = 'Отправьте сообщение для перевода, или вернитесь в меню', reply_markup=markup)
	bot.clear_step_handler_by_chat_id(chat_id = callback.message.chat.id)
	bot.register_next_step_handler(msg, HI_trans)

def HI_trans(message):
	global lang_user
	global user_texts
	lang_user[str(message.chat.id)] = 'hi'
	markup = InlineKeyboardMarkup()
	markup1 = InlineKeyboardButton("Еще раз", callback_data="HI1")
	markup2 = InlineKeyboardButton("Меню", callback_data="menu1")
	markup3 = InlineKeyboardButton("Синтез речи", callback_data="sintezFrom")
	markup4 = InlineKeyboardButton("Вернуться к выбору языка", callback_data="transfromru1")
	markup.add(markup1, markup2, markup3, markup4)
	translated_text = yt.translate("ru", "hi", message.text)
	user_texts[str(message.chat.id)] = translated_text
	bot.reply_to(message, text = f'`{translated_text}`\n\n*Нажмите на текст, чтобы скопировать его.*', reply_markup=markup, parse_mode = 'Markdown')

#---Арабский---
@bot.callback_query_handler(func=lambda callback: callback.data == "AR")
def AR_callback(callback):
	markup = InlineKeyboardMarkup()
	markup.row_width = 1
	markup1 = InlineKeyboardButton("Вернуться к выбору языка", callback_data="transfromru")
	markup2 = InlineKeyboardButton("Меню", callback_data="menu")
	markup.add(markup1, markup2)
	msg = bot.edit_message_text(chat_id = callback.message.chat.id, message_id = callback.message.message_id, text = 'Отправьте сообщение для перевода, или вернитесь в меню', reply_markup=markup)
	bot.clear_step_handler_by_chat_id(chat_id = callback.message.chat.id)
	bot.register_next_step_handler(msg, AR_trans)
	
@bot.callback_query_handler(func=lambda callback: callback.data == "AR1")
def AR1_callback(callback):
	markup = InlineKeyboardMarkup()
	markup.row_width = 1
	markup1 = InlineKeyboardButton("Вернуться к выбору языка", callback_data="transfromru")
	markup2 = InlineKeyboardButton("Меню", callback_data="menu")
	markup.add(markup1, markup2)
	msg = bot.send_message(chat_id = callback.message.chat.id, text = 'Отправьте сообщение для перевода, или вернитесь в меню', reply_markup=markup)
	bot.clear_step_handler_by_chat_id(chat_id = callback.message.chat.id)
	bot.register_next_step_handler(msg, AR_trans)

def AR_trans(message):
	global lang_user
	global user_texts
	lang_user[str(message.chat.id)] = 'ar'
	markup = InlineKeyboardMarkup()
	markup1 = InlineKeyboardButton("Еще раз", callback_data="AR1")
	markup2 = InlineKeyboardButton("Меню", callback_data="menu1")
	markup3 = InlineKeyboardButton("Синтез речи", callback_data="sintezFrom")
	markup4 = InlineKeyboardButton("Вернуться к выбору языка", callback_data="transfromru1")
	markup.add(markup1, markup2, markup3, markup4)
	translated_text = yt.translate("ru", "ar", message.text)
	user_texts[str(message.chat.id)] = translated_text
	bot.reply_to(message, text = f'`{translated_text}`\n\n*Нажмите на текст, чтобы скопировать его.*', reply_markup=markup, parse_mode = 'Markdown')

#---Бенгальский---
@bot.callback_query_handler(func=lambda callback: callback.data == "BN")
def BN_callback(callback):
	markup = InlineKeyboardMarkup()
	markup.row_width = 1
	markup1 = InlineKeyboardButton("Вернуться к выбору языка", callback_data="transfromru")
	markup2 = InlineKeyboardButton("Меню", callback_data="menu")
	markup.add(markup1, markup2)
	msg = bot.edit_message_text(chat_id = callback.message.chat.id, message_id = callback.message.message_id, text = 'Отправьте сообщение для перевода, или вернитесь в меню', reply_markup=markup)
	bot.clear_step_handler_by_chat_id(chat_id = callback.message.chat.id)
	bot.register_next_step_handler(msg, BN_trans)
	
@bot.callback_query_handler(func=lambda callback: callback.data == "BN1")
def BN1_callback(callback):
	markup = InlineKeyboardMarkup()
	markup.row_width = 1
	markup1 = InlineKeyboardButton("Вернуться к выбору языка", callback_data="transfromru")
	markup2 = InlineKeyboardButton("Меню", callback_data="menu")
	markup.add(markup1, markup2)
	msg = bot.send_message(chat_id = callback.message.chat.id, text = 'Отправьте сообщение для перевода, или вернитесь в меню', reply_markup=markup)
	bot.clear_step_handler_by_chat_id(chat_id = callback.message.chat.id)
	bot.register_next_step_handler(msg, BN_trans)

def BN_trans(message):
	global lang_user
	global user_texts
	lang_user[str(message.chat.id)] = 'bn'
	markup = InlineKeyboardMarkup()
	markup1 = InlineKeyboardButton("Еще раз", callback_data="AR1")
	markup2 = InlineKeyboardButton("Меню", callback_data="menu1")
	markup3 = InlineKeyboardButton("Синтез речи", callback_data="sintezFrom")
	markup4 = InlineKeyboardButton("Вернуться к выбору языка", callback_data="transfromru1")
	markup.add(markup1, markup2, markup3, markup4)
	translated_text = yt.translate("ru", "bn", message.text)
	user_texts[str(message.chat.id)] = translated_text
	bot.reply_to(message, text = f'`{translated_text}`\n\n*Нажмите на текст, чтобы скопировать его.*', reply_markup=markup, parse_mode = 'Markdown')

#---Португальский---
@bot.callback_query_handler(func=lambda callback: callback.data == "PT")
def PT_callback(callback):
	markup = InlineKeyboardMarkup()
	markup.row_width = 1
	markup1 = InlineKeyboardButton("Вернуться к выбору языка", callback_data="transfromru")
	markup2 = InlineKeyboardButton("Меню", callback_data="menu")
	markup.add(markup1, markup2)
	msg = bot.edit_message_text(chat_id = callback.message.chat.id, message_id = callback.message.message_id, text = 'Отправьте сообщение для перевода, или вернитесь в меню', reply_markup=markup)
	bot.clear_step_handler_by_chat_id(chat_id = callback.message.chat.id)
	bot.register_next_step_handler(msg, PT_trans)
	
@bot.callback_query_handler(func=lambda callback: callback.data == "PT1")
def PT1_callback(callback):
	markup = InlineKeyboardMarkup()
	markup.row_width = 1
	markup1 = InlineKeyboardButton("Вернуться к выбору языка", callback_data="transfromru")
	markup2 = InlineKeyboardButton("Меню", callback_data="menu")
	markup.add(markup1, markup2)
	msg = bot.send_message(chat_id = callback.message.chat.id, text = 'Отправьте сообщение для перевода, или вернитесь в меню', reply_markup=markup)
	bot.clear_step_handler_by_chat_id(chat_id = callback.message.chat.id)
	bot.register_next_step_handler(msg, PT_trans)

def PT_trans(message):
	global lang_user
	global user_texts
	lang_user[str(message.chat.id)] = 'pt'
	markup = InlineKeyboardMarkup()
	markup1 = InlineKeyboardButton("Еще раз", callback_data="AR1")
	markup2 = InlineKeyboardButton("Меню", callback_data="menu1")
	markup3 = InlineKeyboardButton("Синтез речи", callback_data="sintezFrom")
	markup4 = InlineKeyboardButton("Вернуться к выбору языка", callback_data="transfromru1")
	markup.add(markup1, markup2, markup3, markup4)
	translated_text = yt.translate("ru", "pt", message.text)
	user_texts[str(message.chat.id)] = translated_text
	bot.reply_to(message, text = f'`{translated_text}`\n\n*Нажмите на текст, чтобы скопировать его.*', reply_markup=markup, parse_mode = 'Markdown')

#---Синтез речи ин. яз---
@bot.callback_query_handler(func=lambda callback: callback.data == "sintezFrom")
def sintez_callback(callback):
	global lang_user
	global user_texts
	sint_lang = lang_user[str(callback.message.chat.id)]
	del lang_user[str(callback.message.chat.id)]
	markup = InlineKeyboardMarkup()
	markup.row_width = 1
	markup1 = InlineKeyboardButton("Меню", callback_data="menu1")
	markup.add(markup1)
	voice_text = user_texts[str(callback.message.chat.id)]
	del user_texts[str(callback.message.chat.id)]

#---Синтез + сохранение/удаление mp3 файла---
	voice = gTTS(text = voice_text, lang = sint_lang )
	voice.save('voice.mp3')      
	voice = open('voice.mp3', 'rb')

	markup = InlineKeyboardMarkup()
	markup.row_width = 1
	markup1 = markup1 = InlineKeyboardButton("Вернуться к выбору языка", callback_data="transfromru1")
	markup2 = InlineKeyboardButton("Меню", callback_data="menu1")
	markup.add(markup1, markup2)
	bot.send_audio(callback.message.chat.id, voice, performer = 'Wineus TB' ,title = voice_text, reply_markup=markup)
	voice.close()
	os.remove('voice.mp3')

#---Синтез речи рус---
@bot.callback_query_handler(func=lambda callback: callback.data == "sintezNA")
def sintez_callback(callback):
	global user_texts
	markup = InlineKeyboardMarkup()
	markup.row_width = 1
	markup1 = InlineKeyboardButton("Меню", callback_data="menu1")
	markup.add(markup1)
	voice_text = user_texts[str(callback.message.chat.id)]
	del user_texts[str(callback.message.chat.id)]
	voice = gTTS(text = voice_text, lang = 'ru' )
	voice.save('voice.mp3')      
	voice = open('voice.mp3', 'rb')
	
	markup = InlineKeyboardMarkup()
	markup.row_width = 1
	markup1 = InlineKeyboardButton("Перевести еще раз", callback_data="transRU1")
	markup2 = InlineKeyboardButton("Меню", callback_data="menu1")
	markup.add(markup1, markup2)
	bot.send_audio(callback.message.chat.id, voice, performer = 'Wineus TB' ,title = voice_text, reply_markup=markup)
	voice.close()
	os.remove('voice.mp3')
#Запуск бота
bot.infinity_polling(none_stop=True)