import discord
from discord.ext import commands
from discord_slash import cog_ext
from discord_slash import SlashCommand
from discord_slash import SlashContext
from random import randint

class Ukayg(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @cog_ext.cog_subcommand(base="fun", name="ukayg",
    base_description="楽しもう！", description="おえういあ ← ukayg ← あいうえお",
    guild_ids=[733707710784340100],
    options=[
        {
            "name": "sentence",
            "description": "文字列",
            "type": 3,
            "required": True
        }
    ])
    async def _ukayg(self, ctx, sentence):
        await ctx.send(sentence[::-1])
        return



def setup(bot):
    bot.add_cog(Ukayg(bot))
