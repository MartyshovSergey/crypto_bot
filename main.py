import json
import requests


def get_info():
    """Получаем информацию о актуальных парах на бирже."""

    response = requests.get(url='https://yobit.net/api/3/info')

    with open('info.txt', 'w') as file:
        file.write(response.text)

    return response.text


def get_ticker(coin1='btc', coin2='usd'):
    """Получаем информацию о паре (парах) за последние 24 часа."""

    response = requests.get(url='https://yobit.net/api/3/ticker/{coin1}_{coin2}?ignore_invalid=1')

    with open('ticker.txt', 'w') as file:
        file.write(response.text)

    return response.text


def get_depth(coin1='btc', coin2='usd', limit=150):
    """ Возвращает информацию и выставленных на продажу ордерах."""

    response = requests.get(url='https://yobit.net/api/3/depth/{coin1}_{coin2}?limit={limit}&ignore_invalid=1')

    with open('depth.txt', 'w') as file:
        file.write(response.text)

    bids = response.json()[f'{coin1}_usd']['bids']

    total_bids_amount = 0

    for item in bids:
        price = item[0]
        coin_amount = item[1]

        total_bids_amount += price * coin_amount


    return f'Total bids: {total_bids_amount} $'


def get_trades(coin1='btc', coin2='usd', limit=150):
    """Получаем общую сумму проданных и купленных монет."""

    response = requests.get(url='https://yobit.net/api/3/trades/{coin1}_{coin2}?limit={limit}&ignore_invalid=1')

    with open('trades.txt', 'w') as file:
        file.write(response.text)

    total_trade_ask = 0
    total_trade_bid = 0

    for item in response.json()[f'{coin1}_{coin2}']:
        if item['type'] == 'ask':
            total_trade_ask += item['price'] * item['amount']
        else:
            total_trade_bid += item['price'] * item['amount']
    info = f'[-] TOTAL {coin1} SELL: {round(total_trade_ask, 2)} $\n[+] TOTAL {coin1} BUY: {round(total_trade_bid, 2)} $'

    return info


def main():
    print(get_trades(coin1="xrp"))


if __name__ == '__main__':
    main()
