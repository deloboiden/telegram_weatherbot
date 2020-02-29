import sys
import time
import telepot
from telepot.loop import MessageLoop

TOKEN = '888073607:AAE6Jse41BtKOA9YnQeYTgtZJcZYyJx65Pc'

def handle(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    print(content_type, chat_type, chat_id)

    if content_type == 'text':
        bot.sendMessage(chat_id, msg['text'])
        file = open("messages.txt",'w')
        file.write(msg['text'])
        
        
bot = telepot.Bot(TOKEN)
MessageLoop(bot, handle).run_as_thread()
while 1:
    time.sleep(10)