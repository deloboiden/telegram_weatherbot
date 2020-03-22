import kurs
import time, datetime
import sqlite3
import os
from sense_emu import SenseHat

conn = sqlite3.connect("weather_data.db")
cursor = conn.cursor()
sense = SenseHat()

def compareDataInFiles(filename, data):
    file = open(filename,'r')
    line = file.read()
    file.close()
    if line == data:
        return True
    else:
        return False

for i in range(0,10):
    if i == 5 :
        os.rename("l1.txt","1.txt")
        kurs.write_to_lcd()
        os.rename("1.txt","l1.txt")
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
    temp = sense.temp
    press = sense.pressure
    humi = sense.humidity
    assert compareDataInFiles('l1.txt',"pressure:" + str("%.2f"%round(press/1.33322,2)))
    assert compareDataInFiles('l2.txt',"temp" + str("%.2f"%round(temp,2)) +
     "Hum" + str("%.2f"%round(humi,2)))  

def test_kurs3():
    assert compareDataInFiles('err.log',"ошибка с выводом на экран : error")
