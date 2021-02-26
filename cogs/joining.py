import discord
from discord.ext import commands
from discord_slash import cog_ext
from discord_slash import SlashCommand
from discord_slash import SlashContext
import datetime


class Joining(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @cog_ext.cog_subcommand(base="fun", name="joining",
    base_description='楽しもう！', description='このサーバーに参加している期間',
    guild_ids=[733707710784340100],
    options=[
        {
            "name": "user",
            "description": "表示するユーザー ※未指定で自分",
            "type": 6,
            "required": False
        }
    ])
    async def _joining(self, ctx, user = None):
        now = datetime.datetime.now()
        if user == None:
            user = ctx.author
            joined = user.joined_at
            delta = now - joined
            t = trans(delta)
            embed = discord.Embed(
                title=str(user),
                description=f'{t.day}日 {t.hour}時間 {t.min}分 {t.sec}秒 {t.milli}ミリ秒 {t.micro}マイクロ秒',
                color=user.color
            )
            await ctx.send(embeds=[embed])
            return

        joined = user.joined_at
        delta = now - joined
        t = trans(delta)
        embed = discord.Embed(
            title=str(user),
            description=f'{t.day}日 {t.hour}時間 {t.min}分 {t.sec}秒 {t.milli}ミリ秒 {t.micro}マイクロ秒',
            color=user.color
        )
        await ctx.send(embeds=[embed])
        return


class Delta_to:
    def __init__(self, day, hour, min, sec, milli, micro):
        self.day = day
        self.hour = hour
        self.min = min
        self.sec = sec
        self.milli = milli
        self.micro = micro
    def __str__(self):
        return f"Delta_to(day={self.day}, hour={self.hour}, min={self.min}, sec={self.sec}, milli={self.milli}, micro={self.micro})"

def trans(delta):
    day = delta.days

    hour = delta.seconds // 3600

    min = (delta.seconds - hour * 3600) // 60

    sec = delta.seconds - (hour * 3600) - (min * 60)

    milli = int(delta.microseconds / 1000)
    micro = int(delta.microseconds - milli * 1000)
    return Delta_to(day, hour, min, sec, milli, micro)


def setup(bot):
    bot.add_cog(Joining(bot))
