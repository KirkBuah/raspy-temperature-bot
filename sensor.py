import datetime
import time
import Adafruit_DHT as ada
import sqlite3
from sqlite3 import Error


class TemperatureSensor:
    def __init__(self):
        # Initialize the dht device
        self.DHT_SENSOR = ada.DHT22
        self.DHT_PIN = 4

    def read_sensor(self, timezone=1):
        # Define humidity and temperature as None for the loop
        humidity = None
        temperature = None

        # Keep trying to read temperature and humidity (sometimes it doesn't work with dht)
        while humidity is not None and temperature is not None:
            humidity, temperature = ada.read_retry(self.DHT_SENSOR, self.DHT_PIN)

        # Return temperature, humidity and time of reading in epoch time
        return temperature, humidity, (datetime.datetime.now() + datetime.timedelta(hours=timezone)).timestamp()

    def connect_to_db(self, db):
        # The data from the sensor is stored in an SQLite database

        # Create database
        connection = None
        try:
            connection = sqlite3.connect(db)
        except Error as err:
            print(err)

        # Create a table
        # temperature and humidity will be stored as real numbers, date will be stored as unix epoch time
        c = connection.cursor()
        c.execute(
            """CREATE TABLE IF NOT EXISTS data (temperature real, humidity real, date integer);"""
        )

        return connection

    def write_to_db(self, data, connection):
        # Write data into the database (temperature, humidity and date)
        params = (data[0], data[1], data[2])
        sql = f"""INSERT INTO data(temperature, humidity, date) VALUES (?,?,?)"""
        c = connection.cursor()
        # Execute command using parameters
        c.execute(sql, params)
        # Commit to db
        connection.commit()

    def read_from_db(self, n, connection):
        # Read the last n lines from the database
        c = connection.cursor()
        c.execute(f"SELECT * FROM data ORDER BY rowid DESC LIMIT {n}")

        rows = c.fetchall()
        # Return rows as list of tuples: [(temp,hum,date),(...),...]
        # from most the furthest date to the most recent
        return rows


if __name__ == "__main__":
    ts = TemperatureSensor()
    conn = ts.connect_to_db("./sqlite_db.db")

    while True:
        try:
            # Read sensor and write to db every 5 minutes
            data = ts.read_sensor()
            ts.write_to_db(data, conn)
            time.sleep(300)
        except Exception as e:
            conn.close()
            print("database connection has been terminated")
            print(e)
            exit()
