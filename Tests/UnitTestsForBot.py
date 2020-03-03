import time, datetime
import sqlite3
import matplotlib.pyplot as plt
from weather_bot import Weather_bot

conn = sqlite3.connect("weather_data.db")
cursor = conn.cursor()

def test_weathernow1():
    answer = Weather_bot.weather_now(Weather_bot, 700)
    assert answer == "now the storm is better not to go out"

def test_weathernow2():
    answer = Weather_bot.weather_now(Weather_bot, 710)
    assert answer == "it's raining now don't forget to take an umbrella"

def test_weathernow3():
    answer = Weather_bot.weather_now(Weather_bot, 730)
    assert answer == "outside the window a strong wind, I hope you are not easy to blow off"

def test_weathernow4():
    answer = Weather_bot.weather_now(Weather_bot, 750)
    assert answer == "now variable clarity, possible wind, typical weather for St. Petersburg"

def test_weathernow5():
    answer = Weather_bot.weather_now(Weather_bot, 770)
    assert answer == "the weather is clear and wonderful, do not want to walk?"

def test_weathernow6():
    answer = Weather_bot.weather_now(Weather_bot, 780)
    assert answer == "it seems that clear days will stand for a long time, atypically for Petersburg"

def test_weathernow7():
    answer = Weather_bot.weather_now(Weather_bot, 800)
    assert answer == "I hope you are not a farmer, because there will be a strong drought"

def test_weatherpredict1():
    answer = Weather_bot.weather_predict(Weather_bot, -200)
    assert answer == "the weather will get worse very quickly"

def test_weatherpredict2():
    answer = Weather_bot.weather_predict(Weather_bot, -100)
    assert answer == "the weather will get worse"

def test_weatherpredict3():
    answer = Weather_bot.weather_predict(Weather_bot, 0)
    assert answer == "most likely the weather will not change"

def test_weatherpredict4():
    answer = Weather_bot.weather_predict(Weather_bot, 100)
    assert answer == "the weather will get better"

def test_weatherpredict5():
    answer = Weather_bot.weather_predict(Weather_bot, 200)
    assert answer == "the weather will get better very quickly"

#def test_open():
#    Weather_bot.open(Weather_bot, "hello",seed=2)

#def test_onchatmessage():
#    Weather_bot.on_chat_message(Weather_bot,"data from sensors")