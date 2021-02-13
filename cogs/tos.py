import discord
from discord.ext import commands
from discord_slash import cog_ext
from discord_slash import SlashCommand
from discord_slash import SlashContext
from random import randint

class Tos(commands.Cog):
    def __init__(self, bot):
        if not hasattr(bot, "slash"):
            # Creates new SlashCommand instance to bot if bot doesn't have.
            bot.slash = SlashCommand(bot, override_type=True, auto_register=True, auto_delete=True)
        self.bot = bot
        self.bot.slash.get_cog_commands(self)

    def cog_unload(self):
        self.bot.slash.remove_cog_commands(self)

    @cog_ext.cog_slash(name="tos", description="サーバールールを表示", guild_ids=[733707710784340100],
    options=[
    {
    "name": "rule",
    "description": "表示するルール",
    "type": 3,
    "required": True,
    "choices": [
        {
        "name": "基本ルール",
        "value": "basic"
        },
        {
        "name": "mcserver",
        "value": "mcserver"
        },
        {
        "name": "しりとり",
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
        "name": "表示する",
        "value": "True"
        },
        {
        "name": "表示しない",
        "value": "False"
        }
    ]
    }
    ])
    async def _tos(self, ctx, rule, visibility = 'False'):
        if visibility == 'True':
            if not self.bot.unei_role in ctx.author.roles:
                await ctx.send(content="このモードは運営のみ選択可能です。", complete_hidden=True)
                return

            await ctx.send(content=self.bot.rules[rule])
            return
        else:
            await ctx.send(content=self.bot.rules[rule], complete_hidden=True)



def setup(bot):
    bot.add_cog(Tos(bot))
