import discord
from discord.ext import commands
import aiohttp
import os
from json import loads, dumps

UB_API_TOKEN = os.environ.get('CHOZATU_UB_API_TOKEN')
url = 'https://unbelievaboat.com/api/v1/guilds/'
h = {'Authorization': UB_API_TOKEN}



class Money(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.group()
    @commands.is_owner()
    async def money(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send(embed=discord.Embed(title='サブコマンド一覧', description='```get - 情報取得\nput - 値置き換え\npatch - 価増減```', delete_after=10.0))
            return


    # get user balance
    # api/v1/guilds/{guild_id}/users/{user_id}
    @money.command(name='get')
    async def _get(self, ctx, user_id):
        rep = await ctx.reply(embed=discord.Embed(title='Now requesting...', color=discord.Colour.dark_theme()), mention_author=False)
        async with aiohttp.ClientSession(headers=h) as session:
            async with session.get(url=f'{url}{ctx.guild.id}/users/{user_id}') as r:
                json = await r.json()
                embed = discord.Embed(color=0x00ffff)
                embed.add_field(name='Request url', value=f'```{url}{ctx.guild.id}/users/{user_id}```', inline=False)
                embed.add_field(name='Response json', value=f'```json\n{dumps(json)}```', inline=False)
                await rep.edit(embed=embed)
                return

    # put user balance
    # api/v1/guilds/{guild_id}/users/{user_id}
    @money.command(name='put')
    async def _put(self, ctx, user_id):
        rep = await ctx.reply(embed=discord.Embed(title='Now requesting...', color=discord.Colour.dark_theme()), mention_author=False)
        _json = ctx.message.content[len(f'{ctx.prefix}money put {user_id} '):]
        async with aiohttp.ClientSession(headers=h) as session:
            async with session.put(url=f'{url}{ctx.guild.id}/users/{user_id}', json=loads(_json)) as r:
                json = await r.json()
                embed = discord.Embed(color=0x00ffff)
                embed.add_field(name='Request url', value=f'```{url}{ctx.guild.id}/users/{user_id}```', inline=False)
                embed.add_field(name='Request payload', value=f'```json\n{_json}```', inline=False)
                embed.add_field(name='Response json', value=f'```json\n{dumps(json)}```', inline=False)
                await rep.edit(embed=embed)
                return

    # patch user balance
    # api/v1/guilds/{guild_id}/users/{user_id}
    @money.command(name='patch')
    async def _patch(self, ctx, user_id):
        rep = await ctx.reply(embed=discord.Embed(title='Now requesting...', color=discord.Colour.dark_theme()), mention_author=False)
        _json = ctx.message.content[len(f'{ctx.prefix}money patch {user_id} '):]
        async with aiohttp.ClientSession(headers=h) as session:
            async with session.patch(url=f'{url}{ctx.guild.id}/users/{user_id}', json=loads(_json)) as r:
                json = await r.json()
                embed = discord.Embed(color=0x00ffff)
                embed.add_field(name='Request url', value=f'```{url}{ctx.guild.id}/users/{user_id}```', inline=False)
                embed.add_field(name='Request payload', value=f'```json\n{_json}```', inline=False)
                embed.add_field(name='Response json', value=f'```json\n{dumps(json)}```', inline=False)
                await rep.edit(embed=embed)
                return



def setup(bot):
    return bot.add_cog(Money(bot))
