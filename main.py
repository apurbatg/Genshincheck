import telegram

from telegram.ext import Updater, CommandHandler

from genshinstats import GenshinStats

from genshinstats.errors import InvalidUID

TOKEN = '6270072880:AAFFspd4Blqglk__gGyHEJS1BdMml_dxr2M'

bot = telegram.Bot(token=TOKEN)

gs = GenshinStats()

def start(update, context):

    """Send a message when the command /start is issued."""

    update.message.reply_text('Welcome to the Genshin Impact Stats bot!')

def search(update, context):

    """Retrieve player stats when the command /search is issued."""

    args = context.args

    if len(args) == 0:

        update.message.reply_text('Please enter a player UID.')

    else:

        uid = args[0]

        try:

            stats = gs.get_user_stats(uid)

            update.message.reply_text(f'Player stats for UID {uid}: {stats}')

        except InvalidUID:

            update.message.reply_text('Invalid UID. Please enter a valid UID.')

def main():

    """Start the bot."""

    updater = Updater(TOKEN, use_context=True)

    dp = updater.dispatcher

    dp.add_handler(CommandHandler('start', start))

    dp.add_handler(CommandHandler('search', search))

    updater.start_polling()

    updater.idle()

if __name__ == '__main__':

    main()
