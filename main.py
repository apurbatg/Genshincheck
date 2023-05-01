import logging

import os

import telegram

from telegram.ext import Updater, CommandHandler

from genshinstats import GS

# Set up logging

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',

                    level=logging.INFO)

logger = logging.getLogger(__name__)

# Set up the Genshin Impact stats API wrapper

gs = GS(os.environ.get('GENSHIN_USERNAME'), os.environ.get('GENSHIN_PASSWORD'))

# Define a function to handle the /start command

def start(update, context):

    context.bot.send_message(chat_id=update.effective_chat.id, text="Hi there! Use /stats <username> to see Genshin Impact stats.")

# Define a function to handle the /stats command

def stats(update, context):

    # Get the player's username from the command argument

    username = context.args[0]

    # Fetch the player's stats

    try:

        player_stats = gs.get_user_stats(username)

    except Exception as e:

        logger.error(f"Error fetching stats for {username}: {e}")

        context.bot.send_message(chat_id=update.effective_chat.id, text=f"Error fetching stats for {username}. Please check if the username is correct and try again.")

        return

    # Create a formatted message with the player's stats

    message = f"Stats for {username}:\n\n"

    message += f"Adventure Rank: {player_stats['stats']['level']} ({player_stats['stats']['progress']}%)\n"

    message += f"Total Playtime: {player_stats['stats']['active_days']} days, {player_stats['stats']['active_hours']} hours\n"

    message += f"Abyssal Stars: {player_stats['stats']['spiral_abyss']['total_star']} stars\n"

    message += f"Anemoculus: {player_stats['exploration']['anemoculus']} / 65\n"

    message += f"Geoculus: {player_stats['exploration']['geoculus']} / 131\n"

    message += f"Daily Check-ins: {player_stats['stats']['total_sign_day']} / 180\n"

    message += f"Spiral Abyss Floor {player_stats['stats']['spiral_abyss']['highest_floor']} - {player_stats['stats']['spiral_abyss']['highest_room']}"

    # Send the message to the chat

    context.bot.send_message(chat_id=update.effective_chat.id, text=message)

# Set up the Telegram bot

bot = telegram.Bot(token=os.environ.get('TELEGRAM_TOKEN'))

updater = Updater(token=os.environ.get('TELEGRAM_TOKEN'), use_context=True)

dispatcher = updater.dispatcher

# Add the command handlers

dispatcher.add_handler(CommandHandler('start', start))

dispatcher.add_handler(CommandHandler('stats', stats))

# Start the bot

updater.start_polling()

# Keep the bot running until stopped manually

updater.idle()

