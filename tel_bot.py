import json
import logging
import os

from aiogram.types import ReplyKeyboardMarkup
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, executor, types
import requests

load_dotenv()
TOKEN = os.getenv('TOKEN')
logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['add'])
async def set_commands(message: types.Message):
    command = types.BotCommand(command=message.text.split(' ')[1], description=message.text.split(' ')[2])
    commands = await bot.get_my_commands()
    commands.append(command)
    await message.reply(f'Команда {command.command} додана до меню бота')
    await bot.set_my_commands(commands)


@dp.message_handler(commands=['about'])
async def show_commands(message: types.Message):
    commands = await bot.get_my_commands()
    if commands:
        commands_list = [f'{command.command} - {command.description}' for command in commands]
        text = '\n'.join(commands_list)
        await message.answer(text)
    else:
        await message.answer('None')


@dp.message_handler(commands=['del'])
async def delete_command_handler(message: types.Message):
    command_name = message.text.split(' ')[1]
    commands = await bot.get_my_commands()
    commands = [command for command in commands if command.command != command_name]
    await bot.set_my_commands(commands)
    await message.reply(f'Команда {command_name} видалена з меню бота')


@dp.message_handler(commands=['all_services'])
async def services_handler(message: types.Message):
    services_keyboard = ReplyKeyboardMarkup()
    text = requests.get('http://127.0.0.1:8000/services')
    my = text.json()
    all_services = my['services']['services']
    for i in all_services:
        services_keyboard.insert(i['name'])
    await message.reply(f"services {message}", reply_markup=services_keyboard)


@dp.message_handler(commands=['service'])
async def service_handler(message: types.Message):
    info = message.text.split(' ')[1]
    text = requests.get('http://127.0.0.1:8000/services')
    my = text.json()
    message.text = my['services']['services'][int(info)]
    a = message.text
    await message.reply(a)


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    name = message.chat.first_name
    await message.reply(f"Hi {name}! I'm bot for tonAI!")

# @dp.message_handler(lambda message: message.text == 'foo')
# async def send_response(message: types.Message):
#     message.text = text
#     message.message_id = message_id
#     print(message)
#     await message.answer(message.text)


async def take_message_info(message: types.Message):
    message_id = message.message_id
    chat_id = message.chat.id
    text = message.text
    return {'message_id': message_id, 'chat_id': chat_id, 'text': text}


@dp.message_handler(take_message_info)
async def my_message_handler(message: types.Message, text, chat_id, message_id):
    message.message_id = message_id
    message.chat.id = chat_id
    message.text = text
    all_services = requests.get('http://127.0.0.1:8000/services')
    my = all_services.json()
    for i in my['services']['services']:
        if i['name'] == text:
            await message.reply(text)


if __name__ == '__main__':
    executor.start_polling(dp)

