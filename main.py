from telebot import TeleBot
from telebot.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from random import randint
from telebot import types
import requests

API_URL = 'http://127.0.0.1:8000/'
bot = TeleBot('7937175776:AAHkh9r9ceDPlwCnMj7PpBFOT5V4Ku5S8KU')
state = {}

@bot.message_handler(commands=['start'])
def echo(message: Message):
   bot.send_message(chat_id=message.chat.id, text='выберите команду\n /laptops\n/add_laptop \n/delete_laptop\n/delete_filial\n/add_filial\n/add_note\n/delete_note')


@bot.message_handler(commands=['laptops'])
def get_laptop(message: Message):
   response = requests.get(API_URL + 'laptop')
   if response.status_code == 200:
      lst = []
      for lpt in response.json():
         lst.append(f"{lpt['mark']['mark']}\t{lpt['model']}\t{lpt['filial']['filial']}")
      
      bot.send_message(chat_id=message.chat.id, text='\n'.join(lst))
   else:
      bot.send_message(chat_id=message.chat.id, text='Ошибка')

@bot.message_handler(commands=['add_filial'])
def add_filial(message: Message):
   bot.send_message(chat_id=message.chat.id, text="Напишите название")

   bot.register_next_step_handler(message, add_fil)

@bot.message_handler(commands=['add_laptop'])
def add_laptop(message: Message):
   state[message.chat.id] = {}
   print(message.chat.id)
   filials = get_filials()
   markup = InlineKeyboardMarkup()
   for filial in filials:

      markup.add(InlineKeyboardButton(filial['filial'],callback_data=f"filial-{filial['id']}"))
   
   bot.send_message(chat_id=message.chat.id, text="Выберите  филиал",reply_markup=markup)
   

def mark(message):
   marks = get_marks()
   markup = InlineKeyboardMarkup()
   for mark in marks:

      markup.add(InlineKeyboardButton(mark['mark'],callback_data=f"mark-{mark['id']}"))

   markup.add(InlineKeyboardButton('Добавить Марку'),callback_data = 'mark-0')
   
   bot.send_message(chat_id=message.chat.id, text="Выберите  марку",reply_markup=markup)

def input_mark():
   bot.send_message(chat_id=message.chat.id, text='напишите модель')


def model(message):
   print(message.text)
   bot.send_message(chat_id=message.chat.id, text='напишите модель')
   bot.register_next_step_handler(message, CPU)


def CPU(message):
   print(message.text)
   bot.send_message(chat_id=message.chat.id, text='введите Какой процесор (Intel Core i5-1135G7)')
   state[message.chat.id]['model'] = message.text
   bot.register_next_step_handler(message, CPU_cores)

def CPU_cores(message):
   print(message.text)
   bot.send_message(chat_id=message.chat.id, text=' Введите колличество ядер процессора')
   state[message.chat.id]['CPU'] = message.text
   bot.register_next_step_handler(message, CPU_frequency)

def CPU_frequency(message):
   print(message.text)
   bot.send_message(chat_id=message.chat.id, text='введите частоту процессора')
   state[message.chat.id]['CPU_cores'] = int(message.text)
   bot.register_next_step_handler(message, RAM_amount)

def RAM_amount(message):
   print(message.text)
   bot.send_message(chat_id=message.chat.id, text='введите колличество оперативной памяти')
   state[message.chat.id]['CPU_frequency'] = message.text
   bot.register_next_step_handler(message, video_card)

def video_card(message):
   print(message.text)
   bot.send_message(chat_id=message.chat.id, text='введите видео карту')
   state[message.chat.id]['RAM_amount'] = message.text
   bot.register_next_step_handler(message, drive_type)

def drive_type(message):
   print(message.text)
   bot.send_message(chat_id=message.chat.id, text='введите тип диска (ssd или hdd)')
   state[message.chat.id]['video_card'] = message.text
   bot.register_next_step_handler(message, drive_amount)

def drive_amount(message):
   print(message.text)
   bot.send_message(chat_id=message.chat.id, text='введите размер диска')
   state[message.chat.id]['drive_type'] = message.text.upper()
   print(state[message.chat.id])
   bot.register_next_step_handler(message, add_lpt)


def add_lpt(message):
   state[message.chat.id]['drive_amount'] = int(message.text)
   new_laptop = state[message.chat.id]
   try:

      response = requests.post(API_URL + 'laptop',json=new_laptop)
      print(response.status_code)
      if response.status_code == 200:
         bot.send_message(chat_id=message.chat.id, text='Успешно!')

      else:
         bot.send_message(chat_id=message.chat.id, text=response.text)
   except:
       bot.send_message(chat_id=message.chat.id, text='error')

   state.pop([message.chat.id])



@bot.message_handler(commands=['filials'])
def get_filial(message: Message):
   response = requests.get(API_URL + 'filials')
   if response.status_code == 200:
      lst = []
      for fil in response.json():
         lst.append(f"{fil['filial']}\t")
      
      bot.send_message(chat_id=message.chat.id, text='\n'.join(lst))
   else:
      bot.send_message(chat_id=message.chat.id, text='Ошибка')



@bot.message_handler()
def echo(message: Message):
   bot.send_message(chat_id=message.chat.id, text=f'Привет, {message.from_user.username}')


# @bot.callback_query_handler(func=lambda callback: True)
# def callback_buttons(callback):
#    if callback.data =='yes':
#       bot.send_message(chat_id=callback.message.chat.id, text='Вы нажали ДА')
#    elif callback.data =='no':
#     bot.send_message(chat_id=callback.message.chat.id, text='Вы нажали ne')
#    print(callback)    

def add_fil(message):
   response = requests.post(API_URL + 'filials',json={'filial':message.text,'isative':True})
   print(response.status_code)


def get_filials():
   response = requests.get(API_URL + 'filials')
   lst = []
   if response.status_code == 200:
      lst = response.json()
      
   return lst

def add_mark(message):
   response = requests.post(API_URL + '/laptop/mark',json={'mark':message.text})
   print(response.status_code)

@bot.callback_query_handler(func=lambda call: call.data.startswith('filial-'))
def handler_fil(call: CallbackQuery):
   id = call.data.split('filial-')[1]
   state[call.message.chat.id]['filial_id'] = int(id)

   # bot.register_next_step_handler(call.message, mark)
   mark(call.message)


def get_marks():
   response = requests.get(API_URL + '/laptop/mark')
   lst = []
   if response.status_code == 200:
      lst = response.json()
      
   return lst


@bot.callback_query_handler(func=lambda call: call.data.startswith('mark-'))
def handler_fil(call: CallbackQuery):
   id = call.data.split('mark-')[1]
   if id == '0':
      bot.send_message(chat_id=call.message.chat.id, text='напишите марку')
      bot.register_next_step_handler()
      
   state[call.message.chat.id]['mark_id'] = int(id)

   model(call.message)



bot.polling()
