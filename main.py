import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from telegram.error import (TelegramError, BadRequest,
                            TimedOut, NetworkError)
from screenshot_maker import make_image
from url_helpers import format_url, validate_url
import os


# getting telegram TOKEN from configs
try:
    # you may create config file with TG_TOKEN variable as your token
    import config
    TOKEN = config.TG_TOKEN
# also you may add the token to your system variables
except ModuleNotFoundError:
    TOKEN = os.environ.get("TG_TOKEN")
except AttributeError:
    TOKEN = os.environ.get("TG_TOKEN")

# or simply add your telegram token here:
# TOKEN = "your token"

# Enable logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

logger = logging.getLogger(__name__)


def error_callback(update, context):
    try:
        raise context.error
    except BadRequest:
        # handle malformed requests - read more below!
        update.message.reply_text('Could not make a screenshot of this website. Please try a different one.')
    except TimedOut:
        # handle slow connection problems
        update.message.reply_text('TimedOut')
    except NetworkError:
        # handle other connection problems
        update.message.reply_text('NetworkError')
    except TelegramError:
        # handle all other telegram related errors
        update.message.reply_text('TelegramError')


# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    update.message.reply_text('Welcome to our channel! Type a website address to receive its screenshot.')


def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text('Type a website address to receive its screenshot. The address must be in valid format '
                              '(e.g: www.google.com, https://www.google.com).')


def image(update: Update, context: CallbackContext) -> None:
    """
    This function check if URL is valid, make a screenshot of the webpage, and send it to user.
    """
    url = update.message.text
    url = format_url(url)
    if validate_url(url):
        update.message.reply_text('Processing your request. This may take up to a minute. Please wait.')
        file_name = make_image(url)
        update.message.reply_photo(photo=open(file_name, 'rb'))
    else:
        update.message.reply_text("Please try a valid website address (e.g: www.google.com, https://www.google.com)")


def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater(TOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    dispatcher.add_error_handler(error_callback)
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))

    # on noencommand assume it is a website address and try to make a screenshot
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, image))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
