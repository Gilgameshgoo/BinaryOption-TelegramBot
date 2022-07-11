import datetime
import time

import websocket
from websocket._exceptions import *

import json
import threading
import sqlite3

class Socker():

    def __init__(self, amount=10, token=None, apiUrl=None):
        self.amount=amount
        if not apiUrl:
            apiUrl="wss://ws.binaryws.com/websockets/v3?app_id=****"
        if not token:
            token="********"
        self.ws = self.creator(token,apiUrl)
        self.create_thr()

        self.con = sqlite3.connect('Orders.db')
        self.cur = self.con.cursor()
        self.create_thr()

    def creator(self,token,apiURL):
        socket=websocket.WebSocket()
        socket.connect(apiURL)
        dic_r = json.dumps({"authorize": f"{token}"})
        socket.send(dic_r)
        socket.recv()
        return socket

    def buy(self,msg):
        self.event.clear()
        code = self.get_code(msg)
        req={"buy": code,
             "price":100
             }
        req=json.dumps(req)
        try:
            self.ws.send(req)
        except:
            self.__init__()
            self.ws.send(req)
        res = self.ws.recv()
        res = json.loads(res)
        contract_id= int(res["buy"]['contract_id'])
        ti=datetime.datetime.now()
        ti=str(ti)
        self.cur.execute(f"INSERT INTO contract( contract_id, time, tupik) VALUES(?,?,?)",
            (contract_id,ti,self.typik))
        self.con.commit()
        print(res)
        self.event.set()

    def get_code(self,msg):
        text = msg.split(" ")
        symbol = "frx" + text[0]
        duration = text[1][1:]
        if text[2] == "вверх":
            action = "CALL"
        else:
            action = "PUT"
        req1 = {
            "proposal": 1,
            "amount": self.amount,
            "basis": "stake",
            "contract_type": action,
            "currency": "USD",
            "duration": duration,
            "duration_unit": "m",
            "symbol": symbol
        }
        self.typik=f"{req1['symbol']}:{req1['contract_type']}"
        req = json.dumps(req1)
        self.ws.send(req)
        res = json.loads(self.ws.recv())
        res = dict(res)
        if "error" in res.keys():
            if res["error"]["code"]=="ContractBuyValidationError":
                req1["amount"]=50
                req = json.dumps(req1)
                self.ws.send(req)
                res = json.loads(self.ws.recv())
        res = res['proposal']['id']
        return res

    def create_thr(self):
        self.event = threading.Event()
        t2 = threading.Thread(target=self.ceeper, args=(self.event, self.ws))
        self.event.set()
        t2.start()

    def ceeper(self,event, ws=None):
        while 1:
            f.write("Esti\n")
            #print("I am alive")
            event.wait(timeout=None)
            req={"ping":1}
            req=json.dumps(req)
            ws.send(req)
            ws.recv()
            time.sleep(30)

l=Socker()
