import discord
from discord.ext import commands
from discord_slash import cog_ext
from discord_slash import SlashCommand
from discord_slash import SlashContext

class Empty(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @cog_ext.cog_subcommand(
        base="fun", name="empty",
        base_description="楽しもう！", description="「空白」を送信いたします",
        guild_ids=[733707710784340100]
    )
    async def _empty(self, ctx):
        await ctx.respond(eat=True)
        await ctx.respond(eat=True)
        msg = await ctx.send(embeds=[discord.Embed()])
        await msg.edit(flags=4)
        return



def setup(bot):
    bot.add_cog(Empty(bot))
