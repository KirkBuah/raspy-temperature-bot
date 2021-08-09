import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
from graph import Graph
from TOKEN import TOKEN

# Enable logging
# Create log file
logging.basicConfig(format="format='%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                    level=logging.INFO,
                    filename="./logfile.log",
                    filemode='a')

logger = logging.getLogger(__name__)


def start(update: Update, context: CallbackContext):
    # Send welcome message
    update.message.reply_text("Welcome, here is a list of the available commands:\n"
                              "/start, displays this message.\n"
                              "/temperature_graph <hours>, sends a graph of the last <> hours (24 hours if left blank).\n"
                              "/last_readings, sends the last taken readings (humidity, temperature and dew point).")

    # Update logfile
    user = update.message.from_user
    logging.info(f"issued the /start command (id: {user.id}, first_name: {user.first_name}, last_name: {user.last_name}, username: {user.username})")


def temperature_graph(update: Update, context: CallbackContext):
    # Sends a graph of the last 24h

    # Get hours to be displayed in the graph
    # If not given any, keep 24 hours
    try:
        hours = int(context.args[0])
    except (IndexError, ValueError):
        hours = 24

    update.message.reply_text("Generating graph, please wait.")
    Graph(hours).make_graph()
    update.message.reply_photo("./tmp/temperature.png")

    # Update logfile
    user = update.message.from_user
    logging.info(f"sent temperature graph of the last ({hours}) hours to (id: {user.id}, first_name: {user.first_name}, last_name: {user.last_name}, username: {user.username})")


def last_readings(update: Update, context: CallbackContext):
    # Sends the last readings
    # Get last readings from database (1/12 means only the last reading)
    data = Graph(1/12)

    timestr = data.dates[0].datetime.strftime('%Y/%m/%d at %H:%M')
    temperature = data.temperature[0]
    humidity = data.humidity[0]
    dewpoint = data.dewpoint[0]

    # Send message
    update.message.reply_text(
        "Last recorded data - {0}\n"
        "- temperature: {1:0.1f}±0.5°C\n"
        "- humidity: {2:0.1f}±2%\n"
        "- dew point: {3:0.1f}°C".format(timestr, temperature, humidity, dewpoint)
    )

    # Update logfile
    user = update.message.from_user
    logging.info(f"sent last readings to (id: {user.id}, first_name: {user.first_name}, last_name: {user.last_name}, username: {user.username})")


def main():
    # Run bot

    # Create an updater with the bot's token
    updater = Updater(TOKEN)

    # Get dispatcher
    dispatcher = updater.dispatcher

    # Define different commands
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("temperature_graph", temperature_graph))
    dispatcher.add_handler(CommandHandler("last_readings", last_readings))

    # Start bot
    updater.start_polling()

    logging.info("Bot started")

    updater.idle()


if __name__ == "__main__":
    main()