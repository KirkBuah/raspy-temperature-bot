#!/bin/python3

"""
First, a few callback functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.
Usage:
Example of a bot-user conversation using ConversationHandler.
Send /start to initiate the conversation.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""
import logging
import datetime
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler
from TOKEN import TOKEN
from temperature_twinx import temp_graph, load_obj
# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logger = logging.getLogger(__name__)

WHATSAPPSTATS, RECEIVER = range(2)


def start(update, context):
    user = update.message.from_user
    logger.info("%s issued /start command", user.first_name)
    update.message.reply_text(
        "Hello! I'm a simple bot, here are the commands you can issue me:\n\n/start, show this message again.\n/temperature, i will send you a temperature and humidity graph of the last 24 hours.\n/last_data, i will send you the last recorded data."
        )



def temperature(update,context):
    user = update.message.from_user
    logger.info("%s requested temperature graph", user.first_name)
    update.message.reply_text('Generating graph, please wait.')
    data = load_obj('./obj/temperature.json')
    timestr = datetime.datetime.strptime(list(data.keys())[-1],"%Y/%m/%d - %H:%M:%S").strftime('%Y/%m/%d at %H:%M')
    temperature = list(data.values())[-1][0]
    humidity = list(data.values())[-1][1]
    dewpoint = list(data.values())[-1][2][0]
    dewpointError = list(data.values())[-1][2][1]

    #make graphs
    temp_graph('./obj/temperature.json',24)
    logger.info("Temperature graphs generated, sending to %s.", user.first_name)
    update.message.reply_photo(photo=open('./tmp/temperature.png', 'rb'))
    logger.info("Temperature graph sent to %s.", user.first_name)

def LastRecordedT(update,context):
    user = update.message.from_user
    logger.info("%s requested last recorded data", user.first_name)
    data = load_obj('./obj/temperature.json')
    timestr = datetime.datetime.strptime(list(data.keys())[-1],"%Y/%m/%d - %H:%M:%S").strftime('%Y/%m/%d at %H:%M')
    temperature = list(data.values())[-1][0]
    humidity = list(data.values())[-1][1]
    dewpoint = list(data.values())[-1][2][0]
    dewpointError = list(data.values())[-1][2][1]
    update.message.reply_text("Last recorded data - {0}\n- temperature: {1:0.1f}±0.5°C\n- humidity: {2:0.1f}±2%\n- dew point: {3:0.1f}±{4:0.1f}°C".format(timestr,temperature,humidity,dewpoint,dewpointError))
    logger.info("Data sent to %s.", user.first_name)


def main():

    # Create the Updater and pass it your bot's token.
    updater = Updater(TOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Add conversation handler with the states GENDER, PHOTO, LOCATION and BIO
    start_handler = CommandHandler("start", start)
    temperature_handler = CommandHandler("temperature", temperature)
    LastRecordedT_handler = CommandHandler("last_data", LastRecordedT)
    dp.add_handler(start_handler)
    dp.add_handler(temperature_handler)
    dp.add_handler(LastRecordedT_handler)
    #start bot
    updater.start_polling()

    updater.idle()



if __name__ == '__main__':
    main()
