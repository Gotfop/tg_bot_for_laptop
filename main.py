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
   bot.send_message(chat_id=message.chat.id, text='Напишите  марку')
   # state[message.chat.id]['filial_id'] = int(message.text)
   bot.register_next_step_handler(message, model)

def model(message):
   print(message.text)
   bot.send_message(chat_id=message.chat.id, text='напишите модель')
   state[message.chat.id]['mark_id'] = int(message.text)
   bot.register_next_step_handler(message, CPU)


def CPU(message):
   print(message.text)
   bot.send_message(chat_id=message.chat.id, text='введите CPU')
   state[message.chat.id]['model'] = message.text
   bot.register_next_step_handler(message, CPU_cores)

def CPU_cores(message):
   print(message.text)
   bot.send_message(chat_id=message.chat.id, text='введите CPU_cores')
   state[message.chat.id]['CPU'] = message.text
   bot.register_next_step_handler(message, CPU_frequency)

def CPU_frequency(message):
   print(message.text)
   bot.send_message(chat_id=message.chat.id, text='введите CPU_frequency')
   state[message.chat.id]['CPU_cores'] = int(message.text)
   bot.register_next_step_handler(message, RAM_amount)

def RAM_amount(message):
   print(message.text)
   bot.send_message(chat_id=message.chat.id, text='введите RAM_amount')
   state[message.chat.id]['CPU_frequency'] = message.text
   bot.register_next_step_handler(message, video_card)

def video_card(message):
   print(message.text)
   bot.send_message(chat_id=message.chat.id, text='введите video_card')
   state[message.chat.id]['RAM_amount'] = message.text
   bot.register_next_step_handler(message, drive_type)

def drive_type(message):
   print(message.text)
   bot.send_message(chat_id=message.chat.id, text='введите drive_type')
   state[message.chat.id]['video_card'] = message.text
   bot.register_next_step_handler(message, drive_amount)

def drive_amount(message):
   print(message.text)
   bot.send_message(chat_id=message.chat.id, text='введите drive_amount')
   state[message.chat.id]['drive_type'] = message.text.upper()
   print(state[message.chat.id])
   bot.register_next_step_handler(message, add_lpt)


def add_lpt(message):
   state[message.chat.id]['drive_amount'] = int(message.text)
   new_laptop = state[message.chat.id]
   
   response = requests.post(API_URL + 'laptop',json=new_laptop)
   print(response.status_code)
   state.clear()


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

def get_filials():
   response = requests.get(API_URL + 'filials')
   lst = []
   if response.status_code == 200:
      lst = response.json()
      
   return lst


@bot.callback_query_handler(func=lambda call: call.data.startswith('filial-'))
def handler_fil(call: CallbackQuery):
   id = call.data.split('filial-')[1]
   state[call.message.chat.id]['filial_id'] = int(id)
   print(id)

   # bot.register_next_step_handler(call.message, mark)
   mark(call.message)

bot.polling()
