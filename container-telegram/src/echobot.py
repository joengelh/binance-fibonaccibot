#!/usr/bin/env python
# pylint: disable=C0116,W0613
# This program is dedicated to the public domain under the CC0 license.

"""
Simple Bot to reply to Telegram messages.

First, a few handler functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.

Usage:
Basic Echobot example, repeats messages.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

from envs import env
import redis
import logging
import os

from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments update and
# context.
def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    update.message.reply_markdown_v2(
        fr'Hi {user.mention_markdown_v2()}\!',
        reply_markup=ForceReply(selective=True),
    )


def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')


def echo(update: Update, context: CallbackContext) -> None:
    """Echo the user message."""
    try:
        POSTGRES_PASSWORD=env('POSTGRES_PASSWORD')
        dbHost=env('dbHost')
    except KeyError:
        print("No env variables set.")
        sys.exit(1)
    # Login with redis Cache
    r = redis.Redis(host=dbHost,
        port=6379,
        db=0,
        password=POSTGRES_PASSWORD)
    redisReply = ("openTrades: " + r.get("openTrades").decode('utf-8') + "\n" +
             "simulatedSum: " + r.get("simulatedSum").decode('utf-8') + "\n" +
             "sumResult: " + r.get("sumResult").decode('utf-8')) 
    update.message.reply_text(redisReply)


def main() -> None:
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    try:
        botToken=env('botToken')
    except KeyError:
        print("No env variables set.")
        sys.exit(1)

    # Login to Bot
    updater = Updater(botToken)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))

    # on non command i.e message - echo the message on Telegram
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
