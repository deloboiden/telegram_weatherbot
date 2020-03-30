import time,datetime
import sqlite3

file = open("messages.txt",'r')
conn = sqlite3.connect("weather_data.db")
cursor = conn.cursor()

def test_kurs1():
    hour = datetime.datetime.now().hour
    if 6 <= hour < 12:
        text = "Good morning\n"
    elif  12 <= hour < 17:
        text = "Good day\n"
    elif  17 <= hour < 23:
        text = "Good evening\n"
    elif  23 <= hour or hour < 6:
        text = "Good night\n"
    line = file.readline()
    assert text == line
    line = file.readline()
    text = "{'_': 'ReplyKeyboardMarkup', 'rows': [{'_': 'KeyboardButtonRow', 'buttons': "
    text += "[{'_': 'KeyboardButton', 'text': 'data from sensors'}]}, {'_': 'KeyboardButtonRow',"
    text += " 'buttons': [{'_': 'KeyboardButton', 'text': 'weather now'}]}, {'_': 'KeyboardButtonRow',"
    text += " 'buttons': [{'_': 'KeyboardButton', 'text': 'weather predict'}]}, {'_': 'KeyboardButtonRow',"
    text += " 'buttons': [{'_': 'KeyboardButton', 'text': 'statistic'}]}],"
    text += " 'resize': False, 'single_use': False, 'selective': False}\n"
    assert text == line


def test_kurs2():
    cursor.execute("""select temperature,pressure,
    humidity from data order by id desc LIMIT 1""")
    temp,pres,humi, = cursor.fetchone()
    line = file.readline()
    text = "temperature: "+str("%.2f"%round(temp,2))+" C \n"
    assert line == text
    line = file.readline()
    text = "pressure: "+str("%.2f"%round(pres,2))+" mm Hg \n"
    assert line == text
    line = file.readline()
    text = "humidity: "+str("%.2f"%round(humi,2))+" %\n"
    assert line == text
    line = file.readline()
    text = "None\n"
    assert line == text

def test_kurs3():
    line = file.readline()
    text = "here weather for now: \n"
    assert line == text
    line = file.readline()
    text = "now variable clarity, possible wind, typical weather for St. Petersburg\n"
    assert line == text
    line = file.readline()
    text = "None\n"
    assert line == text

def test_kurs4():
    line = file.readline()
    text = "Sorry, we don't have actual data right now\n"
    assert line == text
    line = file.readline()
    text = "None\n"
    assert line == text
    line = file.readline()
    text = "Нет данных за последние 10 часов\n"
    assert line == text
    line = file.readline()
    text = "None\n"
    assert line == text

def test_kurs5():
    line = file.readline()
    text = "statistic\n"
    assert line == text
    line = file.readline()
    text = "{'_': 'ReplyKeyboardMarkup', 'rows': [{'_': 'KeyboardButtonRow', 'buttons':"
    text += " [{'_': 'KeyboardButton', 'text': 'day'}]}, {'_': 'KeyboardButtonRow', 'buttons':"
    text += " [{'_': 'KeyboardButton', 'text': '3 days'}]}, {'_': 'KeyboardButtonRow', 'buttons':"
    text += " [{'_': 'KeyboardButton', 'text': 'week'}]}, {'_': 'KeyboardButtonRow', 'buttons':"
    text += " [{'_': 'KeyboardButton', 'text': 'mounth'}]}, {'_': 'KeyboardButtonRow', 'buttons':"
    text += " [{'_': 'KeyboardButton', 'text': 'back to main'}]}], 'resize': False, 'single_use':"
    text += " False, 'selective': False}\n"
    assert line == text

def test_kurs6():
    line = file.readline()
    text = "week\n"
    assert line == text
    line = file.readline()
    text = "{'_': 'ReplyKeyboardMarkup', 'rows': [{'_': 'KeyboardButtonRow', 'buttons':"
    text += " [{'_': 'KeyboardButton', 'text': 'temperature'}]}, {'_': 'KeyboardButtonRow', 'buttons':"
    text += " [{'_': 'KeyboardButton', 'text': 'pressure'}]}, {'_': 'KeyboardButtonRow', 'buttons':"
    text += " [{'_': 'KeyboardButton', 'text': 'humidity'}]}, {'_': 'KeyboardButtonRow', 'buttons':"
    text += " [{'_': 'KeyboardButton', 'text': 'back to main'}]}],"
    text += " 'resize': False, 'single_use': False, 'selective': False}\n"
    assert line == text

def test_close_file():
    file.close()
    assert True
