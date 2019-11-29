#import lcddriver
import time, datetime
import Adafruit_DHT
import sqlite3
import schedule
from BMP180 import BMP180
 
bmp = BMP180()
#display = lcddriver.lcd()
sensor = Adafruit_DHT.DHT22 #sensor is DHT22
pin = 4                     #connect to to GPIO pin 4

conn = sqlite3.connect("weather_data.db")
cursor = conn.cursor()

temperature = 0
pressure = 0
humidity = 0
timestamp = 0

def sensBMP():
    pres = 0
    temp = 0
    for i in range(0,10):
        pres += bmp.read_pressure()
        temp += bmp.read_temperature()
    pres /= 10
    temp /= 10
    return pres,temp

def sensDHT():
    humi = 0
    temp = 0
    for i in range(0,10):
         humi1, temp1 = Adafruit_DHT.read_retry(sensor, pin)
         humi += humi1
         temp += temp1
    humi /= 10
    temp /= 10
    return humi,temp

def create_log(err,code):
    file = open('err.log','w')
    if code == 1:
        file.write("ошибка с чтением с датчиков : " + str(err))
        #try:
            #display.lcd_display_string("err: write data", 1)
            #display.lcd_display_string("from sensors", 2)
        #except Exception as er:
            #file.write("\n ошибка с выводом на экран : "+str(er))
    if code == 2:
        file.write("ошибка с выводом на экран : "+ str(err))
    if code == 3:
        file.write("ошибка с записью в базу данных : "+ str(err))
        #try:
            #display.lcd_display_string("err: write data", 1)
            #display.lcd_display_string("to database", 2)
        #except Exception as er:
            #file.write("\n ошибка с выводом на экран : "+str(er))  
    file.close()
    
def read_data():
    global pressure
    global temperature
    global humidity
    temperature1 = 0
    temperature2 = 0
    try:
        pressure,temperature1 = sensBMP() #read inf from BMP180
        humidity, temperature2 = sensDHT() #read inf from DHT22
    except Exception as err:  
        print("Error: ", err)
        create_log(err,1)
    temperature = (temperature1 + temperature2)/2 
    pressure /= 133.322
    if (pressure > 815) or (pressure < 640):
        create_log("давление вышло за рамки допустимого: "+str(pressure),1)
        pressure = 755
    if (temperature1 > 70) or (temperature1 < -70):
        create_log("температура1 вышла за рамки допустимого: "+str(temperature1),1)
        temperature1 = 10
    if (temperature2 > 70) or (temperature2 < -70):
        create_log("температура2 вышла за рамки допустимого: "+str(temperature2),1)
        temperature2 = 10
    if (humidity > 100) or (humidity < 0):
        create_log("влажность вышла за рамки допустимого: "+str(humidity),1)
        humidity = 50
        
def write_to_lcd():
    try:
        display.lcd_display_string("pressure:"+str("%.2f"%round(pressure,2)), 1)
        display.lcd_display_string("temp"+str("%.2f"%round(temperature,2))
                                    +"Hum"+str("%.2f"%round(humidity,2)), 2)
    except Exception as err:  
        print("Error: ", err)
        create_log(err,2)

def write_to_db():
    global timestamp
    timestamp = datetime.datetime.now().timestamp()
    data = (timestamp,temperature,pressure,humidity)
    try:
        sql = """INSERT INTO data
                (timestamp,temperature,pressure,humidity)
                VALUES (?,?,?,?)"""
        cursor.execute(sql, data)
        
    except sqlite3.DatabaseError as err:       
        print("Error: ", err)
        create_log(err,3)
    else:
        conn.commit()
        
schedule.every(1).minutes.do(read_data)
#schedule.every(1).minutes.do(write_to_lcd)
schedule.every(1).hour.do(write_to_db)
while True:
     schedule.run_pending()
     time.sleep(1)