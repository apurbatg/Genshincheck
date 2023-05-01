import telegram

import requests

from bs4 import BeautifulSoup

TOKEN = '6044506381:AAG3kiq3wmvg0EYAj3PiXkmaPm9uwUNU9yU' # replace this with your Telegram bot token

bot = telegram.Bot(token=TOKEN)

def start(update, context):

    context.bot.send_message(chat_id=update.effective_chat.id, text="Welcome to Genshin Stats Bot! Use /search <username> to search for a player's stats.")

def search(update, context):

    try:

        username = context.args[0]

        url = f'https://genshin.honeyhunterworld.com/db/char/{username}/'

        response = requests.get(url)

        soup = BeautifulSoup(response.content, 'html.parser')

        stats = soup.find_all('td', class_='ui-table__td')

        if not stats:

            context.bot.send_message(chat_id=update.effective_chat.id, text='Player not found!')

        else:

            name = stats[0].text

            level = stats[1].text

            element = stats[2].text

            weapon = stats[3].text

            constellation = stats[4].text

            context.bot.send_message(chat_id=update.effective_chat.id, text=f'Name: {name}\nLevel: {level}\nElement: {element}\nWeapon: {weapon}\nConstellation: {constellation}')

    except:

        context.bot.send_message(chat_id=update.effective_chat.id, text='Error. Please use /search <username> to search for a player\'s stats.')

updater = telegram.Updater(token=TOKEN, use_context=True)

updater.dispatcher.add_handler(telegram.CommandHandler('start', start))

updater.dispatcher.add_handler(telegram.CommandHandler('search', search))

updater.start_polling()

updater.idle()

