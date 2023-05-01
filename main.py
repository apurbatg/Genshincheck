import os

import requests

from telegram.ext import Updater, CommandHandler

def start(update, context):

    context.bot.send_message(chat_id=update.effective_chat.id, text="Welcome to the Genshin Impact stats bot! Type /stats <player_name> to get player stats.")

def stats(update, context):

    player_name = " ".join(context.args)
    
    server = "asia"

    api_url = f"https://api.wanshihe.com/genshin/stats?nickname={player_name}&server={server}"

    response = requests.get(api_url)

    if response.status_code == 200:

        stats = response.json()

        message = f"Stats for {player_name}:\nAdventure Rank: {stats['data']['stats']['level']} ({stats['data']['stats']['achievement_points']} achievement points)\nAnemoculus found: {stats['data']['world_exploration']['anemoculus']}\nGeoculus found: {stats['data']['world_exploration']['geoculus']}"

    else:

        message = f"Error fetching stats for {player_name}: {response.status_code} {response.reason}"

    context.bot.send_message(chat_id=update.effective_chat.id, text=message)

if __name__ == '__main__':

    TOKEN = os.environ.get('TOKEN')

    updater = Updater(token=TOKEN, use_context=True)

    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler('start', start))

    dispatcher.add_handler(CommandHandler('stats', stats))

    updater.start_polling()

    updater.idle()
