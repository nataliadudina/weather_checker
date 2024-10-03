import asyncio
import logging
import os

import requests
from datetime import datetime

from aiogram.filters import CommandStart
from dotenv import load_dotenv

from aiogram import Bot, Dispatcher
from aiogram.types import Message

from utils import get_random_goodbye

load_dotenv()

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)

tg_bot_token = os.getenv('TGBOT_TOKEN')  # Токен для бота в Telegram
weather_token = os.getenv('OPEN_WEATHER_TOKEN')  # Токен для OpenWeatherMap API

# Создание экземпляров Bot и Dispatcher
bot = Bot(token=tg_bot_token)
dp = Dispatcher()


# Обработчик команды /start
@dp.message(CommandStart())
async def command_start_handler(message: Message):
    await message.answer("Hello! Enter a city name and get the latest weather update! \U0001F913")


# Обработчик для получения погоды
@dp.message()
async def get_weather(message: Message):
    logger.info(f"Received message: {message.text}")

    # Словарь для перевода кодов погодных условий в эмодзи
    code_pics = {
        'Clear': 'Clear \U00002600',
        'Clouds': 'Cloudy \U00002601',
        'Rain': 'Rain \U00002614',
        'Drizzle': 'Drizzle \U00002614',
        'Thunderstorm': 'Thunderstorm \U000026A1',
        'Snow': 'Snow \U0001F328',
        'Mist': 'Mist \U0001F32B',
    }

    try:
        # Вызов API OpenWeatherMap для получения данных о погоде
        weather_call = requests.get(
            f"https://api.openweathermap.org/data/2.5/weather?q={message.text}&appid={weather_token}&units=metric"
        )
        data = weather_call.json()

        # Извлечение информации о погоде
        city = data['name']
        temp = data['main']['temp']
        wind = data['wind']['speed']
        humidity = data['main']['humidity']
        sunrise = datetime.fromtimestamp(data['sys']['sunrise']).strftime("%H:%M")
        sunset = datetime.fromtimestamp(data['sys']['sunset']).strftime("%H:%M")
        weather = data['weather'][0]['main']

        # Определение эмодзи для текущих погодных условий
        default = 'Hard to define \U0001F914'
        pic = code_pics.get(weather, default)

        # Формирование ответа с информацией о погоде
        await message.answer(
            f'*** {datetime.now().strftime("%d.%m.%Y")} ***\n'
            f'City: {city}\n'
            f'Temperature: {int(temp)} C° - {pic}\n'
            f'Wind: {wind} m/s\n'
            f'Humidity: {humidity}%\n'
            f'Sunrise at {sunrise}\n'
            f'Sunset at {sunset}\n'
            f'***\n'
            f'{get_random_goodbye()} \U00002665'
        )
    except Exception:
        # Отправка сообщения об ошибке, если что-то пошло не так
        await message.answer("\U00002620 Check your spelling. \U00002620")


# Асинхронная функция для запуска бота
async def main() -> None:
    await dp.start_polling(bot)

# Запуск бота
if __name__ == "__main__":
    asyncio.run(main())
