import logging

import requests

from telegram.ext import Updater, CommandHandler

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',

                    level=logging.INFO)

logger = logging.getLogger(__name__)

def start(update, context):

    """Send a message when the command /start is issued."""

    context.bot.send_message(chat_id=update.effective_chat.id, text='Hi! I am a Genshin Impact stats bot. Use /stats <player_name> <server> to see a player\'s stats.')

def stats(update, context):

    """Fetch player stats and send them as a message."""

    if not context.args:

        context.bot.send_message(chat_id=update.effective_chat.id, text="Please enter a player name and server. Usage: /stats <player_name> <server>")

        return

    

    player_name = context.args[0]

    valid_servers = ["america", "europe", "asia"]

    server = context.args[-1].lower()

    

    if server not in valid_servers:

        context.bot.send_message(chat_id=update.effective_chat.id, text="Invalid server code. Valid codes are: america, europe, asia")

        return

    

    try:

        response = requests.get(f'https://api.genshin.dev/players/{player_name}/stats?server={server}')

        response.raise_for_status()

    except requests.exceptions.RequestException as e:

        context.bot.send_message(chat_id=update.effective_chat.id, text=f"Error fetching stats for {player_name}: {e}")

        logger.error(f"Error fetching stats for {player_name}: {e}")

        return

    

    if response.status_code == 200:

        stats = response.json()

        if not stats['data']:

            message = f"Error: player {player_name} not found on {server.capitalize()} server"

        else:

            message = f"Stats for {player_name}:\nAdventure Rank: {stats['data']['stats']['level']} ({stats['data']['stats']['achievement_points']} achievement points)\nAnemoculus found: {stats['data']['world_exploration']['anemoculus']}\nGeoculus found: {stats['data']['world_exploration']['geoculus']}"

    else:

        message = f"Error fetching stats for {player_name}: {response.status_code} {response.reason}"

    

    context.bot.send_message(chat_id=update.effective_chat.id, text=message)

def help_command(update, context):

    """Send a message when the command /help is issued."""

    commands = ['/start', '/stats <player_name> <server>']

    help_text = "Here are the available commands:\n"

    for command in commands:

        help_text += f"{command}\n"

    context.bot.send_message(chat_id=update.effective_chat.id, text=help_text)

def main():

    """Start the bot."""

    TOKEN = '6044506381:AAHrrqTk02jqPtIzHjdCbOzz3S1cZIv7Cx4'

    # Create the Updater and pass it the bot's token.

    updater = Updater(token=TOKEN, use_context=True)

    # Add command handlers

    updater.dispatcher.add_handler(CommandHandler('start', start))

    updater.dispatcher.add_handler(CommandHandler('stats', stats))

    updater.dispatcher.add_handler(CommandHandler('help', help_command))

    # Start the bot

    updater.start_polling()

    logger.info("Bot started")

    updater.idle()

if __name__ == '__main__':

    main()

