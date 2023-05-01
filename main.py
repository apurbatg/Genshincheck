import os

import logging

from genshinstats import api as gsapi, spiral

from genshinstats.errors import GenshinStatsError

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# Set up logging

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',

                    level=logging.INFO)

# Define the command handlers

def start(update, context):

    """Send a welcome message when the command /start is issued."""

    update.message.reply_text('Hi! I am a Genshin Impact stats bot. Send me a player UID to get their stats!')

def help(update, context):

    """Send a help message when the command /help is issued."""

    update.message.reply_text('Send me a player UID to get their stats!')

def echo(update, context):

    """Search for the player with the given UID and display their stats."""

    uid = update.message.text

    try:

        player_data = gsapi.get_user_stats(uid)

        message = f"Stats for UID {uid}:\n"

        message += f"Adventure Rank: {player_data['stats']['level']}\n"

        message += f"Abyss Floor: {spiral.get_total_spiral_battles(uid)} (Highest: {spiral.get_highest_floor(uid)}F)\n"

        update.message.reply_text(message)

    except GenshinStatsError:

        update.message.reply_text("Player not found. Please check the UID and try again.")

def error(update, context):

    """Log the error message."""

    logging.error(f"Update {update} caused error {context.error}")

def main():

    """Start the bot."""

    # Get the Telegram bot token from the environment variable

    bot_token = os.environ.get('BOT_TOKEN')

    if bot_token is None:

        logging.error("Please set the BOT_TOKEN environment variable.")

        return

    # Set up the Telegram bot updater and dispatcher

    updater = Updater(bot_token, use_context=True)

    dp = updater.dispatcher

    # Add the command and message handlers

    dp.add_handler(CommandHandler('start', start))

    dp.add_handler(CommandHandler('help', help))

    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

    # Log all errors

    dp.add_error_handler(error)

    # Start the bot

    updater.start_polling()

    updater.idle()

if __name__ == '__main__':

    main()

