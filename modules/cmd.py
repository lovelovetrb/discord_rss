from discord.ext import commands
from discord.ext import tasks

from modules.db_operate import urlDatabase as db
import modules.parse_rss as parse_rss

import os
import datetime
from dotenv import load_dotenv
import validators

# TODO テストケースを書く
class Commands(commands.Cog):
    def __init__(self, bot):
        load_dotenv()
        self.CHANNEL_ID = int(os.getenv('CHANNEL_ID', ''))
        self.db = db()
        self.bot = bot
        self._last_member = None

    @commands.Cog.listener()
    async def on_ready(self):
        print('Bot is ready!')
        self.loop.start()

    @commands.command()
    async def add(self, ctx, url):
        # TODO 引数が無い場合の処理を追加する
        if not validators.url(url):
            await ctx.send('Invalid URL')
            return
        elif len(url) == 0:
            await ctx.send('need url')
            return
        await ctx.send('Adding...')
        await ctx.send(self.db.addUrl(url))

    @commands.command()
    async def remove(self, ctx, arg):
        # TODO 引数が無い場合の処理を追加する
        if(arg.isdigit()):
            try:
                await ctx.send('Removing...')
                await ctx.send(self.db.removeUrl(int(arg)))
            except ValueError:
                await ctx.send('Invalid Number')
        elif len(arg) == 0:
            await ctx.send('need number')
        else:
            await ctx.send('Invalid Number')

    @commands.command(name='howtouse')
    async def _help(self, ctx):
        await ctx.send(
            '''--- Discord RSS Bot ---
            :add <url> : Add RSS URL
            :remove <number> : Remove RSS URL
            :list : Show RSS URL List
            :show : Show RSS Entry
            :howtouse : Show this message

            --- RSS Entry ---
            <title>
            <link>
            --------------------
            '''
        )

    @commands.command()
    async def list(self, ctx):
        _list = self.db.getData('*')
        if len(_list) == 0:
            await ctx.send('No data')
            return
        for url in _list:
            await ctx.send(f'{url[0]} : {url[1]}')

    @commands.command()
    async def show(self, ctx):
        urlList = self.db.getData('url')
        if len(urlList) == 0:
            await ctx.send('No data')
            return
        for url in urlList:
            parsed = parse_rss.parse_rss(url[0])
            for entry in parsed:
                try:
                    await ctx.send(entry['title'])
                    await ctx.send(entry['link'])
                    await ctx.send('-' * 30)
                except Exception as e:
                    ctx.send(e)
        await ctx.send('Done!')

    utc = datetime.timezone.utc

    # If no tzinfo is given then UTC is assumed.
    # TODO 時間をconfig.yamlとかから変更できたら嬉しい
    times = [ datetime.time(hour=11, minute=00, tzinfo=utc),  datetime.time(hour=18, minute=30, tzinfo=utc)]
    @tasks.loop(times)
    async def loop(self):
        urlList = self.db.getData('url')
        if len(urlList) == 0:
            return
        for url in urlList:
            parsed = parse_rss.parse_rss(url[0])
            for entry in parsed:
                try:
                    await self.bot.get_channel(self.CHANNEL_ID).send(entry['title'])
                    await self.bot.get_channel(self.CHANNEL_ID).send(entry['link'])
                    await self.bot.get_channel(self.CHANNEL_ID).send('-' * 30)
                except Exception as e:
                    await self.bot.get_channel(self.CHANNEL_ID).send('Can\'t get entry')
                    await self.bot.get_channel(self.CHANNEL_ID).send(e)
        await self.bot.get_channel(self.CHANNEL_ID).send('Done!')

def setup(bot):
    return bot.add_cog(Commands(bot))
