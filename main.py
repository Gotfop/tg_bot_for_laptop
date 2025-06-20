from telebot import TeleBot
from telebot.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from random import randint
from telebot import types
import requests

API_URL = 'http://127.0.0.1:8000/'
bot = TeleBot('7937175776:AAHTS2wBvYfzYY9yFRRUe5cBr8yRqh3_wF8')
state = {}
filials = {}
marks = {}

def cancel_step(func):
    def wrapper(message):
        if message.text and message.text.startswith('/'):
            bot.clear_step_handler(message)
            return bot.process_new_messages([message])
        return func(message)
    return wrapper

@bot.message_handler(commands=['start'])
def echo(message: Message):
   bot.clear_step_handler(message)
   if message.chat.id in state:
      del state[message.chat.id]
   bot.set_my_commands([
      types.BotCommand('laptops','Список ноутбуков'),
      types.BotCommand('add_laptop','Добавить новый ноутбук'),
      types.BotCommand('add_filial','Добавить филиал'),
      

   ])
   bot.send_message(chat_id=message.chat.id, text='выберите команду\n /laptops\n/add_laptop \n/delete_laptop\n/delete_filial\n/add_filial\n/add_note\n/delete_note\n/filials')


@bot.message_handler(commands=['filials'])
def get_filial(message: Message):
   bot.clear_step_handler(message)
   if message.chat.id in state:
      del state[message.chat.id]
   response = requests.get(API_URL + 'filials')
   if response.status_code == 200:
      lst = []
      for fil in response.json():
         lst.append(f"{fil['filial']}\t")
      
      bot.send_message(chat_id=message.chat.id, text='\n'.join(lst))
   else:
      bot.send_message(chat_id=message.chat.id, text='Ошибка')

@bot.message_handler(commands=['laptops'])
def get_laptop(message: Message):
   bot.clear_step_handler(message)
   if message.chat.id in state:
      del state[message.chat.id]
   response = requests.get(API_URL + 'laptop')
   if response.status_code == 200:
      lst = '```\n'
      for lpt in response.json():
         lst += f"| {lpt['mark']['mark'].ljust(8)}| {lpt['model'][0:15].ljust(15)}| {lpt['filial']['filial'][0:9].ljust(9)}|\n"
      lst += '```'
      
      bot.send_message(chat_id=message.chat.id, text= lst,parse_mode='Markdown')
   else:
      bot.send_message(chat_id=message.chat.id, text='Ошибка')

@bot.message_handler(commands=['add_filial'])
def add_filial(message: Message):
   bot.clear_step_handler(message)
   if message.chat.id in state:
      del state[message.chat.id]
   bot.send_message(chat_id=message.chat.id, text="Напишите название")

   bot.register_next_step_handler(message, add_fil)

@bot.message_handler(commands=['add_laptop'])
def add_laptop(message: Message):
   bot.clear_step_handler(message)
   if message.chat.id in state:
      del state[message.chat.id]
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

   markup.add(InlineKeyboardButton('Добавить Марку',callback_data = 'mark-0'))
   
   bot.send_message(chat_id=message.chat.id, text="Выберите  марку",reply_markup=markup)

# def input_mark():
#    bot.send_message(chat_id=message.chat.id, text='напишите модель')


def model(message):
   print(message.text)
   bot.send_message(chat_id=message.chat.id, text='напишите модель')
   bot.register_next_step_handler(message, CPU)

@cancel_step
def CPU(message):
   print(message.text)
   bot.send_message(chat_id=message.chat.id, text='введите Какой процесор (Intel Core i5-1135G7)')
   state[message.chat.id]['model'] = message.text
   bot.register_next_step_handler(message, CPU_cores)
@cancel_step
def CPU_cores(message):
   print(message.text)
   bot.send_message(chat_id=message.chat.id, text=' Введите колличество ядер процессора')
   state[message.chat.id]['CPU'] = message.text
   bot.register_next_step_handler(message, CPU_frequency)

@cancel_step
def CPU_frequency(message):
   print(message.text)
   bot.send_message(chat_id=message.chat.id, text='введите частоту процессора')
   state[message.chat.id]['CPU_cores'] = int(message.text)
   bot.register_next_step_handler(message, RAM_amount)
@cancel_step
def RAM_amount(message):
   print(message.text)
   bot.send_message(chat_id=message.chat.id, text='введите колличество оперативной памяти')
   state[message.chat.id]['CPU_frequency'] = message.text
   bot.register_next_step_handler(message, video_card)
@cancel_step
def video_card(message):
   print(message.text)
   bot.send_message(chat_id=message.chat.id, text='введите видео карту')
   state[message.chat.id]['RAM_amount'] = message.text
   bot.register_next_step_handler(message, drive_type)
@cancel_step
def drive_type(message):
   print(message.text)
   bot.send_message(chat_id=message.chat.id, text='введите тип диска (ssd или hdd)')
   state[message.chat.id]['video_card'] = message.text
   bot.register_next_step_handler(message, drive_amount)
@cancel_step
def drive_amount(message):
   print(message.text)
   bot.send_message(chat_id=message.chat.id, text='введите размер диска')
   state[message.chat.id]['drive_type'] = message.text.upper()
   print(state[message.chat.id])
   bot.register_next_step_handler(message, add_lpt)

@cancel_step
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

   state.pop(message.chat.id)







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
      for filial  in lst:
         filials[filial['id']] = filial['filial']

   
      
   return lst

def add_mark(message):
   response = requests.post(API_URL + '/laptop/mark',json={'mark':message.text})
   if response.status_code == 200:
      mark(message)
   else:
      bot.send_message(chat_id=message.chat.id, text='Ошибка')
  

@bot.callback_query_handler(func=lambda call: call.data.startswith('filial-'))
def handler_fil(call: CallbackQuery):
   id = call.data.split('filial-')[1]
   state[call.message.chat.id]['filial_id'] = int(id)

   bot.edit_message_text(chat_id=call.message.chat.id,message_id=call.message.message_id,text=f'Выбрано: {filials[int(id)]}',reply_markup=None)

   # bot.register_next_step_handler(call.message, mark)
   mark(call.message)


def get_marks():
   response = requests.get(API_URL + '/laptop/mark')
   lst = []
   if response.status_code == 200:
      lst = response.json()
      for mark  in lst:
         marks[mark['id']] = mark['mark']
      
   return lst


@bot.callback_query_handler(func=lambda call: call.data.startswith('mark-'))
def handler_fil(call: CallbackQuery):
   id = call.data.split('mark-')[1]
   if id == '0':
      bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=None,text='напишите марку')
      bot.register_next_step_handler(call.message,add_mark)


   
   else:
      
      state[call.message.chat.id]['mark_id'] = int(id)

      bot.edit_message_text(chat_id=call.message.chat.id,message_id=call.message.message_id,text=f'Выбрано: {marks[int(id)]}',reply_markup=None)

      model(call.message)



bot.polling()
