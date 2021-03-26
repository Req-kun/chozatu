import discord
from discord.ext import commands
from discord_slash import cog_ext
from discord_slash import SlashCommand
from discord_slash import SlashContext
from random import randint

class Tos(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @cog_ext.cog_subcommand(base="server", name="tos",
    base_description="サーバー関係", description="サーバールールを表示",
    guild_ids=[733707710784340100],
    options=[
        {
            "name": "rule",
            "description": "表示するルール",
            "type": 3,
            "required": True,
            "choices": [
                {
                    "name": "basic",
                    "value": "basic"
                },
                {
                    "name": "mcserver",
                    "value": "mcserver"
                },
                {
                    "name": "siritori",
                    "value": "siritori"
                }
            ]
        },
        {
            "name": "visibility",
            "description": "送信されるルールが全員から見えるようにするか ※表示する は運営のみ選択可能 | デフォルト：表示しない",
            "type": 3,
            "required": False,
            "choices": [
                {
                "name": "visible",
                "value": "True"
                },
                {
                "name": "invisible",
                "value": "False"
                }
            ]
        }
    ])
    async def _tos(self, ctx, rule, visibility = 'False'):
        await ctx.respond(eat=True)
        if visibility == 'True':
            if not self.bot.unei_role in ctx.author.roles:
                await ctx.send(content="このモードは運営のみ選択可能です。", hidden=True)
                return

            await ctx.send(content=self.bot.rules[rule])
            return
        else:
            await ctx.send(content=self.bot.rules[rule], hidden=True)



def setup(bot):
    bot.add_cog(Tos(bot))
