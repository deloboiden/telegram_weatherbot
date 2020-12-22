import telepot
import time, datetime
import sqlite3
import matplotlib.pyplot as plt
from telepot.namedtuple import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from telepot.loop import MessageLoop
from telepot.delegate import per_chat_id, create_open, pave_event_space

TOKEN = '698304710:AAGxfMDUIB-wBXnoNGGtFlE9r1UHAkMvj2g'
admin = 268115509  # admin's id in Telegram


class Weather_bot(telepot.helper.ChatHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.markup = ""
        self.ttime = 0
        self.timeDict = {'day': 86400, '3 days': 259200, 'week': 604800, 'mounth': 2592000}

    def weather_now(self, pres):
        if pres < 708.81:
            return "now the storm is better not to go out"
        if 708.81 <= pres <= 723.811:
            return "it's raining now don't forget to take an umbrella"
        if 723.811 <= pres <= 738.812:
            return "outside the window a strong wind, I hope you are not easy to blow off"
        if 738.812 <= pres <= 761.314:
            return "now variable clarity, possible wind, typical weather for St. Petersburg"
        if 761.314 <= pres <= 776.315:
            return "the weather is clear and wonderful, do not want to walk?"
        if 776.315 <= pres <= 787.567:
            return "it seems that clear days will stand for a long time, atypically for Petersburg"
        if pres > 787.567:
            return "I hope you are not a farmer, because there will be a strong drought"
        return "odd testimony some wild"

    def weather_predict(self, pressureArray):
        sumX, sumY, sumX2, sumXY = 0, 0, 0, 0
        for i in range(0, len(pressureArray)):
            sumX += i
            sumX2 += i * i
            sumY += pressureArray[i]
            sumXY += pressureArray[i] * i
        delta = len(pressureArray) * sumXY - sumX * sumY
        delta /= (len(pressureArray) * sumX2 - sumX * sumX)
        delta *= len(pressureArray)
        if delta < -150:
            return "the weather will get worse very quickly"
        if -150 <= delta <= -50:
            return "the weather will get worse"
        if -50 <= delta <= 50:
            return "most likely the weather will not change"
        if 50 <= delta <= 150:
            return "the weather will get better"
        if delta > 150:
            return "the weather will get better very quickly"
        return "odd testimony some wild"

    def open(self, initial_msg, seed):
        self.markup = ReplyKeyboardMarkup(keyboard=[
            [KeyboardButton(text='data from sensors')],
            [KeyboardButton(text='weather now')],
            [KeyboardButton(text='weather predict')],
            [KeyboardButton(text='statistic')],
        ])
        hour = datetime.datetime.now().hour
        if 6 <= hour < 12:
            self.sender.sendMessage("Good morning", reply_markup=self.markup)
        elif 12 <= hour < 17:
            self.sender.sendMessage("Good day", reply_markup=self.markup)
        elif 17 <= hour < 23:
            self.sender.sendMessage("Good evening", reply_markup=self.markup)
        elif 23 <= hour or hour < 6:
            self.sender.sendMessage("Good night", reply_markup=self.markup)
        return True

    def SaveGraphic(self, x, y):
        plt.plot(x, y)
        plt.tight_layout()
        plt.savefig('graphic.png', type='png')
        return 'graphic.png'

    def on_chat_message(self, msg):
        content_type, chat_type, chat_id = telepot.glance(msg)
        command = msg['text']
        conn = sqlite3.connect("weather_data.db")
        cursor = conn.cursor()

        if command == 'data from sensors':
            try:
                cursor.execute("""select temperature,pressure,
                humidity from data order by id desc LIMIT 1""")
            except sqlite3.DatabaseError as err:
                self.bot.sendMessage(admin, "error with database" + str(err))
            else:
                temp, pres, humi, = cursor.fetchone()
                self.sender.sendMessage("temperature: %.2f C" % round(temp, 2))
                self.sender.sendMessage("pressure: %.2f mm Hg" % round(pres, 2))
                self.sender.sendMessage("humidity: %.2f " % round(humi, 2))
        elif command == 'weather now':
            try:
                cursor.execute("select pressure from data order by id desc LIMIT 1")
            except sqlite3.DatabaseError as err:
                self.bot.sendMessage(admin, "error with database" + str(err))
            else:
                pres, = cursor.fetchone()
                self.sender.sendMessage("here weather for now:")
                self.sender.sendMessage(self.weather_now(pres))
        elif command == 'weather predict':
            pressureArray = list()
            timestamp = datetime.datetime.now().timestamp()
            sql = "select pressure from data where timestamp between {} and {}".format(
                timestamp - 36000, timestamp)
            try:
                for row in cursor.execute(sql):
                    pressureArray.append(row[0])
            except sqlite3.DatabaseError as err:
                self.bot.sendMessage(admin, "error with database" + str(err))
            else:
                if len(pressureArray) < 7:
                    self.sender.sendMessage("Sorry, we don't have actual data right now")
                    self.bot.sendMessage(admin, "no data for week")
                else:
                    self.sender.sendMessage("here weather predict for now:")
                    self.sender.sendMessage(self.weather_predict(pressureArray))
        elif command == 'statistic':
            self.markup = ReplyKeyboardMarkup(keyboard=[
                [dict(text='day')],
                [dict(text='3 days')],
                [dict(text='week')],
                [dict(text='mounth')],
                [dict(text='back to main')],
            ])
            self.sender.sendMessage(command, reply_markup=self.markup)
        elif command in ['day', '3 days', 'week', 'mounth']:
            self.markup = ReplyKeyboardMarkup(keyboard=[
                [dict(text='temperature')],
                [dict(text='pressure')],
                [dict(text='humidity')],
                [dict(text='back to main')],
            ])
            self.sender.sendMessage(command, reply_markup=self.markup)
            self.ttime = self.timeDict[command]
        elif command == 'back to main':
            self.markup = ReplyKeyboardMarkup(keyboard=[
                [dict(text='data from sensors')],
                [dict(text='weather now')],
                [dict(text='weather predict')],
                [dict(text='statistic')],
            ])
            self.sender.sendMessage(command, reply_markup=self.markup)
        elif command in ['temperature', 'pressure', 'humidity']:
            x, y = [], []
            timestamp = datetime.datetime.now().timestamp()
            sql = "select timestamp, {} from data where timestamp between {} and {}".format(
                command, timestamp - self.ttime, timestamp)
            try:
                for row in cursor.execute(sql):
                    x.append(datetime.datetime.fromtimestamp(row[0]))
                    y.append(row[1])
            except sqlite3.DatabaseError as err:
                self.bot.sendMessage(admin, "error with database" + str(err))
            else:
                path = self.SaveGraphic(x, y)
                self.sender.sendPhoto(open(path, 'rb'))

    def on__idle(self, event):
        self.markup = ReplyKeyboardRemove()
        self.sender.sendMessage("Good bye", reply_markup=self.markup)
        self.close()


if __name__ == "__main__":
    bot = telepot.DelegatorBot(TOKEN, [
        pave_event_space()(
            per_chat_id(), create_open, Weather_bot, timeout=90),
    ])
    MessageLoop(bot).run_as_thread()
    print('Listening ...')

    while 1:
        time.sleep(20)
        file = open('err.log', 'r')
        data = file.read()
        if data:
            bot.sendMessage(admin, data)
            file.close()
            file = open('err.log', 'w')
        file.close()
