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
   
def read_data():
    try:
        global pressure
        global temperature
        global humidity
        pressure,temperature1 = sensBMP() #read inf from BMP180
        humidity, temperature2 = sensDHT() #read inf from DHT22
        temperature = (temperature1 + temperature2)/2    
        display.lcd_display_string("pressure:"+str(pressure/133.3), 1) # Write line of text to first line of display
        display.lcd_display_string("temp"+str(temperature)+"Hum"+str(humidity), 2)
    
    except Exception as e:  
        print(e)
        display.lcd_clear()
        
def write_to_db():
    try:
        global date
        global ttime
        now = datetime.datetime.now()
        date = now.year*10000 + now.month*100 + now.day
        ttime = now.hour*100 + now.minute
        data = (date,time,temperature,pressure,humidity)
        cursor.execute("INSERT INTO data VALUES (?,?,?,?,?)", data)
        
    except sqlite3.DatabaseError as err:       
        print("Error: ", err)
    else:
        conn.commit() 
    
schedule.every(1).minutes.do(read_data)
schedule.every().hour.do(write_to_db)
while True:
     schedule.run_pending()
     time.sleep(1)
    