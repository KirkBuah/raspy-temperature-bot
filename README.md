# raspy-temperature-bot

**Note: This project is currently not maintained.**

This is a telegram bot hosted by a Raspberry Pi equipped with a temperature and humidity sensor. The bot is capable of sending plots and readings.  

![graph example](https://i.imgur.com/YO6baGM.jpeg)


## Structure

This project is composed of 3 main files:
- `bot.py` is used to host the telegram bot.
- `graph.py` contains the `Graph` class, used to make graphs.
- `sensor.py` contains the `TemperatureSensor` class, used to write and read from the sqlite3 database, as well as the
function that reads the temperature and humidity values from the sensor.

`bot.py` will call both the `Graph` and `TemperatureSensor` classes.


## Installation

### Dependencies

- [Adafruit_DHT](https://github.com/adafruit/Adafruit_Python_DHT)
- [matplotlib](https://matplotlib.org/stable/users/installing.html)
- [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot)

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

3. cd into the repository and install the requirements.
```bash
cd ./raspy-temperature-bot
pip3 install -r ./requirements.txt
```

4. Paste your [bot token](https://core.telegram.org/bots#6-botfather) in the `TOKEN.py` file.

5. Create a service for the temperature sensor:
   1. Create a file called `temperature_sensor.service`:
      ```bash
      sudo nano /etc/systemd/system/temperature_sensor.service
      ```
   2. Paste the following:
      ```
      [Unit]
      Description=ROT13 demo service
      After=network.target
      StartLimitIntervalSec=0
      
      [Service]
      Type=simple
      Restart=always
      RestartSec=1
      User=username
      ExecStart=python3 /path/to/sensor.py

      [Install]
      WantedBy=multi-user.target
      ```
      Set your username after `User=` and the path to `sensor.py` after `ExecStart=`.

   3. Enable the service by issuing on the terminal:
      ```bash
      systemctl start temperature_sensor.service
      systemctl enable temperature_sensor.service
      ```
      From the moment you start the service a reading will be taken by the sensor every 5 minutes and saved in a
      sqlite3 database.

6. Create a service for the telegram bot in an analogous way.

Your bot should be now active, in case of restart both the bot and the sensor will start automatically.

## Usage

Once the bot is installed and running, send the `/start` command on telegram to receive the list of available commands.

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.


## License
[MIT](https://choosealicense.com/licenses/mit/)
