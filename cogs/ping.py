import discord
from discord.ext import commands
import asyncio
from datetime import datetime


class Ping(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.command(name="ping")
    async def _ping(self, ctx):
        now = datetime.now()
        msg = await ctx.send(embed=discord.Embed(title='計測中...', color=discord.Colour.dark_theme()))
        created = msg.created_at

        command_latency = (now - ctx.message.created_at).microseconds
        message_latency = (msg.created_at - now).microseconds
        socket_latency = self.bot.latency

        await msg.edit(content=f'Pong! :ping_pong:', embed=(discord.Embed(title='計測結果', description=f'websocket: `{round(socket_latency*1000, 1)}ms`\nmessage: `{round(message_latency/1000, 1)}`\ncommand: `{round(command_latency/1000, 1)}`')).set_footer(text='この計測値はあくまでも目安であり、正しくない可能性があります'))
        return

def setup(bot):
    return bot.add_cog(Ping(bot))
