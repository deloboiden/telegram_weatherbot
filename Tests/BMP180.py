from sense_emu import SenseHat

class BMP180(object):
    def __init__(self):
        global sense
        sense = SenseHat()
 
    def read_temperature(self):
        temp = sense.temp
        return temp
 
    def read_pressure(self):
        pres = sense.pressure*100
        return pres