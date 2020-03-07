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
    print(event)
    if event.photo:
        print("photo")
        event.download_media("photo")
    #file = open("messages.txt",'w') 
    #print(event.message.to_dict()['message'])
    #print(event.message.to_dict()['reply_markup'])
    #file.write(event.message.to_dict()['message']+"\n")
    #file.write(str(event.message.to_dict()['reply_markup'])+"\n")
    #file.flush()
    #file.close()
      
client.start()

#client.send_message('wettther_bot', 'hello')
#time.sleep(1)
#client.send_message('wettther_bot', 'data from sensors')
#time.sleep(1)
#client.send_message('wettther_bot', 'weather now')
#time.sleep(1)
#client.send_message('wettther_bot', 'weather predict')
#time.sleep(1)
#client.send_message('wettther_bot', 'statistic')

client.run_until_disconnected()