import lcddriver
import time
from datetime import datetime
import Adafruit_DHT
import sqlite3
import schedule
import sys
from BMP180 import BMP180


class SensorReader():

    def __init__(self, dbPath, dhtPin):
        self.bmpSensor = BMP180()
        self.display = None  # lcddriver.lcd()
        self.dhtSensor = Adafruit_DHT.DHT22
        self.dhtPin = dhtPin
        self.pressure, self.temperature, self.humidity = 0, 0, 0
        try:
            self.dbConnection = sqlite3.connect(dbPath)
        except sqlite3.Error as E:
            print("failed by {}".format(E))
            sys.exit(-1)

    def sensBMP(self):
        pres = 0
        temp = 0
        for i in range(0, 10):
            pres += self.bmpSensor.read_pressure()
            temp += self.bmpSensor.read_temperature()
        pres /= 10
        temp /= 10
        return pres, temp

    def sensDHT(self):
        humi = 0
        temp = 0
        for i in range(0, 10):
            humi1, temp1 = Adafruit_DHT.read_retry(self.dhtSensor, self.dhtPin)
            humi += humi1
            temp += temp1
        humi /= 10
        temp /= 10
        return humi, temp

    def create_log(self, err, code):
        with open('err.log', 'w') as file:
            if code == 1:
                file.write("РѕС€РёР±РєР° СЃ С‡С‚РµРЅРёРµРј СЃ РґР°С‚С‡РёРєРѕРІ : ")
                self.display.lcd_display_string("err: write data", 1)
                self.display.lcd_display_string("from sensors", 2)
            if code == 2:
                file.write("РѕС€РёР±РєР° СЃ РІС‹РІРѕРґРѕРј РЅР° СЌРєСЂР°РЅ : ")
            if code == 3:
                file.write("РѕС€РёР±РєР° СЃ Р·Р°РїРёСЃСЊСЋ РІ Р±Р°Р·Сѓ РґР°РЅРЅС‹С… : ")
                self.display.lcd_display_string("err: write data", 1)
                self.display.lcd_display_string("to database", 2)
            file.write(str(err))

    def read_data(self):
        try:
            self.pressure, temperature1 = self.sensBMP()
            self.humidity, temperature2 = self.sensDHT()
            self.temperature = (temperature1 + temperature2) / 2
            self.pressure /= 133.322
        except Exception as err:
            print("Error: ", err)
            self.create_log(err, 1)

    def print_data(self, filename=None):
        if filename is not None:
            with open(filename, 'w') as file:
                file.write("%.2f" % round(self.temperature, 2))
                file.write("%.2f" % round(self.pressure, 2))
                file.write("%.2f" % round(self.humidity, 2))
        else:
            print("temperature: %.2f, pressure: %.2f, humidity: %.2f" %
                  (round(self.temperature, 2), round(self.pressure, 2), round(self.humidity, 2)))

    def write_to_lcd(self):
        try:
            self.display.lcd_display_string("pressure: %.2f" % round(self.pressure, 2), 1)
            self.display.lcd_display_string("temp %.2f Hum %.2f" %
                                            (round(self.temperature, 2), round(self.humidity, 2)), 2)
        except Exception as err:
            print("Error: ", err)
            self.create_log(err, 2)

    def write_to_db(self):
        try:
            with self.dbConnection.cursor() as cursor:
                cursor.execute("INSERT INTO data (timestamp,temperature,pressure,humidity) \
                VALUES (?,?,?,?)", [datetime.now().timestamp(), self.temperature, self.pressure, self.humidity])
            self.dbConnection.commit()
        except sqlite3.DatabaseError as err:
            print("Error: ", err)
            self.create_log(err, 3)


if __name__ == "__main__":
    sensors = SensorReader("weather_data.db", 4)
    schedule.every(1).minutes.do(sensors.read_data)
    schedule.every(1).minutes.do(sensors.print_data)
    # schedule.every(2).minutes.do(sensors.write_to_lcd)
    schedule.every(1).hour.do(sensors.write_to_db)
    while True:
        schedule.run_pending()
        time.sleep(10)
