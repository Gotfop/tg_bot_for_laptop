from telebot import TeleBot
from telebot.types import Message
from random import randint
from telebot import types
import requests

API_URL = 'http://127.0.0.1:8000/'
bot = TeleBot('7937175776:AAHUa8z2gBxYYirbdfqVWATAs8ve8YhgCqI')

@bot.message_handler(commands=['menu'])
def echo(message: Message):
   markup = types.ReplyKeyboardMarkup()
   markup.add(types.KeyboardButton('yes'))
   markup.add(types.KeyboardButton('Нет'))
   bot.send_message(chat_id=message.chat.id, text='Выбери поисковик', reply_markup=markup)


@bot.message_handler(commands=['random'])
def randm(message: Message):
   bot.send_message(chat_id=message.chat.id, text=randint(0,100000))


@bot.message_handler(commands=['add_problem'])
def get_note(message: Message):
   bot.send_message(chat_id=message.chat.id, text="Напишите заметку")


@bot.message_handler(commands=['laptops'])
def get_laptop(message: Message):
   response = requests.get(API_URL + 'laptop')
   if response.status_code() == 200:
      lst = []
      for lpt in response.json():
         lst.append(f'{lpt['mark_id']}\t{lpt['model']}')
      
      bot.send_message(chat_id=message.chat.id, text='\n'.join(lst))
   else:
      bot.send_message(chat_id=message.chat.id, text='Ошибка')


@bot.message_handler(commands=['laptop_filial'])
def laptop_filial(message: Message):
   markup = types.InlineKeyboardMarkup()
   markup.add(types.InlineKeyboardButton('Мозайка'))
   markup.add(types.InlineKeyboardButton('Лотос'))
   bot.send_message(chat_id=message.chat.id, text="Выберите филиалы:", reply_markup=markup)


@bot.message_handler()
def echo(message: Message):
   bot.send_message(chat_id=message.chat.id, text=f'Привет, {message.from_user.username}')


@bot.callback_query_handler(func=lambda callback: True)
def callback_buttons(callback):
   if callback.data =='yes':
      bot.send_message(chat_id=callback.message.chat.id, text='Вы нажали ДА')
   elif callback.data =='no':
    bot.send_message(chat_id=callback.message.chat.id, text='Вы нажали ne')
   print(callback)    


bot.polling()