import asyncio
import time
import threading
from telethon import TelegramClient, events, types
import datetime
from Creating import Socker

api_id = ******
api_hash = ******
client = TelegramClient(*****, api_id, api_hash)
client.start()



async def my_event_handler(ev):
    print(ev.message.from_id.user_id)
    if ev.message.from_id.user_id == 1648843091 or ev.message.from_id.user_id == 5075842966:
        if "Сигнал" in ev.message.text:
            pass
        else:
            print("Got sygnal")
            print(ev.message.text)
            sock.buy(ev.message.text)
    else:
        pass
if __name__ == '__main__':
    sock = Socker(amount=50)
    client.add_event_handler(my_event_handler, events.NewMessage)
    client.run_until_disconnected()
