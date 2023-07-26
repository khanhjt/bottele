import random
import requests
import telebot
import wikipedia
from googletrans import Translator
from openweathermap import OpenWeatherMap
from wikipedia import Wikipedia
from pyjokes import get_jokes
from tqdm import tqdm

bot = telebot.TeleBot('6578230278:AAHGSCHqfQmHOxeP1yJMjfDSOIr3yOZTQ8U')

@bot.message_handler(commands=['translate'])
def translate_message(message):
    language = message.text.split()[1]
    text = message.text.split()[2]
    translator = Translator()
    translated_text = translator.translate(text, dest=language)
    bot.send_message(message.chat.id, translated_text)


@bot.message_handler(commands=['weather'])
def get_weather(message):
    city = message.text.split()[1]
    url = 'https://api.openweathermap.org/data/2.5/weather?q=' + city + '&appid=YOUR_API_KEY&units=metric'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        weather = data['weather'][0]
        temperature = data['main']['temp']
        humidity = data['main']['humidity']
        wind_speed = data['wind']['speed']
        bot.send_message(message.chat.id, 'The weather in ' + city + ' is:' + '\n' + '* Temperature: ' + str(
            temperature) + '°C' + '\n' + '* Humidity: ' + str(humidity) + '%' + '\n' + '* Wind speed: ' + str(
            wind_speed) + 'm/s')
    else:
        bot.send_message(message.chat.id, 'Error getting weather information for ' + city)


@bot.message_handler(commands=['wikipedia'])
def get_wikipedia_info(message):
    query = message.text.split()[1]
    response = wikipedia.summary(query, sentences=2)
    bot.send_message(message.chat.id, response)


@bot.message_handler(commands=['joke'])
def get_joke(message):
    joke = get_jokes()
    bot.send_message(message.chat.id, joke)


@bot.message_handler(commands=['meme'])
def get_meme(message):

    url = "https://www.reddit.com/r/memes/top/.json?limit=100"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        memes = data['data']['children']
        meme = memes[random.randint(0, len(memes) - 1)]['data']
        bot.send_message(message.chat.id, meme['url'])
    else:
        bot.send_message(message.chat.id, 'Error getting meme')


bot.polling()
