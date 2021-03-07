import os
from discord.ext import commands, tasks
import discord


class ara_ng(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.Cog.listener()
    async def on_message(self, message):
      if not message.author.bot:
          ruizisan = os.path.join(os.path.dirname(__file__), 'ngwords.txt')
            with open(ruizisan, 'r', encoding='utf-8') as file:
                bad_words = [bad_word.strip().lower() for bad_word in file.readlines()]
                if any(bad_word in message.content for bad_word in bad_words):
                    await message.delete()


def setup(bot):
    bot.add_cog(ara_ng(bot))
