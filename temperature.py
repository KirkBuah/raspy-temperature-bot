#!/bin/python3
import time, datetime, json
import Adafruit_DHT as ada
import numpy as np

# Initial the dht device, with data pin connected to:
DHT_SENSOR = ada.DHT22
DHT_PIN = 4

# you can pass DHT22 use_pulseio=False if you wouldn't like to use pulseio.
# This may be necessary on a Linux single board computer like the Raspberry Pi,
# but it will not work in CircuitPython.
# dhtDevice = adafruit_dht.DHT22(board.D18, use_pulseio=False)
tempdict = {}


def save_obj(obj):
    with open('./obj/temperature.json','r+') as f:
        dic = json.load(f)
        dic.update(obj)
        f.seek(0)
        json.dump(dic, f)

def load_obj(filepath):
    with open('./obj/temperature.json', 'r') as fp:
        data = json.load(fp)
    return data

def readSensor():
    humidity, temperature = ada.read_retry(DHT_SENSOR, DHT_PIN)
    return humidity,temperature

def write():
    print('Temperature = {0:0.1f}°C  Humidity = {1:0.1f}%'.format(temperature, humidity))
    date_time = (datetime.datetime.now()+datetime.timedelta(hours=1)).strftime('%Y/%m/%d - %H:%M:%S')

    b = 17.368
    c = 238.88

    gamma = np.log(humidity/100)+1/((c/(b*temperature)+1/b))
    dewpoint = 1/((b/c*gamma)-1/c)

    sigmaGamma = np.sqrt(((2/humidity)**2)+(((0.5/temperature)*(1/((c/b*temperature)+(1/b))))**2))
    dewpointError = (sigmaGamma/gamma)*(1/((b/c*gamma)-1/c))

    tempdict[date_time] = [temperature, humidity, [dewpoint,dewpointError]]
    save_obj(tempdict)


while True:
    humidity, temperature = readSensor()
    while humidity is not None and temperature is not None:
        write()
        time.sleep(5*60)
        break
