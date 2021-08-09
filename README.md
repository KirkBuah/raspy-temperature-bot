# raspy-temperature-bot

This is a telegram bot hosted by a raspberrypi equipped with a temperature and humidity sensor. The bot is capable of sending plots and readings.

The [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot) library was used to make the telegram bot.

## Installation

The following installation guide is divided in 2 parts.

#### Raspberry Pi setup

To make this project i used a Raspberry Pi Zero W with an AM2302 temperature and humidity sensor.


#### Telegram bot setup


## Structure

This project is composed of 3 main files:
- `bot.py` is used to host the telegram bot.
- `graph.py` contains the `Graph` class, used to make graphs.
- `sensor.py` contains the `TemperatureSensor` class, used to write and read from the sqlite3 database.

`bot.py` will call both the `Graph` and the `TemperatureSensor` classes.

## Usage

Once the bot is installed and running, send the `/start` command on telegram to receive a set of instructions.

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)
