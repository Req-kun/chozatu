from discord.ext import commands
import discord


class Ng_word(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        for ng_word in self.bot.ng_words:
            if ng_word in message.content:
                await message.delete()
                return


def setup(bot):
    bot.add_cog(Ng_word(bot))
