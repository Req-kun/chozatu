import discord
from discord.ext import commands
from discord_slash import cog_ext
from discord_slash import SlashCommand
from discord_slash import SlashContext

class Soushoku_rem(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @cog_ext.cog_subcommand(base="fun", name="mdremover",
    base_description="楽しもう！", description="文字装飾を無効化する",
    guild_ids=[733707710784340100],
    options=[
        {
            "name": "MessageURL",
            "description": "MessageURL",
            "type": 3,
            "required": True
        }
    ])
    async def _soushoku_rem(self, ctx, message_url):
         
        msg = await self.bot.fetch_message(message_url)
        content = msg.content.replace('\\', '').replace('`', '\\`').replace('|', '\\|').replace('*', '\\*').replace('_', '\\_').replace('~', '\\~').replace('[', '\\[')
        await ctx.send(content, hidden=True)



def setup(bot):
    bot.add_cog(Soushoku_rem(bot))
