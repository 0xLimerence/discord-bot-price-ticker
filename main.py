#!/usr/bin/env python3

import discord
from discord.ext import commands

import os

import config

class TickerBot(commands.AutoShardedBot):

    def __init__(self):
        client_intents = discord.Intents.all()
        client_intents.presences = False
        client_intents.members = False
        client_intents.message_content = False

        super().__init__(
            shard_ids=[x for x in range(0, config.SHARD_COUNT)],
            shard_count=config.SHARD_COUNT,
            command_prefix=commands.when_mentioned,
            case_insensitive=True,
            owner_id=config.OWNER_ID,
            max_messages=None,
            intents=client_intents,
            member_cache_flags=discord.MemberCacheFlags.none(),
            chunk_guilds_at_startup=False,
        )

        self.remove_command('help')

        for filename in os.listdir('./cogs'):
            if filename.endswith('.py') and filename not in ['config.py']:
                self.load_extension(f'cogs.{filename[:-3]}')

    def run(self):
        super().run(config.DISCORD_TOKEN, reconnect=True)
    
client = TickerBot()

def main():
    print('[*] Ticker bot started')
    client.run()

if __name__ == '__main__':
    main()