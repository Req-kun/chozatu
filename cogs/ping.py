import discord
from discord.ext import commands
import asyncio
class Ping(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.command(name="ping")
    async def _ping(self, ctx):
        await ctx.reply(f'Pong! :ping_pong: `{round(self.bot.latency*1000, 3)}ms`', mention_author=False, delete_after=10.0)
        await asyncio.sleep(10)
        await ctx.message.delete()
        return

def setup(bot):
    return bot.add_cog(Ping(bot))
