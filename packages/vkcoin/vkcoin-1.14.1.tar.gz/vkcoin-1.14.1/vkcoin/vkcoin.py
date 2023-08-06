import requests
import time
from threading import Thread
from random import randint
import json
import socket
from websocket import create_connection, WebSocketConnectionClosedException


class Entity:
    def __init__(self, data):
        if isinstance(data, dict):
            for k, v in data.items():
                if isinstance(v, dict):
                    self.__dict__[k] = Entity(v)
                elif isinstance(v, list):
                    self.__dict__[k] = [Entity(i) for i in v]
                else:
                    self.__dict__[k] = v
        self._dict = data

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __repr__(self):
        return str(self._dict)


class VKCoinApi:
    def __init__(self, user_id, key):
        self.link = 'https://coin-without-bugs.vkforms.ru/merchant/'
        self.user_id = user_id
        self.key = key
        self.reg_endpoint = False
        self.handler = None
        self.longpoll_handler = None
        self.last_trans = None
        self.port = None

    def send_coins(self, to_id, amount):
        data = {'merchantId': self.user_id, 'key': self.key, 'toId': to_id, 'amount': amount}
        return requests.post(self.link + 'send', json=data).json()

    def get_payment_url(self, amount, payload=None, free_amount=False):
        if not payload:
            payload = randint(-2e9, 2e9)
        user_id = hex(self.user_id)[2:]
        amount = hex(amount)[2:]
        payload = hex(payload)[2:]
        link = f'vk.com/coin#m{user_id}_{amount}_{payload}'
        if free_amount:
            link += '_1'
        return link

    def get_transactions(self, tx, last_tx=None):
        data = {'merchantId': self.user_id, 'key': self.key, 'tx': tx}
        if last_tx:
            data['lastTx'] = last_tx
        return requests.post(self.link + 'tx', json=data).json()

    def get_user_balance(self, *users):
        data = {'merchantId': self.user_id, 'key': self.key, 'userIds': users}
        return requests.post(self.link + 'score', json=data).json()

    def get_my_balance(self):
        return self.get_user_balance(self.user_id)

    def set_callback_endpoint(self, address=None):
        try:
            self.port = int(address.split(':')[1])
        except ValueError:
            raise Exception('Неверный порт')
        self.reg_endpoint = True
        data = {'merchantId': self.user_id, 'key': self.key, 'callback': address}
        return requests.post(self.link + 'set', json=data).json()

    def remove_callback_endpoint(self):
        data = {'merchantId': self.user_id, 'key': self.key, 'callback': None}
        return requests.post(self.link + 'set', json=data).json()

    def callback_start(self):
        if not self.reg_endpoint:
            raise Exception('Необходима регистрация CallBack-endpoint')
        sock = socket.socket()
        sock.bind(('', self.port))
        sock.listen(1)
        while True:
            c_sock, _ = sock.accept()
            msg = c_sock.recv(1024).decode('utf-8')
            if msg:
                c_sock.send(b'HTTP/1.1 200 OK\n\n\n')
                try:
                    data = Entity(json.loads(msg.split('\r\n\r\n')[-1]))
                except json.JSONDecodeError:
                    c_sock.close()
                else:
                    self.handler(data)
    
    def longpoll_start(self, tx, interval=0.2):
        self.last_trans = Entity(self.get_transactions(tx)).response
        while True:
            time.sleep(interval)
            current_trans = Entity(self.get_transactions(tx)).response
            if self.last_trans[0] != current_trans[0]:
                new_trans = current_trans[0]
                if new_trans.to_id == self.user_id:
                    self.last_trans = current_trans
                    if self.longpoll_handler:
                        self.longpoll_handler(new_trans)

    def set_shop_name(self, name):
        data = {'merchantId': self.user_id, 'key': self.key, 'name': name}
        return requests.post(self.link + 'set', json=data).json()
      
    def cb_handler(self, func):
        self.handler = func
        return func

    def lp_handler(self, func):
        self.longpoll_handler = func
        return func


class VKCoinWS(Thread):
    def __init__(self, token=None, iframe_link=None, notify=False):
        Thread.__init__(self)
        self.method_url = 'https://api.vk.com/method/'
        self.token = token
        self.iframe_link = iframe_link
        self.notify = notify
        self.score = 0
        self.user_id = 0
        self.link = None
        self.ws_link = None
        self.handler_f = None
        self.ws = None

    def run_ws(self):
        self.ws_link = self._create_ws_link()
        self.start()

    def _create_ws_link(self):
        if not self.iframe_link:
            response = requests.get(self.method_url + 'apps.get', params={'access_token': self.token, 'app_id': 6915965,
                                                                          'v': 5.52}).json()
            try:
                self.iframe_link = response['response']['items'][0]['mobile_iframe_url']
            except KeyError:
                raise Exception('Неверный токег')

        user_id = int(self.iframe_link.split('user_id=')[-1].split('&')[0])
        ch = user_id % 32
        self.user_id = user_id
        ws_link = self.iframe_link.replace('https', 'wss').replace('\\', '')
        ws_link = ws_link.replace('index.html', f'channel/{ch}')
        ws_link += f'&ver=1&upd=1&pass={user_id - 1}'
        return ws_link

    def run(self):
        self.ws = create_connection(self.ws_link)
        while True:
            try:
                msg = self.ws.recv()
                self._message_handler(msg)
            except WebSocketConnectionClosedException:
                self.ws = create_connection(self.ws_link)
            time.sleep(0.1)

    def _message_handler(self, msg):
        if msg.startswith('TR'):
            amount, user_from, trans = msg.split()[1:]
            self.score += int(amount)
            if self.notify:
                print(f'Пополнение на сумму {int(amount) / 1000} от vk.com/id{user_from}')
                print(f'Текущий баланс: {self.score / 1000}')
            if self.handler:
                data = Entity({'user_id': self.user_id, 'balance': self.score, 'user_from': user_from,
                               'amount': amount})
                self.handler_f(data)
        elif len(msg) > 50000:
            msg = json.loads(msg)
            self.score = msg['score']
            if self.notify:
                print('Баланс', msg['score'] / 1000)

    def get_top(self, top_type='user'):
        if not self.ws_link:
            self.ws_link = self._create_ws_link()
        ws = create_connection(self.ws_link)
        init = json.loads(ws.recv())
        ws.close()
        return init.get('top').get(f'{top_type}Top')

    def handler(self, func):
        self.handler_f = func
        return func
