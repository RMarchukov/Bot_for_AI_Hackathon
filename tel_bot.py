import os
import requests
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, executor, types


load_dotenv()
TOKEN = os.getenv('TOKEN')

bot = Bot(token=TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    name = message.chat.first_name
    await message.answer(f"Hi {name}! I'm bot for tonAI!")
    await services_handler(message)

# @dp.message_handler(commands=['add'])
# async def set_commands(message: types.Message):
#     command = types.BotCommand(command=message.text.split(' ')[1], description=message.text.split(' ')[2])
#     commands = await bot.get_my_commands()
#     commands.append(command)
#     await message.reply(f'Команда {command.command} додана до меню бота')
#     await bot.set_my_commands(commands)

@dp.message_handler(commands=['help'])
async def show_commands(message: types.Message):
    commands = await bot.get_my_commands()
    if commands:
        commands_list = [f'{command.command} - {command.description}' for command in commands]
        text = '\n'.join(commands_list)
        await message.answer(text)
    else:
        await message.answer('None')


# @dp.message_handler(commands=['del'])
# async def delete_command_handler(message: types.Message):
#     command_name = message.text.split(' ')[1]
#     commands = await bot.get_my_commands()
#     commands = [command for command in commands if command.command != command_name]
#     await bot.set_my_commands(commands)
#     await message.answer(f'Команда {command_name} видалена з меню бота')


class Form(StatesGroup):
    service = State()
    text = State()
    params = State()


async def get_data():
    services = {}
    response = requests.get('http://127.0.0.1:8000/services')
    g = response.json()
    all_services = g['services']['services']
    count = 0
    for i in all_services:
        services.update({count: {i["name"]: i["id"]}})
        count += 1
    return services


@dp.message_handler(commands=['all_services'])
async def services_handler(message: types.Message):
    services_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    our = await get_data()
    for k, v in our.items():
        for i in v.keys():
            services_keyboard.insert(i)
    services_keyboard.add('/cancel')
    await Form.service.set()
    await message.answer('Choose your service!', reply_markup=services_keyboard)


@dp.message_handler(state='*', commands=['cancel'])
async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.answer('Cancelled.', reply_markup=types.ReplyKeyboardRemove())


@dp.message_handler(state=Form.service)
async def process_name(message: types.Message, state: FSMContext):
    number = 0
    our = await get_data()
    for k, v in our.items():
        for i in v.keys():
            if i == message.text:
                number = k
                break

    response = requests.get('http://127.0.0.1:8000/services')
    g = response.json()
    list_of_params = []
    count = 0
    if g['services']['services'][number]['params']['required'] is None:
        print('There are not any main parameters.')

    for i in g['services']['services'][number]['params']['required']:
        list_of_params.append(f'{i["name"]}_main')
        count += 1
    if message.text not in g['services']['services'][number]['name']:
        return await message.answer("There is not this service. Choose service from buttons.")
    else:
        if g['services']['services'][number]['params'] is not None:
            if g['services']['services'][number]['params']['optional'] is None:
                print('There are not any optional parameters.')
            else:
                count = 0
                for i in g['services']['services'][number]['params']['optional']:
                    list_of_params.append(f"{i['name']}_optional")
                    count += 1

    async with state.proxy() as data:
        data['service'] = message.text
        data['params'] = list_of_params
    markup = types.ReplyKeyboardMarkup().insert(types.KeyboardButton('/cancel'))
    await Form.next()
    param = ', ~'.join(list_of_params)
    await message.answer(f"Enter your params. Use comma and space between parameters: ~{param}", reply_markup=markup)


@dp.message_handler(state=Form.text)
async def process_gender(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['text'] = message.text
        our = await get_data()
        for k, v in our.items():
            for i, b in v.items():
                if i == data['service']:
                    my_id = b

        markup = types.ReplyKeyboardRemove()
        result = data['text'].split(', ')
        count = 1
        a = {}
        for i in result:
            a.update({f'{count}': i})
            count += 1

        payload = {'service_id': my_id}
        count = 1
        for i in data['params']:
            if i[-1] == 'n':
                u = i[0:-5]
                payload[f'{u}'] = a.get(f'{count}')
            else:
                u = i[0:-9]
                payload[f'{u}'] = a.get(f'{count}')
            count += 1

        info = requests.post(f'http://127.0.0.1:8000/services/{my_id}', json=payload)
        a = info.json()
        await message.answer(f"{a}", reply_markup=markup)
    await state.finish()

# @dp.callback_query_handler(lambda callback: True)
# async def choice_market_callback(callback: types.CallbackQuery):
#     data = callback.data
#     chat_id = callback.message.chat.id
#     await bot.send_message(chat_id=chat_id, text=data)

# @dp.message_handler(lambda message: message.text == 'foo')
# async def send_response(message: types.Message):
#     message.text = text
#     message.message_id = message_id
#     print(message)
#     await message.answer(message.text)

async def take_message_info(message: types.Message):
    text = message.text
    return {'text': text}


@dp.message_handler(take_message_info)
async def my_message_handler(message: types.Message, text):
    message.text = f"{text} it is your message. You can use command: /all_services for use this bot."
    await message.answer(message.text)


if __name__ == '__main__':
    executor.start_polling(dp)
