import datetime
import os
from zoneinfo import ZoneInfo

import validators
from discord.ext import commands, tasks

import modules.parse_rss as parse_rss
from modules.db_operate import urlDatabase as db


# TODO テストケースを書く
class Commands(commands.Cog):
    times = [
        datetime.time(hour=10, minute=00, tzinfo=ZoneInfo("Asia/Tokyo")),
        datetime.time(hour=18, minute=30, tzinfo=ZoneInfo("Asia/Tokyo")),
    ]

    def __init__(self, bot):
        self.CHANNEL_ID = int(os.getenv("CHANNEL_ID", ""))
        self.db = db()
        self.bot = bot
        self._last_member = None

    @commands.Cog.listener()
    async def on_ready(self):
        print("Bot is ready!")
        self.loop.start()

    @commands.command()
    async def ping(self, ctx):
        await ctx.send("pong")

    @commands.command()
    async def add(self, ctx, url):
        # TODO: 引数が無い場合の処理を追加する
        if not validators.url(url):
            await ctx.send("Invalid URL")
            return
        elif len(url) == 0:
            await ctx.send("need url")
            return
        await ctx.send("Adding...")
        await ctx.send(self.db.addUrl(url))

    @commands.command()
    async def remove(self, ctx, arg):
        # TODO 引数が無い場合の処理を追加する
        if arg.isdigit():
            try:
                await ctx.send("Removing...")
                await ctx.send(self.db.removeUrl(int(arg)))
            except ValueError:
                await ctx.send("Invalid Number")
        elif len(arg) == 0:
            await ctx.send("need number")
        else:
            await ctx.send("Invalid Number")

    @commands.command(name="howtouse")
    async def _help(self, ctx):
        await ctx.send(
            """--- Discord RSS Bot ---
            :add <url> : Add RSS URL
            :remove <number> : Remove RSS URL
            :list : Show RSS URL List
            :show : Show RSS Entry
            :howtouse : Show this message

            --- RSS Entry ---
            <title>
            <link>
            --------------------
            """
        )

    @commands.command()
    async def list(self, ctx):
        _list = self.db.getData("*")
        send_msg = ""
        if len(_list) == 0:
            await ctx.send("No data")
            return
        for url in _list:
            send_msg += str(url[0]) + " : " + url[1] + "\n"
        try:
            await ctx.send(send_msg)
        except Exception as e:
            await ctx.send(e)

    @commands.command()
    async def show(self, ctx):
        urlList = self.db.getData("url")
        if len(urlList) == 0:
            await ctx.send("No data")
            return
        send_msg = ""
        for url in urlList:
            parsed = parse_rss.parse_rss(url[0])
            for entry in parsed:
                send_msg += (
                    entry["title"]
                    + "\n"
                    + "<"
                    + entry["link"]
                    + ">"
                    + "\n"
                    + "-" * 30
                    + "\n"
                )
        try:
            await ctx.send(send_msg)
            await ctx.send("Done!")
        except Exception as e:
            ctx.send(e)

    @tasks.loop(time=times)
    async def loop(self):
        await self.show()
        await self.bot.get_channel(self.CHANNEL_ID).send("Done!")


def setup(bot):
    return bot.add_cog(Commands(bot))
