#!/usr/bin/env python3

import discord
from discord.ext import commands, tasks

import requests
from json import loads as parse

import config

class GetTickerPrice(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.ticker = config.TICKER
        self.convert = config.CONVERT
        self.convert_symbol = config.CONVERT_SYMBOL
        self.api_key = config.API_KEY
        self.base_url = 'https://min-api.cryptocompare.com/data/price'
        self.get_ticker_price_loop.start()
        
    @tasks.loop(minutes=15)
    async def get_ticker_price_loop(self):
        try:
            full_url = f'{self.base_url}?fsym={self.ticker}&tsyms={self.convert}&api_key={self.api_key}'

            r = requests.get(full_url)

            if r.status_code != 200:
                print(f'[!] Error getting price for ticker: HTTP {r.status_code}')
                return

            data = parse(r.text)
            price = data[self.convert]

            print(f'[+] Setting {self.ticker} to {self.convert_symbol}{price}')

            await self.client.change_presence(
                activity=discord.Activity(
                    type=discord.ActivityType.watching,
                    name=f'{self.convert_symbol}{price:.2f}'
                )
            )
        except Exception as error:
            print(f'[!] Error in get_ticker_price_loop(): {error}')

    @get_ticker_price_loop.before_loop
    async def before_get_ticker_price_loop(self):
        await self.client.wait_until_ready()
        print('[*] Status loop ready, starting...')

    def cog_unload(self):
        self.get_ticker_price_loop.cancel()

def setup(client):
    client.add_cog(GetTickerPrice(client))
