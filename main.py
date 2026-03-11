import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
import requests

# Мои ключи
TOKEN = ''
API_KEY = ''
URL = 'https://api.openweathermap.org/data/2.5/weather'

# Эмодзи для разной погоды
EMOJI_CODE = {
    800: '☀️',
    801: '🌤️',
    802: '⛅',
    803: '☁️',
    804: '☁️',
    200: '⛈️',
    300: '🌦️',
    500: '🌧️',
    600: '❄️',
    701: '🌫️',
    900: '🌪️'
}

bot = telebot.TeleBot(TOKEN)

# Клавиатура
keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
btn_loc = KeyboardButton('Получить погоду', request_location=True)
btn_about = KeyboardButton('О проекте')
keyboard.add(btn_loc)
keyboard.add(btn_about)


def get_weather(lat, lon):
    params = {
        'lat': lat,
        'lon': lon,
        'lang': 'ru',
        'units': 'metric',
        'appid': API_KEY
    }

    try:
        resp = requests.get(URL, params=params).json()

        if resp.get('cod') != 200:
            return f"😕 Ошибка: {resp.get('message', 'Не удалось получить погоду')}"

        city = resp['name']
        desc = resp['weather'][0]['description']
        code = resp['weather'][0]['id']
        temp = resp['main']['temp']
        feels = resp['main']['feels_like']
        hum = resp['main']['humidity']

        emoji = EMOJI_CODE.get(code, '🌡️')

        msg = f"Погода в: {city}\n"
        msg += f"{emoji} {desc.capitalize()}.\n"
        msg += f"Температура: {temp}°C.\n"
        msg += f"Ощущается как: {feels}°C.\n"
        msg += f"Влажность: {hum}%."

        return msg
    except Exception as e:
        return f"Что-то пошло не так: {e}"


@bot.message_handler(commands=['start'])
def send_welcome(message):
    text = "Отправь мне свое местоположение, и я скажу погоду рядом."
    bot.send_message(message.chat.id, text, reply_markup=keyboard)


@bot.message_handler(content_types=['location'])
def send_weather(message):
    lon = message.location.longitude
    lat = message.location.latitude

    result = get_weather(lat, lon)
    bot.send_message(message.chat.id, result, reply_markup=keyboard)


@bot.message_handler(regexp='О проекте')
def send_about(message):
    text = "Бот Погоды для Кода Будущего\n"
    text += "Сделал Гриша\n"
    text += "Всем солнечной погоды"
    bot.send_message(message.chat.id, text, reply_markup=keyboard)


if __name__ == '__main__':
    print("Бот запущен...")
    bot.infinity_polling()