import discord
from discord.ext import commands

import os
from dotenv import load_dotenv
import asyncio

load_dotenv()
DISCORD_TOKEN = os.getenv('TOKEN', '')

INITIAL_EXTENSIONS = [
    'modules.cmd',
]

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix=':', intents=intents)

async def load_extension():
    for cog in INITIAL_EXTENSIONS:
        await bot.load_extension(cog)

async def main():
    async with bot:
        await load_extension()
        await bot.start(DISCORD_TOKEN)

if __name__ == '__main__':
    asyncio.run(main())

