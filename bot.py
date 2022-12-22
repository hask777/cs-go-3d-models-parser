from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text
from aiogram.utils.markdown import hbold, hlink
from main import collect_data
import json
import os
import time

bot = Bot(token='5927159558:AAFslDjCx3gFsP9lUFtpoQFDVDw8ZdmPxzc', parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)

@dp.message_handler(commands='start')
async def start(message: types.Message):
    start_buttons = ['Ножи', 'Перчатки', 'Снайперские винтовки']
    keyboard = types.ReplyKeyboardMarkup()
    keyboard.add(*start_buttons)

    await message.answer('Выберете категорию', reply_markup=keyboard)

@dp.message_handler(Text(equals='Ножи'))
async def get_discount_knifes(message: types.Message):
    await message.answer('Please waiting ...')

    collect_data()

    with open('result.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    for index, item in enumerate(data):
        card = f'{hlink(item.get("full_name"), item.get("3d"))}\n' \
            f'{hbold("Скидка: ")}{item.get("discount")}\n'\
            f'{hbold("Цена: ")}${item.get("price")}'

        print(card)
        
        if index % 20 == 0:
            time.sleep(3)

        await message.answer(card)




def main():
    executor.start_polling(dp)

if __name__ == '__main__':
    main()
