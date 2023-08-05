import threading
import requests
import random
import time
try:
    from websocket import create_connection, WebSocketConnectionClosedException
    import vk
except ImportError:
    pass


class Merchant:
    def __init__(self, user_id, key):
        self.key = key
        self.id = int(user_id)
        self.url = 'https://coin-without-bugs.vkforms.ru/merchant/'
        self.is_send_request_running = False  # Защита от получения ANOTHER_TRANSACTION_IN_PROGRESS_AT_SAME_TIME
        self.token = None
        self.session = None
        self.api = None
        self.app_url = None
        self.wss_url = None
        self.on_payment = None
        self.ws = None

    def long_poll(self):
        try:
            while True:
                time.sleep(0.2)
                message = self.ws.recv()
                if message.startswith('TR'):
                    message = message.split()
                    self.on_payment(int(message[2]), float(message[1]) / 1000)
        except WebSocketConnectionClosedException:
            self.ws = create_connection(self.wss_url)
            threading.Thread(target=self.long_poll).start()

    def register_payment_callback(self, token, callback):
        self.on_payment = callback
        self.token = token
        self.session = vk.Session(access_token=self.token)
        self.api = vk.API(self.session, v='5.92')
        self.app_url = self.api.apps.get(app_id=6915965)['items'][0]['mobile_iframe_url']

        channel = self.id % 32
        self.wss_url = self.app_url.replace('https', 'wss').replace('\\', '')
        self.wss_url = self.wss_url.replace('index.html', 'channel/{channel}'.format(channel=channel))
        self.wss_url += '&ver=1&upd=1&pass={user_id}'.format(user_id=self.id - 1)

        self.ws = create_connection(self.wss_url)
        threading.Thread(target=self.long_poll).start()

    def get_payment_url(self, amount, payload=random.randint(-2000000000, 2000000000), free_amount=False):
        if free_amount:
            return 'vk.com/coin#x{id}_{sum}_{payload}_1'.format(id=self.id, sum=amount * 1000, payload=payload)
        else:
            return 'vk.com/coin#x{id}_{sum}_{payload}'.format(id=self.id, sum=amount * 1000, payload=payload)

    def get_transactions(self, tx, last_tx=None):
        if last_tx is None:
            transactions = requests.post(self.url + 'tx/', json={'merchantId': self.id, 'key': self.key, 'tx': tx})
        else:
            transactions = requests.post(self.url + 'tx/',
                                         json={'merchantId': self.id, 'key': self.key, 'tx': tx, 'lastTx': last_tx})
        return transactions.json()

    def send(self, to_id, amount):
        if not self.is_send_request_running:
            self.is_send_request_running = True
            transactions = requests.post(self.url + 'send/',
                                         json={'merchantId': self.id, 'key': self.key, 'toId': to_id,
                                               'amount': amount * 1000})
            self.is_send_request_running = False
            return transactions.json()

    def get_balance(self, *args):
        balance = requests.post(self.url + 'score/', json={'merchantId': self.id, 'key': self.key, 'userIds': args})
        return balance.json()
