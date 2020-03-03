import telepot
import time, datetime
import sqlite3
import matplotlib.pyplot as plt
from telepot.namedtuple import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, ForceReply
from telepot.loop import MessageLoop
from telepot.delegate import per_chat_id, create_open, pave_event_space

TOKEN = '698304710:AAGxfMDUIB-wBXnoNGGtFlE9r1UHAkMvj2g'
admin = 268115509 #admin's id in Telegram

class Weather_bot(telepot.helper.ChatHandler):
    def __init__(self, *args, **kwargs):
        super(Weather_bot, self).__init__(*args, **kwargs)
        self.markup = ""
        self.ttime = 0 

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
    
    def weather_predict(self, delta):
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
            self.sender.sendMessage ("Good morning",reply_markup=self.markup)
        elif  12 <= hour < 17:
            self.sender.sendMessage ("Good day",reply_markup=self.markup)
        elif  17 <= hour < 23:
            self.sender.sendMessage ("Good evening",reply_markup=self.markup)
        elif  23 <= hour or hour < 6:
            self.sender.sendMessage ("Good night",reply_markup=self.markup)
        return True 

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
                self.bot.sendMessage(admin,"ошибка с чтением из базы данных "+str(err))
            temp,pres,humi, = cursor.fetchone()
            self.sender.sendMessage ("temperature: "+str("%.2f"%round(temp,2))+" C \n"+
            "pressure: "+str("%.2f"%round(pres,2))+" mm Hg \n" +
            "humidity: "+str("%.2f"%round(humi,2))+" %")
        elif command == 'weather now':
            try:
                cursor.execute("select pressure from data order by id desc LIMIT 1")
            except sqlite3.DatabaseError as err:
                self.bot.sendMessage(admin,"ошибка с чтением из базы данных "+str(err))    
            pres, = cursor.fetchone()
            self.sender.sendMessage ("here weather for now: \n"
                                     + self.weather_now(pres))
        elif command == 'weather predict':
            arr = list()
            timestamp = datetime.datetime.now().timestamp()
            sql = "select pressure from data where timestamp between "
            sql += str(timestamp-36000)+" and "+str(timestamp)
            try:
                for row in cursor.execute(sql):
                    arr.append(row[0])
            except sqlite3.DatabaseError as err:
                self.bot.sendMessage(admin,"ошибка с чтением из базы данных "+str(err))    
            if len(arr) < 7:
                self.sender.sendMessage ("Sorry, we don't have actual data right now")
                self.bot.sendMessage(admin,"Нет данных за последние 10 часов")
            else:
                sumX = 0
                sumY = 0
                sumX2 = 0
                sumXY = 0
                for i in range(0,len(arr)):
                    sumX += i
                    sumX2 += i*i
                    sumY += arr[i]
                    sumXY += arr[i]*i
                delta = len(arr) * sumXY - sumX*sumY
                delta /= (len(arr)*sumX2 - sumX*sumX)
                delta *= len(arr)
                self.sender.sendMessage ("here weather predict for now: \n"
                                         + self.weather_predict(delta))
        elif command == 'statistic':
            self.markup = ReplyKeyboardMarkup(keyboard=[
            [dict(text='day')],
            [dict(text='3 days')],
            [dict(text='week')],
            [dict(text='mounth')],
            [dict(text='back to main')],
            ])
            self.sender.sendMessage (command ,reply_markup=self.markup)
        elif (command == 'day')or(command == '3 days')or(command == 'week')or(command == 'mounth'):
            self.markup = ReplyKeyboardMarkup(keyboard=[
            [dict(text='temperature')],
            [dict(text='pressure')],
            [dict(text='humidity')],
            [dict(text='back to main')],
            ])
            self.sender.sendMessage (command ,reply_markup=self.markup)
            if command == 'day' : self.ttime = 86400
            if command == '3 days' : self.ttime = 259200
            if command == 'week' : self.ttime = 604800
            if command == 'mounth' : self.ttime = 2592000
        elif command == 'back to main':
            self.markup = ReplyKeyboardMarkup(keyboard=[
            [dict(text='data from sensors')],
            [dict(text='weather now')],
            [dict(text='weather predict')],
            [dict(text='statistic')],
            ])
            self.sender.sendMessage (command ,reply_markup=self.markup)
        elif command == 'temperature':
            y = list()
            x = list()
            timestamp = datetime.datetime.now().timestamp()
            sql = "select timestamp, temperature from data where timestamp between "
            sql += str(timestamp-self.ttime)+" and "+str(timestamp)
            try:
                for row in cursor.execute(sql):
                    x.append(datetime.datetime.fromtimestamp(row[0]))
                    y.append(row[1])
            except sqlite3.DatabaseError as err:
                self.bot.sendMessage(admin,"ошибка с чтением из базы данных "+str(err))    
            plt.figure()
            plt.plot(x,y)
            plt.tight_layout()
            plt.savefig('foo.png')
            self.sender.sendPhoto (open('foo.png','rb'))
        elif command == 'pressure':
            y = list()
            x = list()
            timestamp = datetime.datetime.now().timestamp()
            sql = "select timestamp, pressure from data where timestamp between "
            sql += str(timestamp-self.ttime)+" and "+str(timestamp)
            try:
                for row in cursor.execute(sql):
                    x.append(datetime.datetime.fromtimestamp(row[0]))
                    y.append(row[1])
            except sqlite3.DatabaseError as err:
                self.bot.sendMessage(admin,"ошибка с чтением из базы данных "+str(err))    
            plt.figure()
            plt.plot(x,y)
            plt.tight_layout()
            plt.savefig('foo.png')
            self.sender.sendPhoto (open('foo.png','rb'))
        elif command == 'humidity':
            y = list()
            x = list()
            timestamp = datetime.datetime.now().timestamp()
            sql = "select timestamp, humidity from data where timestamp between "
            sql += str(timestamp-self.ttime)+" and "+str(timestamp)
            try:
                for row in cursor.execute(sql):
                    x.append(datetime.datetime.fromtimestamp(row[0]))
                    y.append(row[1])
            except sqlite3.DatabaseError as err:
                self.bot.sendMessage(admin,"ошибка с чтением из базы данных "+str(err))    
            plt.figure()
            plt.plot(x,y)
            plt.tight_layout()
            plt.savefig('foo.png')
            self.sender.sendPhoto (open('foo.png','rb'))
        
    def on__idle(self, event):
        self.markup = ReplyKeyboardRemove()
        self.sender.sendMessage ("Good bye" ,reply_markup=self.markup)
        self.close()

#bot = telepot.DelegatorBot(TOKEN,[
#    pave_event_space()(
#        per_chat_id(), create_open, Weather_bot, timeout=90),
#])
#MessageLoop(bot).run_as_thread()
#print('Listening ...')

#while 1:
#    time.sleep(10)
#    file = open('err.log', 'r')
#    data = file.read()
#    if ( data != ""):
#        bot.sendMessage(admin,data)
#        file.close
#        file = open('err.log', 'w')
#    file.close()
