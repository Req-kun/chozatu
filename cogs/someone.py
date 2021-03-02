import discord
from discord.ext import commands
import random


class Someone(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.Cog.listener()
    async def on_message(self, message):
        if not message.content == '@someone':
            return
        if not message.author.guild_permissions.administrator:
            return
        member = random.choice(message.guild.members)
        await message.reply(member.mention, mention_author=False)
        return


def setup(bot):
    return bot.add_cog(Someone(bot))
