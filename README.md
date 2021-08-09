# raspy-temperature-bot

This is a telegram bot hosted by a Raspberry Pi equipped with a temperature and humidity sensor. The bot is capable of sending plots and readings.

The [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot) library was used to make the telegram bot.

## Installation

The following installation guide is divided in 3 phases.

#### Raspberry Pi setup

To make this project i used a Raspberry Pi Zero W with an AM2302 temperature and humidity sensor.

The humidity sensor has 3 pins:
- DATA, connected to the GPIO 4 port, it sends the readings to the Raspberry Pi.
- GROUND, connected to one of the ground ports.
- VCC, connected to one of the 5V ports.

![gpio pinout](https://www.etechnophiles.com/wp-content/uploads/2020/12/R-Pi-Zero-Pinout.jpg?ezimgfmt=ng%3Awebp%2Fngcb40%2Frs%3Adevice%2Frscb40-1)

Once your sensor is connected to your Raspberry Pi, go ahead and proceed to [install](https://www.raspberrypi.org/software/) a clean version of Raspberry Pi OS Lite.

#### raspy-temperature-bot installation

To install raspy-temperature-bot:
1. Ssh into your Raspberry Pi
```bash
ssh pi@raspberrypi.local
```
2. Clone the repository
```bash
git clone https://github.com/Kirgnition/raspy-temperature-bot.git
```
3. Paste your [bot token](https://core.telegram.org/bots#6-botfather) in the `TOKEN.py` file
4. 

#### Telegram bot setup


## Structure

This project is composed of 3 main files:
- `bot.py` is used to host the telegram bot.
- `graph.py` contains the `Graph` class, used to make graphs.
- `sensor.py` contains the `TemperatureSensor` class, used to write and read from the sqlite3 database.

`bot.py` will call both the `Graph` and `TemperatureSensor` classes.

## Usage

Once the bot is installed and running, send the `/start` command on telegram to receive a set of instructions.

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)
