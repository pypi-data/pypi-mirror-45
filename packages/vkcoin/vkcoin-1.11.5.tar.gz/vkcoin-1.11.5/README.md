# vkcoin
Враппер для платёжного API VK Coin. https://vk.com/@hs-marchant-api

[![PyPI version](https://badge.fury.io/py/vkcoin.svg)](https://badge.fury.io/py/vkcoin) [![Week downloads](https://img.shields.io/pypi/dw/vkcoin.svg)](https://pypi.org/project/vkcoin) [![Чат ВКонтакте](https://img.shields.io/badge/%D0%A7%D0%B0%D1%82-%D0%92%D0%9A%D0%BE%D0%BD%D1%82%D0%B0%D0%BA%D1%82%D0%B5-informational.svg)](https://vk.me/join/AJQ1d25EgA8/Mv0/xkMvc0i1) [![Чат Telegram](https://img.shields.io/badge/%D0%A7%D0%B0%D1%82-Telegram-informational.svg)](https://t.me/vkcoin_python)
# Установка
* Скачайте и установите [Python](https://www.python.org/downloads/) версии 3.6 и выше
* Введите следующую команду в командную строку:
```bash
pip install vkcoin
```
* Вы прекрасны!
# Начало работы
Для начала разработки, необходимо создать в своей папке исполняемый файл с расширением .py, например test.py. **Вы не можете назвать файл vkcoin.py**, так как это приведёт к конфликту. Теперь файл нужно открыть и импортировать библиотеку:
```python
import vkcoin
```
Библиотека содержит в себе **2 класса**:
- **VKCoinApi** - для работы с VKCoin API
- **VKCoinWS** - для получения CallBack сообщений о зачислении коинов

# VKCoinApi
```python
merchant = vkcoin.VKCoinApi(user_id=123456789, key='xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx')
```
|Параметр|Тип|Описание|
|-|-|-|
|user_id|Integer|ID аккаунта ВКонтакте|
|key|String|Ключ для взаимодействия с API|
# Методы
Необязательные параметры при вызове функций выделены _курсивом_.

[`get_payment_url`](https://vk.com/@hs-marchant-api?anchor=ssylka-na-oplatu) - получет ссылку на оплату VK Coin
```python
result = merchant.get_payment_url(amount=10, payload=78922, free_amount=False)
print(result)
```
|Параметр|Тип|Описание|
|-|-|-|
|amount|Float|Количество VK Coin для перевода|
|_payload_|Integer|Число от -2000000000 до 2000000000, вернется в списке транзаций|
|_free_amount_|Boolean|True, чтобы разрешить пользователю изменять сумму перевода|
#
[`get_transactions`](https://vk.com/@hs-marchant-api?anchor=poluchenie-spiska-tranzaktsy) - получает список ваших транзакций
```python
result = merchant.get_transactions(tx=[2])
print(result)
```
|Параметр|Тип|Описание|
|-|-|-|
|tx|List|Массив ID переводов для получения или [1] - 1000 последних транзакций со ссылок на оплату, [2] — 100 последних транзакций на текущий аккаунт|
|_last_tx_|Integer|Если указать номер последней транзакции, то будут возвращены только транзакции после указанной|
#
[`send_coins`](https://vk.com/@hs-marchant-api?anchor=perevod) - делает перевод другому пользователю
```python
result = merchant.send_coins(to_id, amount)
print(result)
```
|Параметр|Тип|Описание|
|-|-|-|
|amount|Float|Сумма перевода|
|to_id|Integer|ID аккаунта, на который будет совершён перевод|
#
[`get_user_balance`](https://vk.com/@hs-marchant-api?anchor=poluchenie-balansa) - возвращает баланс аккаунта
```python
result = merchant.get_user_balance(123456789, 987654321)
print(result)
```
|Тип|Описание|
|-|-|
Integer|ID аккаунтов, баланс которых нужно получить|
#
`get_my_balance` - возвращает ваш баланс
```python
result = merchant.get_my_balance()
print(result)
```
#
[`set_shop_name`](https://vk.com/@hs-marchant-api?anchor=nazvanie-magazina) - устанавливает название магазина

Обратите внимание что название может быть закешированно на срок до 5 часов. Сбросить кеш никак нельзя.
```python
merchant.set_shop_name(name='Best Shop Ever')
```
|Параметр|Тип|Описание|
|-|-|-|
|name|String|Новое название магазина|

# Callback
Оффициальный Callback. Все приведённые ниже функции находятся в классе **VKCoinApi**

`set_callback_endpoint` - устанавливает Endpoint
```python
merchant.set_callback_endpoint()
```
|Параметр|Тип|Описание|
|-|-|-|
|_address_|String|Адрес, на который будет поступать информация|
|_port_|Integer|Порт|
#
`remove_callback_endpoint` - удаляет Endpoint
```python
merchant.remove_callback_endpoint()
```
#
[`callback_start`](https://vk.com/@hs-marchant-api?anchor=callback-api) - запускает сервер для Callback
```python
merchant.callback_start()
```

# VKCoinWS _(CallBack)_
**Рекомендуется использовать новый [Сallback](https://github.com/crinny/vkcoin#callback)**

**VKCoin** для взаимодействия между клиентом и сервером использует протокол WebSocket.
Данный класс реализован для получения обратных вызовов при входящих транзакциях на аккаунт, доступ к которому может быть предоставлен одним из следующих параметров при создании объекта класса:
```python
callback = vkcoin.VKCoinWS(token, iframe_link)
```
|Параметр|Тип|Описание|
|-|-|-|
|token|String|acces_token вашего аккаунта **\***|
|iframe_link|String|ссылка на iframe сервиса VKCoin **\*\***|

**\*** получение токена - перейдите по [ссылке](https://vk.cc/9f4IXA), нажмите "Разрешить" и скопируйте часть адресной строки после `access_token=` и до `&expires_in` (85 символов)

Если при использовании способа выше вы получаете ошибку, перейдите по ссылке: `https://oauth.vk.com/token?grant_type=password&client_id=2274003&client_secret=hHbZxrka2uZ6jB1inYsH&username=LOGIN&password=PASSWORD`, перед этим заменив login и password на ваш логин и пароль. После перехода по этой ссылке вам будет выдан расширенный токен.

**\*\*** эту ссылку можно получить в коде страницы vk.com/coin
1.  Перейдите на [vk.com/coin](http://vk.com/coin)
2.  Используйте сочетание клавиш ```Ctrl + U``` для просмотра исходного кода страницы
3.  Откройте поиск, введите `sign=`
4.  Скопируйте найденную ссылку, содержащую параметр `sign`

После инициализации объекта необходимо зарегистрировать функцию, которая будет обрабатывать входящие платежи. Для этого используется декоратор `handler`
```python
@callback.handler
def your_func(data):
	do_something...
```
При получении обратного вызова - входящей транзакции - в зарегестрированную функцию возвращается объект класса `Entity`, который является абстракцией входящего перевода и содержит следующие параметры:
```python
data.user_id  # ваш ID
data.balance  # баланс вашего аккаунта 
data.user_from  # ID отправителя (инициатор входящей транзакции)
data.amount  # количество полученных коинов
```


# Примеры
Примеры расположены в отдельной [папке](https://github.com/crinny/vkcoin/tree/master/examples) репозитория.

# Где меня можно найти
Я готов ответить на ваши вопросы, связанные с библиотекой.
* [ВКонтакте Crinny](https://vk.com/crinny)   or  [ВКонтакте Spooti](https://vk.com/edgar_gorobchuk)
* [Telegram Crinny](https://t.me/truecrinny)  or  [Telegram Spooti](https://t.me/spooti)
* [Чат ВКонтакте по VK Coin API](https://vk.me/join/AJQ1d5eSUQ81wnwgfHSRktCi)
