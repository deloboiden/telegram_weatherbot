import kurs
import time, datetime
import sqlite3
import os
from sense_emu import SenseHat

conn = sqlite3.connect("weather_data.db")
cursor = conn.cursor()
sense = SenseHat()

for i in range(0,10):
    kurs.read_data()
    kurs.write_to_lcd()
    kurs.write_to_db()
    time.sleep(1)

def test_kurs1():
    temp = sense.temp
    press = sense.pressure
    humi = sense.humidity
    sql = "select timestamp, temperature, pressure, humidity from data order by id desc LIMIT 10"
    try:
        for row in cursor.execute(sql):
            assert abs(temp - row[1]) < 0.1
            assert abs(press/1.33322 - row[2]) < 0.1
            assert abs(humi - row[3]) < 0.5
    except sqlite3.DatabaseError as err:
        assert False

def test_kurs2():
    assert True        