from websocket import create_connection
import vk
import threading
import requests
import random
import json
import time


class Merchant:
    def __init__(self, user_id, key, token=None, on_payment=None):
        self.key = key
        self.id = int(user_id)
        self.url = 'https://coin-without-bugs.vkforms.ru/merchant/'
        self.is_send_request_running = False  # Защита от получения ANOTHER_TRANSACTION_IN_PROGRESS_AT_SAME_TIME
        if on_payment is not None and token is not None:
            self.token = token
            self.on_payment = on_payment
            self.session = vk.Session(access_token=self.token)
            self.api = vk.API(self.session, v='5.92')
            self.app_url = self.api.apps.get(app_id=6915965)['items'][0]['mobile_iframe_url']

            channel = self.id % 32
            ws_link = self.app_url.replace('https', 'wss').replace('\\', '')
            ws_link = ws_link.replace('index.html', 'channel/{channel}'.format(channel=channel))
            ws_link += '&ver=1&upd=1&pass={user_id}'.format(user_id=self.id - 1)
            self.wss_url = ws_link
            self.on_payment = on_payment

            self.ws = create_connection(self.wss_url)
            threading.Thread(target=self.long_poll).start()

    def long_poll(self):
        while True:
            time.sleep(0.2)
            message = self.ws.recv()
            if message.startswith('TR'):
                message = message.split()
                self.on_payment(int(message[2]), float(message[1]) / 1000)

    def get_payment_url(self, amount, payload=random.randint(-2000000000, 2000000000), free_amount=False):
        if free_amount:
            return 'vk.com/coin#m{id}_{sum}_{payload}_1'.format(id=self.id, sum=amount * 1000, payload=payload)
        else:
            return 'vk.com/coin#m{id}_{sum}_{payload}'.format(id=self.id, sum=amount * 1000, payload=payload)

    def get_transactions(self, tx, last_tx=None):
        if last_tx is None:
            transactions = requests.post(self.url + 'tx/',
                                         data=json.dumps({'merchantId': self.id, 'key': self.key, 'tx': tx}),
                                         headers={"Content-Type": "application/json"})
        else:
            transactions = requests.post(self.url + 'tx/',
                                         data=json.dumps({'merchantId': self.id, 'key': self.key, 'tx': tx,
                                                          'lastTx': last_tx}),
                                         headers={"Content-Type": "application/json"})
        return transactions.json()['response']

    def send(self, to_id, amount):
        if not self.is_send_request_running:
            self.is_send_request_running = True
            transactions = requests.post(self.url + 'send/',
                                         data=json.dumps({'merchantId': self.id, 'key': self.key, 'toId': to_id,
                                                          'amount': amount * 1000}),
                                         headers={"Content-Type": "application/json"})
            self.is_send_request_running = False
            return transactions.json()['response']

    def get_balance(self, user_ids):
        balance = requests.post(self.url + 'score/',
                                data=json.dumps({'merchantId': self.id, 'key': self.key, 'userIds': user_ids}),
                                headers={"Content-Type": "application/json"})
        return balance.json()['response']
