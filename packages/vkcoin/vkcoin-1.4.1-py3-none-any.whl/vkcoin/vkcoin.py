import requests
import random
import json


class Merchant:
    def __init__(self, user_id, key):
        self.key = key
        self.id = int(user_id)
        self.url = 'https://coin-without-bugs.vkforms.ru/merchant/'
        self.is_send_request_running = False  # Защита от получения ANOTHER_TRANSACTION_IN_PROGRESS_AT_SAME_TIME

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
                                         data=json.dumps({'merchantId': self.id, 'key': self.key, 'tx': tx, 'lastTx': last_tx}),
                                         headers={"Content-Type": "application/json"})
        return transactions.json()

    def send(self, to_id, amount):
        if not self.is_send_request_running:
            self.is_send_request_running = True
            transactions = requests.post(self.url + 'send/',
                                         data=json.dumps({'merchantId': self.id, 'key': self.key, 'toId': to_id,
                                               'amount': amount * 1000}), headers={"Content-Type": "application/json"})
            self.is_send_request_running = False
            return transactions.json()

    def get_balance(self, user_id=371576679):
        test_transaction = self.send(user_id, 0.001)
        return test_transaction['response']['current']
