import discord
from discord.ext import commands
import aiohttp
import os
from json import loads

UB_API_TOKEN = os.environ.get('CHOZATU_UB_API_TOKEN')
url = 'https://unbelievaboat.com/api/v1/guilds/733707710784340100'
h = {'Authorization': UB_API_TOKEN}



class Money(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.command(name="money")
    @commands.is_owner()
    async def _money(self, ctx, mode, end):
        # c/money /users/123 put
        print()
        json = loads(ctx.message.content[len(ctx.prefix)+len(ctx.invoked_with)+len(mode)+len(end)+3:])
        async with aiohttp.ClientSession(headers=h) as session:
            if mode == 'patch':
                async with session.patch(url=f'{url}{end}', json=json) as r:
                    rjson = await r.json()
                    await ctx.send(rjson)
                    return
            if mode == 'put':
                async with session.put(url=f'{url}{end}', json=json) as r:
                    rjson = await r.json()
                    await ctx.send(rjson)
                    return
            if mode == 'get':
                async with session.get(url=f'{url}{end}', json=json) as r:
                    rjson = await r.json()
                    await ctx.send(rjson)
                    return

def setup(bot):
    return bot.add_cog(Money(bot))
