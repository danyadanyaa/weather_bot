import logging
import os
import requests

from dotenv import load_dotenv

from aiogram import Bot, Dispatcher, executor, types

load_dotenv()
API_TOKEN = os.getenv('tg_token')
token = os.getenv('token')

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    await message.reply("Этот бот подскажет тебе погоду. Введи название города что бы узнать погоду")


@dp.message_handler()
async def get_weather(message: types.Message):
    try:
        params = {
            'city': message.text,
            'format': 'json'
        }
        geocode = requests.get('https://nominatim.openstreetmap.org/search?', params=params).json()
        data = {
            'lat': geocode[0]['lat'],
            'lon': geocode[0]['lon'],
            'appid': token,
            'units': 'metric'
        }
        wthr = requests.get('https://api.openweathermap.org/data/2.5/weather', params=data).json()['main']
        await message.reply(
            f"Погода в {geocode[0]['display_name']}\n"
            f"Температура: {wthr['temp']}\n"
            f"Ощущается: {wthr['feels_like']}\n"
            f"Влажность: {wthr['humidity']}\n"
            f"Давление: {wthr['pressure']} мм.рт.ст."
        )
        await bot.send_location(message.chat.id, latitude=geocode[0]['lat'], longitude=geocode[0]['lon'])
    except:
        await message.reply('Такой город не найден')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)