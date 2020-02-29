import weather_bot
import telepot
import time, datetime
import sqlite3

bot = weather_bot.Weather_bot()

def test_weather_now():
    result = bot.weather_now(765)
    assert result == "the weather is clear and wonderful, do not want to walk?"
    
def test_weather_predict():
    result = bot.weather_predict(25)
    assert result == "most likely the weather will not change"