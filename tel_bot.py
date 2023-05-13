import json
import logging
import os
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
    text = requests.get('http://127.0.0.1:8000/services')
    my = text.json()
    message.text = my['services']['services'][1]
    a = message.text
    await message.answer(a)


# @dp.message_handler(commands=['service'])
# @dp.message_handler(take_message_info)
# async def service_handler(message: types.Message, message_id, chat_id):
#     message.message_id = message_id
#     message.chat.id = chat_id
#     service = message.text.split(' ')[1]
#     response = requests.get('http://127.0.0.1:8000/services')
#     my = response.json()
#     await message.answer(text=my['services']['services'][service])


response = requests.get('http://127.0.0.1:8000/services')
my = response.json()
print(my['services']['services'][1])
if __name__ == '__main__':
    executor.start_polling(dp)

