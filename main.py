from telebot import TeleBot
from telebot.types import Message
from random import randint
from telebot import types
import requests

API_URL = 'http://127.0.0.1:8000/'
bot = TeleBot('7937175776:AAHUa8z2gBxYYirbdfqVWATAs8ve8YhgCqI')
lpt = []

@bot.message_handler(commands=['start'])
def echo(message: Message):
   bot.send_message(chat_id=message.chat.id, text='выберите команду\n /all_laptop\n/add_laptop \n/delete_laptop\n/delete_filial\n/add_filial\n/add_note\n/delete_note')

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
   bot.send_message(chat_id=message.chat.id, text="Напишите  марку")
   bot.register_next_step_handler(message, model)

def model(message):
   print(message.text)
   bot.send_message(chat_id=message.chat.id, text='напишите модель')
   lpt.append(message.text)
   bot.register_next_step_handler(message, CPU)


def CPU(message):
   print(message.text)
   bot.send_message(chat_id=message.chat.id, text='введите CPU')
   lpt.append(message.text)
   bot.register_next_step_handler(message, CPU_cores)

def CPU_cores(message):
   print(message.text)
   bot.send_message(chat_id=message.chat.id, text='введите CPU_cores')
   lpt.append(message.text)
   bot.register_next_step_handler(message, CPU_frequency)

def CPU_frequency(message):
   print(message.text)
   bot.send_message(chat_id=message.chat.id, text='введите CPU_frequency')
   lpt.append(message.text)
   bot.register_next_step_handler(message, RAM_amount)

def RAM_amount(message):
   print(message.text)
   bot.send_message(chat_id=message.chat.id, text='введите RAM_amount')
   lpt.append(message.text)
   bot.register_next_step_handler(message, video_card)

def video_card(message):
   print(message.text)
   bot.send_message(chat_id=message.chat.id, text='введите video_card')
   lpt.append(message.text)
   bot.register_next_step_handler(message, drive_type)

def drive_type(message):
   print(message.text)
   bot.send_message(chat_id=message.chat.id, text='введите drive_type')
   lpt.append(message.text)
   bot.register_next_step_handler(message, drive_amount)

def drive_amount(message):
   print(message.text)
   bot.send_message(chat_id=message.chat.id, text='введите drive_amount')
   lpt.append(message.text)
   bot.register_next_step_handler(message, filial_id)

def filial_id(message):
   print(message.text)
   bot.send_message(chat_id=message.chat.id, text='введите filial_id')
   lpt.append(message.text)
   bot.register_next_step_handler(message, add_lpt)

def add_lpt(message):
   lpt.append(message.text)
   parametr = lpt
   
   response = requests.post(API_URL + 'laptop',json={
  "mark_id": int(parametr[0]),
  "model": parametr[1],
  "CPU": parametr[2],
  "CPU_cores": int(parametr[3]),
  "CPU_frequency": parametr[4],
  "RAM_amount": parametr[5],
  "video_card": parametr[6],
  "drive_type": parametr[7].upper(),
  "drive_amount": int(parametr[8]),
  "filial_id": int(parametr[9])
})
   print(response.status_code)
   lpt.clear()


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


@bot.callback_query_handler(func=lambda callback: True)
def callback_buttons(callback):
   if callback.data =='yes':
      bot.send_message(chat_id=callback.message.chat.id, text='Вы нажали ДА')
   elif callback.data =='no':
    bot.send_message(chat_id=callback.message.chat.id, text='Вы нажали ne')
   print(callback)    

def add_fil(message):
   response = requests.post(API_URL + 'filials',json={'filial':message.text,'isative':True})
   print(response.status_code)


bot.polling()
