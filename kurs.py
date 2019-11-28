import lcddriver
import time, datetime
import Adafruit_DHT
import sqlite3
import schedule
from BMP180 import BMP180
 
bmp = BMP180()
display = lcddriver.lcd()
sensor = Adafruit_DHT.DHT22 #sensor is DHT22
pin = 4                     #connec to to GPIO pin 4

conn = sqlite3.connect("weather_data.db")
cursor = conn.cursor()

temperature = 0
pressure = 0
humidity = 0
date = 0
ttime = 0

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

def create_log(err):
    file = open('actual.txt','a')
    file.write(err)
    file.close()
    
def read_data():
    try:
        global pressure
        global temperature
        global humidity
        pressure,temperature1 = sensBMP() #read inf from BMP180
        humidity, temperature2 = sensDHT() #read inf from DHT22
        temperature = (temperature1 + temperature2)/2
        pressure /= 133.322
        display.lcd_display_string("pressure:"+str(pressure), 1) # Write line of text to first line of display
        display.lcd_display_string("temp"+str("%.2f"%round(temperature,2))
                                   +"Hum"+str("%.2f"%round(humidity,2)), 2)
        file = open('actual.txt','w')
        file.write("%.2f"%round(temperature,2))
        file.write("%.2f"%round(pressure,2))
        file.write("%.2f"%round(humidity,2))
        file.close()
    
    except Exception as err:  
        print("Error: ", err)
        create_log(err)
        
def write_to_db():
    try:
        global date
        global ttime
        now = datetime.datetime.now()
        date = now.year*10000 + now.month*100 + now.day
        ttime = now.hour*100 + now.minute
        data = (date,ttime,temperature,pressure,humidity)
        sql = """INSERT INTO data
                (date,time,temperature,pressure,humidity)
                VALUES (?,?,?,?,?)"""
        cursor.execute(sql, data)
        
    except sqlite3.DatabaseError as err:       
        print("Error: ", err)
        create_log(err)
    else:
        conn.commit() 
read_data()   
schedule.every(1).minutes.do(read_data)
schedule.every().hour.do(write_to_db)
while True:
     schedule.run_pending()
     time.sleep(1)