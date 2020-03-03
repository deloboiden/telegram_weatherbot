import time, datetime
import sqlite3
from telethon.sync import TelegramClient, events

conn = sqlite3.connect("weather_data.db")
cursor = conn.cursor()
# Вставляем api_id и api_hash
api_id = 1306507
api_hash = 'a9ae117b00ed08426f22e49a502b29c7'

client = TelegramClient('session_name', api_id, api_hash)

@client.on(events.NewMessage(chats=('wettther_bot'),from_users='wettther_bot'))
def normal_handler(event):
    #print(event)
    print(event.message.to_dict()['message'])
    #file.write(event.message.to_dict()['message']+"\n")
    #file.flush()
      
client.start()

#file = open("messages.txt",'w') 
client.send_message('wettther_bot', 'hello')
print("1")
client.send_message('wettther_bot', 'data from sensors')
print("2")
client.send_message('wettther_bot', 'weather now')
print("3")

client.run_until_disconnected()
#file.close()