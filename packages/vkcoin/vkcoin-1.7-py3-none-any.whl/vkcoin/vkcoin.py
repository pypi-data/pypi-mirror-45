import requests
import time
from threading import Thread
from random import randint
import json

try:
	from websocket import create_connection
	from websocket import WebSocketConnectionClosedException as WebSocketClosed
	import vk
except ImportError:
	pass


class Entity:
	pass


class VKCoinWS(Thread):
	def __init__(self, token=None, iframe_link=None, notify=False):
		Thread.__init__(self)
		self.token = token
		self.iframe_link = iframe_link
		self.notify = notify
		self.score = 0
		self.user_id = 0
		self.count_ws_restarts = 0
	
	def run_ws(self):
		if self.iframe_link:
			self.ws_link = self._create_ws_link()
		else:
			session = vk.Session(access_token=self.token)
			api = vk.API(session, v='5.92')
			self.link = api.apps.get(app_id=6915965)['items'][0]['mobile_iframe_url']
			self.ws_link = self._create_ws_link(self)
		self.start()
	
	def _create_ws_link(self):
		user_id = int(self.iframe_link.split('user_id=')[-1].split('&')[0])
		ch = user_id % 32
		self.user_id = user_id
		ws_link = self.iframe_link.replace('https', 'wss').replace('\\', '')
		ws_link = ws_link.replace('index.html', f'channel/{ch}')
		ws_link += f'&ver=1&upd=1&pass={user_id - 1}'
		return ws_link
	
	def run(self):
		ws = create_connection(self.ws_link)
		print('Ok')
		while True:
			try:
				msg = ws.recv()
				self._message_handler(msg)
			except WebSocketClosed:
				self.count_ws_restarts += 1
				if self.count_ws_restarts < 3:
					print('WebSocket закрыт. Перезапуск через 5 секунд')
					time.sleep(5)
					self.run()
				else:
					print('WebSocket окончательно закрыт')
					return
	
	def _message_handler(self, msg):
		if msg.startswith('TR'):
			amount, user_from, trans = msg.split()[1:]
			self.score += int(amount)
			if self.notify:
				print(f'Пополнение на сумму {int(amount)/1000} от vk.com/id{user_from}')
				print(f'Текущий баланс: {self.score/1000}')
			if self.handler:
				data = Entity()
				data.__dict__ = {'user_id': self.user_id, 'balance': self.score, 'user_from': user_from, 'amount': amount}
				self.handler(data)
		elif len(msg) > 50000:
			msg = json.loads(msg)
			self.score = msg['score']
			if self.notify:
				print('Баланс', msg['score'] / 1000)
	
	def handler(self, func):
		self.handler = func
		return func


class VKCoinApi:
	link = 'https://coin-without-bugs.vkforms.ru/merchant/'
	
	def __init__(self, user_id, key):
		self.user = user
		self.key = key
	
	def send_coins(self, to_id, amount):
		data = {'merchantId': self.user, 'key': self.key, 'toId': to_id, 'amount': amount}
		return requests.post(link + 'send', json=data).json()
	
	def get_payment_url(self, amount, payload=None, free_amount=False):
		if not payload:
			payload = randint(-2e9, 2e9)
		user_id = hex(self.merchant_id)[2:]
		amount = hex(amount)[2:]
		payload = hex(payload)[2:]
		link = f'vk.com/coin#m{user_id}_{amount}_{payload}'
		if free_amount:
			link += '_1'
		return link
	
	def get_transactions(self, tx=[2]):

		data = {'merchantId': self.user, 'key': self.key, 'tx': tx}
		return requests.post(link + 'th', json=data).json()
	
	def get_user_balance(self, *users):
		data = {'merchantId': self.user, 'key': self.key, 'userIds': users}
		return requests.post(link + 'score', json=data).json()
	
	def get_my_balance(self):
		data = {'merchantId': self.user, 'key': self.key, 'userIds': [self.user]}
		return requests.post(link + 'score', json=data).json()