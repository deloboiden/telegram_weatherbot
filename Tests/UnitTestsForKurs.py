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

def test_SensBMP():
    pressure1,temperature1 = kurs.sensBMP()
    pressure2 = sense.pressure*100
    temperature2 = sense.temp
    assert temperature1 - temperature2 < 0.01
    assert pressure1 - pressure2 < 0.01
    
def test_SensDHT():
    humidity1, temperature1 = kurs.sensDHT()
    humidity2 = sense.humidity
    temperature2 = sense.temp
    assert temperature1 - temperature2 < 0.01
    assert humidity1 - humidity2 < 0.01
    
def test_write_to_lcd1():
    kurs.temperature = 25.4
    kurs.pressure = 765.1
    kurs.humidity = 78.6
    kurs.write_to_lcd()
    assert compareDataInFiles('l1.txt',"pressure:765.10")
    assert compareDataInFiles('l2.txt',"temp25.40Hum78.60")
    
def test_write_to_lcd2():
    os.rename("l1.txt","1.txt")
    kurs.write_to_lcd()
    os.rename("1.txt","l1.txt")
    assert compareDataInFiles('err.log',"ошибка с выводом на экран : error")
    
def test_write_to_db1():
    kurs.temperature = 25.4
    kurs.pressure = 765.1
    kurs.humidity = 78.6
    kurs.write_to_db()
    cursor.execute("""select timestamp,temperature,pressure,
                humidity from data order by id desc LIMIT 1""")
    stamp,temp,pres,humi, = cursor.fetchone()
    assert (datetime.datetime.now().timestamp() - stamp) < 3
    assert temp == 25.4
    assert pres == 765.1
    assert humi == 78.6
    
def test_write_to_db2():
    os.rename("weather_data.db","1.db")
    kurs.write_to_db()
    os.rename("1.db","weather_data.db")
    assert compareDataInFiles('err.log',"ошибка с записью в базу данных : " +
                              "attempt to write a readonly database")
    assert compareDataInFiles('l1.txt',"err: write data")
    assert compareDataInFiles('l2.txt',"to database")
    
def test_create_log1():
    kurs.create_log("error",1)
    assert compareDataInFiles('err.log',"ошибка с чтением с датчиков : error")
    assert compareDataInFiles('l1.txt',"err: write data")
    assert compareDataInFiles('l2.txt',"from sensors")
    
def test_create_log2():
    kurs.create_log("error",2)
    assert compareDataInFiles('err.log',"ошибка с выводом на экран : error")
    
def test_create_log3():
    kurs.create_log("error",3)
    assert compareDataInFiles('err.log',"ошибка с записью в базу данных : error")
    assert compareDataInFiles('l1.txt',"err: write data")
    assert compareDataInFiles('l2.txt',"to database")
    
def test_read_data1():
    kurs.read_data()
    assert kurs.temperature - sense.temp < 0.01
    assert kurs.humidity - sense.humidity < 0.01
    assert (sense.pressure/1.33322) - kurs.pressure < 0.02
    
def test_read_data2():
    print("выставь в sense HAT Emulator давление ниже 800m mbar, у вас 10 сек")
    time.sleep(10)
    kurs.read_data()
    assert compareDataInFiles('err.log',"ошибка с чтением с датчиков : "
                              +"давление вышло за рамки допустимого: "+ str(sense.pressure/1.33322) )
    assert compareDataInFiles('l1.txt',"err: write data")
    assert compareDataInFiles('l2.txt',"from sensors")
    
def test_read_data3():
    print("выставь в sense HAT Emulator температуру выше 80 градусов, у вас 10 сек")
    time.sleep(10)
    kurs.read_data()
    assert compareDataInFiles('err.log',"ошибка с чтением с датчиков : "
                              +"температура2 вышла за рамки допустимого: "+ str(sense.temp))
    assert compareDataInFiles('l1.txt',"err: write data")
    assert compareDataInFiles('l2.txt',"from sensors")
    
    
