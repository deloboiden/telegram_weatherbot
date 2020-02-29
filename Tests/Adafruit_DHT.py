from sense_emu import SenseHat
DHT22 = 22
def read_retry(sensor, pin):
    sense = SenseHat()
    humi = sense.humidity
    temp = sense.temp
    return (humi,temp)
    